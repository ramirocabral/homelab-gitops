# homelab-gitops

Everything that runs in the homelab's k8s cluster, deployed by Argo CD. The machines and the
cluster itself are provisioned from [homelab](https://github.com/ramirocabral/homelab).

## How it works

Argo CD runs a root Application, `apps`, that syncs every file in `apps/`. Each of those files
is the Application for one component: a Helm chart, its values from `values/<name>/`, and any
extra manifests from `workloads/<name>/`. Everything syncs automatically, with prune and
self-heal.

```text
bootstrap/argocd/root-app.yaml
        │
        ▼
     [ apps ]   root Application
        │       one Application per apps/<name>.yaml
        ▼
    [ <name> ] ──> Helm chart (upstream repo or the app's own repo)
               ├──> values/<name>/values.yaml
               └──> workloads/<name>/   extra manifests, SealedSecrets
```

Cilium and Argo CD are installed by hand from `bootstrap/`, since the cluster needs them before
Argo can sync anything. Secrets are committed as SealedSecrets.

## Repository structure

```text
homelab-gitops/
├── bootstrap/   Cilium and Argo CD, installed by hand
├── apps/        One Argo CD Application per component
├── values/      Helm values, one folder per app
├── workloads/   Extra manifests and SealedSecrets, one folder per app
├── scripts/     SealedSecret helper and alerting doc generator
└── docs/        Generated alerting reference
```

## Adding an app

1. Add `apps/<name>.yaml`.
2. Put its Helm values in `values/<name>/` and any extra manifests in `workloads/<name>/`.
3. Push. Argo CD picks it up.
