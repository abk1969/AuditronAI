#!/bin/bash
set -e

echo "🚀 Configuration de l'environnement de production..."

# Créer les dossiers nécessaires
mkdir -p k8s/production/{base,overlays}

# Configuration de base Kubernetes
cat > k8s/production/base/kustomization.yaml << EOF
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - deployment.yaml
  - service.yaml
  - ingress.yaml
  - configmap.yaml
  - secrets.yaml

commonLabels:
  app: auditronai
  env: production
EOF

# Déploiement principal
cat > k8s/production/base/deployment.yaml << EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: auditronai
spec:
  replicas: 3
  selector:
    matchLabels:
      app: auditronai
  template:
    spec:
      containers:
      - name: backend
        image: auditronai-backend:latest
        resources:
          requests:
            cpu: "500m"
            memory: "512Mi"
          limits:
            cpu: "1000m"
            memory: "1Gi"
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
      - name: frontend
        image: auditronai-frontend:latest
        resources:
          requests:
            cpu: "200m"
            memory: "256Mi"
          limits:
            cpu: "500m"
            memory: "512Mi"
EOF

# Service
cat > k8s/production/base/service.yaml << EOF
apiVersion: v1
kind: Service
metadata:
  name: auditronai
spec:
  ports:
  - name: http
    port: 80
    targetPort: 8000
  - name: https
    port: 443
    targetPort: 8000
  selector:
    app: auditronai
EOF

# Ingress
cat > k8s/production/base/ingress.yaml << EOF
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: auditronai
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts:
    - api.auditronai.com
    secretName: auditronai-tls
  rules:
  - host: api.auditronai.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: auditronai
            port:
              number: 80
EOF

echo "✅ Configuration de production générée avec succès" 