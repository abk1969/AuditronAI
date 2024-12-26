#!/bin/bash
set -e

echo "🔄 Configuration de GitHub Actions..."

# Créer le dossier des workflows
mkdir -p .github/workflows

# Workflow principal CI/CD
cat > .github/workflows/main.yml << EOF
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
          
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install poetry
          poetry install
          
      - name: Run tests
        run: poetry run pytest
        
      - name: Run security checks
        run: poetry run bandit -r AuditronAI/

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: \${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: \${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: eu-west-1
          
      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1
        
      - name: Build and push Docker image
        env:
          ECR_REGISTRY: \${{ steps.login-ecr.outputs.registry }}
          IMAGE_TAG: \${{ github.sha }}
        run: |
          docker build -t \$ECR_REGISTRY/auditronai:\$IMAGE_TAG .
          docker push \$ECR_REGISTRY/auditronai:\$IMAGE_TAG

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to production
        env:
          KUBE_CONFIG: \${{ secrets.KUBE_CONFIG }}
        run: |
          echo "\$KUBE_CONFIG" > kubeconfig.yaml
          export KUBECONFIG=kubeconfig.yaml
          kubectl apply -k k8s/overlays/production
EOF

echo "✅ GitHub Actions configuré avec succès" 