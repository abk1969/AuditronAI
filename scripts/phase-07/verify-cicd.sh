#!/bin/bash
set -e

echo "🔍 Vérification de la configuration CI/CD..."

# Vérifier GitHub Actions
check_github_actions() {
    echo "Vérification de GitHub Actions..."
    if [ -f ".github/workflows/main.yml" ]; then
        echo "✅ Configuration GitHub Actions présente"
    else
        echo "❌ Configuration GitHub Actions manquante"
        return 1
    fi
}

# Vérifier ArgoCD
check_argocd() {
    echo "Vérification d'ArgoCD..."
    if kubectl get pods -n argocd | grep -q "argocd-server"; then
        echo "✅ ArgoCD opérationnel"
    else
        echo "❌ ArgoCD non disponible"
        return 1
    fi
}

# Vérifier Jenkins
check_jenkins() {
    echo "Vérification de Jenkins..."
    if curl -s http://localhost:8080 > /dev/null; then
        echo "✅ Jenkins opérationnel"
    else
        echo "❌ Jenkins non disponible"
        return 1
    fi
}

# Vérifier SonarQube
check_sonarqube() {
    echo "Vérification de SonarQube..."
    if curl -s http://localhost:9000 > /dev/null; then
        echo "✅ SonarQube opérationnel"
    else
        echo "❌ SonarQube non disponible"
        return 1
    fi
}

# Exécuter toutes les vérifications
check_github_actions
check_argocd
check_jenkins
check_sonarqube

echo "✅ Vérification CI/CD terminée avec succès" 