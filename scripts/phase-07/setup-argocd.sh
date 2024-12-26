#!/bin/bash
set -e

echo "🚀 Configuration d'ArgoCD..."

# Installation d'ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Attendre que ArgoCD soit prêt
echo "Attente du démarrage d'ArgoCD..."
kubectl wait --for=condition=available --timeout=300s deployment/argocd-server -n argocd

# Configuration de l'application
cat > k8s/argocd/application.yaml << EOF
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: auditronai
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/votre-org/auditronai.git
    targetRevision: HEAD
    path: k8s/overlays/production
  destination:
    server: https://kubernetes.default.svc
    namespace: auditronai
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
EOF

kubectl apply -f k8s/argocd/application.yaml

echo "✅ ArgoCD configuré avec succès" 