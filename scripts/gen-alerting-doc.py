#!/usr/bin/env python3
"""
gen-alerting-doc.py — genera docs/alerting.md a partir del chart y los values.

Renderiza kube-prometheus-stack con los values del repo y vuelca en un solo
documento el ruteo de Alertmanager, los receivers, los inhibit rules, el
template de Telegram y todas las reglas de alerta, que de otro modo quedan
repartidas en decenas de objetos PrometheusRule generados por el chart.

Uso:
  scripts/gen-alerting-doc.py            # escribe docs/alerting.md
  scripts/gen-alerting-doc.py --check    # falla si el doc esta desactualizado
"""

import argparse
import pathlib
import subprocess
import sys
import tempfile

import yaml

REPO = pathlib.Path(__file__).resolve().parent.parent
APP = REPO / "apps" / "kube-prometheus-stack.yaml"
VALUES = REPO / "values" / "kube-prometheus-stack" / "values.yaml"
OUT = REPO / "docs" / "alerting.md"

# chat_id es un entero: si el placeholder sigue puesto, helm falla al renderizar.
PLACEHOLDER_CHAT_ID = "-1000000000000"


def chart_coords():
    """Saca repoURL y targetRevision de la Application, para no duplicar la version."""
    app = yaml.safe_load(APP.read_text())
    for src in app["spec"]["sources"]:
        if src.get("chart") == "kube-prometheus-stack":
            return src["repoURL"], src["targetRevision"]
    sys.exit("no encontre la source del chart en apps/kube-prometheus-stack.yaml")


def render():
    repo_url, version = chart_coords()
    values = VALUES.read_text().replace("REEMPLAZAR_CHAT_ID", PLACEHOLDER_CHAT_ID)
    with tempfile.NamedTemporaryFile("w", suffix=".yaml") as tmp:
        tmp.write(values)
        tmp.flush()
        out = subprocess.run(
            ["helm", "template", "kps", "kube-prometheus-stack",
             "--repo", repo_url, "--version", version,
             "-n", "observability", "-f", tmp.name],
            capture_output=True, text=True,
        )
    if out.returncode != 0:
        sys.exit(f"helm template fallo:\n{out.stderr}")
    return version, list(yaml.safe_load_all(out.stdout))


def local_rules():
    """PrometheusRule propios del repo: el chart no los conoce."""
    found = []
    for path in sorted((REPO / "workloads").rglob("*.yaml")):
        try:
            for d in yaml.safe_load_all(path.read_text()):
                if d and d.get("kind") == "PrometheusRule":
                    d["_origen"] = str(path.relative_to(REPO))
                    found.append(d)
        except yaml.YAMLError:
            continue
    return found


def collect(docs):
    rules, am_cfg, templates = [], None, {}
    for d in docs:
        if not d:
            continue
        if d.get("kind") == "PrometheusRule":
            rules.append(d)
        elif d.get("kind") == "Secret" and d["metadata"]["name"].endswith("-alertmanager"):
            import base64
            for k, v in (d.get("data") or {}).items():
                text = base64.b64decode(v).decode()
                if k == "alertmanager.yaml":
                    am_cfg = yaml.safe_load(text)
                elif k.endswith(".tmpl"):
                    templates[k] = text
            for k, v in (d.get("stringData") or {}).items():
                if k == "alertmanager.yaml":
                    am_cfg = yaml.safe_load(v)
                elif k.endswith(".tmpl"):
                    templates[k] = v
    return rules + local_rules(), am_cfg, templates


def fmt_matchers(node):
    m = node.get("matchers") or []
    if not m:
        for key, op in (("match", "="), ("match_re", "=~")):
            m += [f"{k} {op} {v!r}" for k, v in (node.get(key) or {}).items()]
    return ", ".join(m) if m else "(todo lo que no matchee arriba)"


def route_tree(node, out, depth=0):
    pad = "  " * depth
    bits = []
    for key in ("group_by", "group_wait", "group_interval", "repeat_interval"):
        if key in node:
            val = node[key]
            bits.append(f"{key}={','.join(val) if isinstance(val, list) else val}")
    cond = "raiz" if depth == 0 else fmt_matchers(node)
    out.append(f"{pad}- **{cond}** → `{node.get('receiver', '(hereda)')}`"
               + (f"  · {' · '.join(bits)}" if bits else ""))
    for child in node.get("routes") or []:
        route_tree(child, out, depth + 1)


def alert_rows(rules):
    rows = []
    for pr in rules:
        src = pr.get("_origen") or pr["metadata"]["name"].replace("kube-prometheus-stack-", "")
        for g in pr["spec"].get("groups", []):
            for r in g.get("rules", []):
                if "alert" in r:
                    rows.append({
                        "name": r["alert"],
                        "sev": (r.get("labels") or {}).get("severity", "-"),
                        "for": r.get("for", "-"),
                        "group": g["name"],
                        "src": src,
                        "propia": "_origen" in pr,
                        "expr": " ".join(str(r["expr"]).split()),
                        "summary": (r.get("annotations") or {}).get("summary", ""),
                        "runbook": (r.get("annotations") or {}).get("runbook_url", ""),
                    })
    return rows


def recording_rows(rules):
    rows = []
    for pr in rules:
        for g in pr["spec"].get("groups", []):
            for r in g.get("rules", []):
                if "record" in r:
                    rows.append((g["name"], r["record"]))
    return rows


SEV_ORDER = {"critical": 0, "warning": 1, "info": 2, "none": 3, "-": 4}


def build(version, rules, am_cfg, templates):
    alerts = alert_rows(rules)
    records = recording_rows(rules)
    o = []
    a = o.append

    a("# Alerting — referencia")
    a("")
    a(f"> Generado por `scripts/gen-alerting-doc.py` desde el chart "
      f"`kube-prometheus-stack {version}` y `values/kube-prometheus-stack/values.yaml`.")
    a("")
    counts = {}
    for r in alerts:
        counts[r["sev"]] = counts.get(r["sev"], 0) + 1
    resumen = " · ".join(f"{k}: {v}" for k, v in sorted(counts.items(), key=lambda x: SEV_ORDER.get(x[0], 9)))
    propias = sum(1 for r in rules if "_origen" in r)
    a(f"**{len(alerts)} alertas** ({resumen}) y **{len(records)} recording rules**, "
      f"repartidas en {len(rules)} objetos `PrometheusRule`: "
      f"{len(rules) - propias} los genera el chart, {propias} son propios del repo.")
    a("")

    a("## Ruteo")
    a("")
    a("Primera coincidencia gana: una alerta cae en **una sola** rama.")
    a("")
    route_tree(am_cfg["route"], o)
    a("")

    a("## Receivers")
    a("")
    for rcv in am_cfg.get("receivers", []):
        name = rcv["name"]
        kinds = [k.replace("_configs", "") for k in rcv if k != "name"]
        a(f"### `{name}`")
        if not kinds:
            a("")
            a("Sin destino: descarta la alerta a propósito.")
            a("")
            continue
        for k in kinds:
            for cfg in rcv[f"{k}_configs"]:
                a("")
                a(f"- tipo: **{k}**")
                for key, val in cfg.items():
                    if key == "message":
                        val = "(ver template abajo)"
                    a(f"  - `{key}`: `{val}`")
        a("")

    a("## Inhibit rules")
    a("")
    a("Silencian la alerta *target* mientras exista la *source* con las mismas labels de `equal`.")
    a("")
    a("| # | source | target | equal |")
    a("|---|--------|--------|-------|")
    for i, ir in enumerate(am_cfg.get("inhibit_rules", []), 1):
        s = ", ".join(ir.get("source_matchers") or []) or "—"
        t = ", ".join(ir.get("target_matchers") or []) or "—"
        e = ", ".join(ir.get("equal") or []) or "—"
        a(f"| {i} | `{s}` | `{t}` | `{e}` |")
    a("")

    if templates:
        a("## Templates")
        a("")
        for name, body in templates.items():
            a(f"### `{name}`")
            a("")
            a("```gotemplate")
            a(body.rstrip())
            a("```")
            a("")

    a("## Alertas")
    a("")
    a("### Índice")
    a("")
    a("| Alerta | Sev | for | Grupo |")
    a("|--------|-----|-----|-------|")
    for r in sorted(alerts, key=lambda x: (SEV_ORDER.get(x["sev"], 9), x["name"])):
        a(f"| [{r['name']}](#{r['name'].lower()}) | `{r['sev']}` | `{r['for']}` | {r['group']} |")
    a("")

    a("### Detalle")
    a("")
    by_group = {}
    for r in alerts:
        by_group.setdefault(r["group"], []).append(r)
    for group in sorted(by_group):
        a(f"#### {group}")
        a("")
        first = by_group[group][0]
        origen = (f"`{first['src']}` (propio del repo)" if first["propia"]
                  else f"`kube-prometheus-stack-{first['src']}` (generado por el chart)")
        a(f"<sub>PrometheusRule: {origen}</sub>")
        a("")
        for r in sorted(by_group[group], key=lambda x: (SEV_ORDER.get(x["sev"], 9), x["name"])):
            a(f"##### {r['name']}")
            a("")
            a(f"`{r['sev']}` · `for: {r['for']}`" + (f" · [runbook]({r['runbook']})" if r["runbook"] else ""))
            a("")
            if r["summary"]:
                a(f"{r['summary']}")
                a("")
            a("```promql")
            a(r["expr"])
            a("```")
            a("")

    a("## Recording rules")
    a("")
    a("| Grupo | Serie |")
    a("|-------|-------|")
    for g, rec in sorted(records):
        a(f"| {g} | `{rec}` |")
    a("")

    return "\n".join(o) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="no escribe: sale 1 si docs/alerting.md quedo desactualizado")
    args = ap.parse_args()

    version, docs = render()
    rules, am_cfg, templates = collect(docs)
    if am_cfg is None:
        sys.exit("no encontre el Secret de Alertmanager en el render")
    content = build(version, rules, am_cfg, templates)

    if args.check:
        if not OUT.exists() or OUT.read_text() != content:
            sys.exit(f"{OUT.relative_to(REPO)} esta desactualizado: corre scripts/gen-alerting-doc.py")
        print(f"{OUT.relative_to(REPO)} al dia")
        return

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(content)
    n_alerts = len(alert_rows(rules))
    n_rec = len(recording_rows(rules))
    print(f"escrito {OUT.relative_to(REPO)} — {n_alerts} alertas, {n_rec} recording rules, "
          f"{len(rules)} PrometheusRule, chart {version}")


if __name__ == "__main__":
    main()
