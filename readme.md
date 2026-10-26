To resume the GitOps lab
1. Start the kind cluster container back up


docker start argocd-lab-control-plane
2. Wait ~20-30s, then confirm the cluster is reachable


kubectl get nodes
kubectl get pods -n argocd
Give it a minute if pods show Unknown/not-ready right after start — that's normal while they settle.

3. Re-open the port-forward to ArgoCD (run in background)


nohup kubectl port-forward svc/argocd-server -n argocd 8080:443 > /tmp/argocd-pf.log 2>&1 < /dev/null &
disown
4. Log back into the ArgoCD CLI


ADMIN_PW=$(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d)
argocd login localhost:8080 --username admin --password "$ADMIN_PW" --insecure
unset ADMIN_PW

kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d; echo


5. Check the app


argocd app get argocd-lab-dev
It should come back Synced/Healthy since nothing in the cluster state changed — you just paused and resumed the container.

Things to remember for next time
App name is argocd-lab-dev (not hello-dev), deployed as dev-hello-gitops in namespace argocd-lab-dev
dex-server, notifications-controller, and applicationset-controller are scaled to 0 — intentional, to fit Docker Desktop's memory budget; leave them at 0 unless you need SSO/notifications/ApplicationSets
Docker Desktop memory is set to ~6GB — don't lower it, or you'll hit the OOMKill crash-loop from earlier again
If kubectl/argocd time out with TLS handshake errors after a long sleep/wake of your Mac, that's the same Docker Desktop networking glitch — docker restart argocd-lab-control-plane fixes it