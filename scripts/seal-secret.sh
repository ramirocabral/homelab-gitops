#!/usr/bin/env bash
#
# seal-secret.sh — crea un SealedSecret listo para commitear.
#
# Uso:
#   scripts/seal-secret.sh -n NAMESPACE -s NAME [-o OUTFILE] \
#       [--from-literal k=v ...] [--from-file k=path ...] [--from-env-file path ...]
#
#   scripts/seal-secret.sh -n NAMESPACE -s NAME [-o OUTFILE] \
#       --docker-server SERVER --docker-username USER
#
#   Sin ningun --from-*  -> modo interactivo (pregunta key y value oculto).
#   Con --docker-server  -> Secret para bajar imagenes (dockerconfigjson), para
#                           imagePullSecrets. El password/token se pide oculto.
#   Sin -o OUTFILE       -> workloads/<namespace>/<name>.sealedsecret.yaml
#                           (relativo a la raiz del repo).
#
# Env vars opcionales:
#   SEALED_CONTROLLER_NAME  (default: sealed-secrets-controller)
#   SEALED_CONTROLLER_NS    (default: sealed-secrets)
#   SEALED_SCOPE            (default: strict | namespace-wide | cluster-wide)

set -euo pipefail

CONTROLLER_NAME="${SEALED_CONTROLLER_NAME:-sealed-secrets-controller}"
CONTROLLER_NS="${SEALED_CONTROLLER_NS:-sealed-secrets}"
SCOPE="${SEALED_SCOPE:-strict}"

NAMESPACE="" NAME="" OUTFILE=""
DOCKER_SERVER="" DOCKER_USER=""
CREATE_ARGS=()

die() { echo "error: $*" >&2; exit 1; }

usage() {
  cat >&2 <<'EOF'
Uso: seal-secret.sh -n NAMESPACE -s NAME [-o OUTFILE] [--from-literal k=v ...] [--from-file k=path ...] [--from-env-file path ...]
     seal-secret.sh -n NAMESPACE -s NAME [-o OUTFILE] --docker-server SERVER --docker-username USER
  -n, --namespace     namespace del Secret (requerido)
  -s, --name          nombre del Secret (requerido)
  -o, --out           archivo de salida (default: workloads/<ns>/<name>.sealedsecret.yaml)
  --from-literal      par key=value (repetible)
  --from-file         key=path a archivo (repetible)
  --from-env-file     archivo KEY=VALUE, una key por linea (repetible)
  --docker-server     registry (ej: ghcr.io); arma un Secret para imagePullSecrets
  --docker-username   usuario del registry (requerido con --docker-server)
  -h, --help          esta ayuda
Sin --from-*: modo interactivo (valor oculto).
Con --docker-server: pide el password/token oculto.
EOF
  exit "${1:-0}"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -n|--namespace) NAMESPACE="${2:?}"; shift 2 ;;
    -s|--name|--secret) NAME="${2:?}"; shift 2 ;;
    -o|--out) OUTFILE="${2:?}"; shift 2 ;;
    --from-literal) CREATE_ARGS+=(--from-literal="${2:?}"); shift 2 ;;
    --from-file) CREATE_ARGS+=(--from-file="${2:?}"); shift 2 ;;
    --from-env-file) CREATE_ARGS+=(--from-env-file="${2:?}"); shift 2 ;;
    --docker-server) DOCKER_SERVER="${2:?}"; shift 2 ;;
    --docker-username) DOCKER_USER="${2:?}"; shift 2 ;;
    -h|--help) usage 0 ;;
    *) echo "argumento desconocido: $1" >&2; usage 1 ;;
  esac
done

command -v kubectl  >/dev/null || die "falta kubectl"
command -v kubeseal >/dev/null || die "falta kubeseal (Arch: sudo pacman -S kubeseal)"
[[ -n "$NAMESPACE" ]] || { echo "falta -n NAMESPACE" >&2; usage 1; }
[[ -n "$NAME"      ]] || { echo "falta -s NAME"      >&2; usage 1; }

TYPE=generic
if [[ -n "$DOCKER_SERVER" || -n "$DOCKER_USER" ]]; then
  [[ -n "$DOCKER_SERVER" && -n "$DOCKER_USER" ]] || die "--docker-server y --docker-username van juntos"
  [[ ${#CREATE_ARGS[@]} -eq 0 ]] || die "--docker-server no se combina con --from-*"
  # El token se pide oculto por lo mismo que el modo interactivo: no queda en history.
  read -r -s -p "password/token de $DOCKER_USER en $DOCKER_SERVER (oculto): " pw; echo
  [[ -n "${pw:-}" ]] || die "password vacio"
  TYPE=docker-registry
  CREATE_ARGS=(--docker-server="$DOCKER_SERVER" --docker-username="$DOCKER_USER" --docker-password="$pw")
# Sin --from-*: pedir key/valor interactivo (valor oculto, no queda en history).
elif [[ ${#CREATE_ARGS[@]} -eq 0 ]]; then
  read -r -p "key: " k
  [[ -n "${k:-}" ]] || die "key vacia"
  read -r -s -p "value (oculto): " v; echo
  CREATE_ARGS+=(--from-literal="$k=$v")
fi

# Default OUTFILE relativo a la raiz del repo.
if [[ -z "$OUTFILE" ]]; then
  repo_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
  OUTFILE="$repo_root/workloads/$NAMESPACE/$NAME.sealedsecret.yaml"
fi
mkdir -p "$(dirname "$OUTFILE")"

# Verificar que el controller este accesible (baja su cert publica).
kubeseal --controller-name "$CONTROLLER_NAME" --controller-namespace "$CONTROLLER_NS" \
  --fetch-cert >/dev/null 2>&1 \
  || die "no pude contactar el controller $CONTROLLER_NAME/$CONTROLLER_NS (esta corriendo? kubecontext ok?)"

kubectl create secret "$TYPE" "$NAME" \
  --namespace "$NAMESPACE" \
  "${CREATE_ARGS[@]}" \
  --dry-run=client -o yaml \
| kubeseal --format yaml \
    --scope "$SCOPE" \
    --controller-name "$CONTROLLER_NAME" \
    --controller-namespace "$CONTROLLER_NS" \
  > "$OUTFILE"

echo "OK -> $OUTFILE"
echo "   secret '$NAME' en ns '$NAMESPACE' (scope=$SCOPE)"
echo "   commitea ese archivo; Argo + el controller crean el Secret real."
