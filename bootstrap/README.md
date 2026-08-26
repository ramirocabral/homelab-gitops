# bootstrap/

Day-0, **imperative** cluster setup. Everything here is applied **by hand**
(`helm install` / `kubectl apply`) and is **NOT reconciled by Argo CD**.

Why it lives outside Argo: these components are what Argo *runs on top of*.
Argo cannot manage the CNI it depends on to run — bootstrapping it via an
in-cluster GitOps controller is a chicken-and-egg. So it stays here, and the
root ApplicationSet is scoped to `apps/*` (never the repo root) so it never
tries to reconcile this folder.

## cilium/

CNI + kube-proxy replacement + LoadBalancer IPs announced on the LAN over ARP.
Install order:

```bash
export KUBECONFIG=.../ansible/kubeconfig
helm repo add cilium https://helm.cilium.io && helm repo update cilium
helm install cilium cilium/cilium --version 1.20.0 -n kube-system -f cilium/values.yaml
cilium status --wait
kubectl apply -f cilium/lb-pool.yaml
kubectl apply -f cilium/l2-announcement.yaml
```

`lab-pool` is `192.168.9.240-254`, carved out of the node LAN.

## argocd/

GitOps controller. Installed once by hand (it's what everything in `apps/` runs
under), then it manages itself and every app from git. The version is pinned (not
`stable`) so a rebuild reproduces the exact same install.

```bash
# 1) Install Argo CD 
kubectl create namespace argocd
kubectl apply -n argocd --server-side --force-conflicts \
  -f https://raw.githubusercontent.com/argoproj/argo-cd/v2.13.2/manifests/install.yaml
kubectl -n argocd rollout status deploy/argocd-server

# 2) Run argocd-server in insecure (HTTP) mode: TLS is terminated upstream at the
#    Envoy Gateway (HTTPRoute -> argocd-server:80), so the backend must not do its
#    own TLS or it redirect-loops. Sets server.insecure in argocd-cmd-params-cm.
kubectl patch configmap argocd-cmd-params-cm -n argocd \
  --type merge -p '{"data":{"server.insecure":"true"}}'
kubectl rollout restart deployment argocd-server -n argocd

# Seed the root ApplicationSet -- from here on, apps/ is fully GitOps-managed.
kubectl apply -f argocd/root-appset.yaml
```

After step 2, deploying an app = committing a folder under `apps/`; Argo picks it
up on its own. See `apps/README.md`.
