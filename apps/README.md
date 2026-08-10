# apps/

Every subdirectory here becomes one Argo CD Application automatically, via the
root ApplicationSet (git directory generator) in
`bootstrap/argocd/root-appset.yaml`.

## Adding an app

Create a folder `apps/<name>/`. The Application will be named `<name>` and its
resources deployed into a namespace also called `<name>` (auto-created). The
folder can contain any of:

- **plain manifests** — `*.yaml` with Kubernetes objects.
- **kustomize** — a `kustomization.yaml`.
- **a Helm chart** — `Chart.yaml` + `values.yaml`. To install an upstream chart,
  use an *umbrella* chart that declares it as a dependency, e.g.:

  ```yaml
  # apps/cert-manager/Chart.yaml
  apiVersion: v2
  name: cert-manager
  version: 0.0.0
  dependencies:
    - name: cert-manager
      version: v1.16.2
      repository: https://charts.jetstack.io
  ```

  and put your overrides in `apps/cert-manager/values.yaml`.

## Removing an app

Delete its folder. The ApplicationSet drops the Application and `prune: true`
removes the resources from the cluster.

## Secrets

Never commit plaintext Secrets. This repo uses **Sealed Secrets**: commit the
encrypted `SealedSecret`, the controller decrypts it in-cluster. (The Sealed
Secrets controller itself is deployed as one of these apps.)
