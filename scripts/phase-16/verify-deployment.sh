#!/bin/bash
set -e

# Ce script vérifie la configuration du déploiement et de la production
# Il contrôle :
# - Les configurations de déploiement
# - L'environnement de production
# - La surveillance
# - Les procédures d'urgence

echo "🔍 Vérification du déploiement et de la production..."

# Vérifier le déploiement
check_deployment() {
    echo "Vérification du déploiement..."
    
    if [ -f "deployment/environments/environments.yaml" ] && \
       [ -f "deployment/configs/deployment-config.yaml" ]; then
        echo "✅ Configuration de déploiement présente"
    else
        echo "❌ Configuration de déploiement manquante"
        return 1
    fi
}

# Vérifier la production
check_production() {
    echo "Vérification de la production..."
    
    if [ -f "production/configs/production-config.yaml" ] && \
       [ -f "production/security/security-measures.yaml" ]; then
        echo "✅ Configuration de production présente"
    else
        echo "❌ Configuration de production manquante"
        return 1
    fi
}

# Vérifier la surveillance
check_monitoring() {
    echo "Vérification de la surveillance..."
    
    if [ -f "monitoring/services/monitoring-config.yaml" ] && \
       [ -f "monitoring/alerts/alert-rules.yaml" ]; then
        echo "✅ Configuration de surveillance présente"
    else
        echo "❌ Configuration de surveillance manquante"
        return 1
    fi
}

# Vérifier les procédures d'urgence
check_emergency() {
    echo "Vérification des procédures d'urgence..."
    
    if [ -x "production/emergency/incident-response.sh" ]; then
        echo "✅ Procédures d'urgence configurées"
    else
        echo "❌ Procédures d'urgence manquantes"
        return 1
    fi
}

# Exécuter toutes les vérifications
check_deployment
check_production
check_monitoring
check_emergency

echo "✅ Vérification du déploiement et de la production terminée avec succès"

# Pour utiliser ce script :
# 1. ./verify-deployment.sh
# 2. Vérifier les résultats
# 3. Corriger les problèmes détectés

# Cette configuration assure :
# - L'intégrité du déploiement
# - La robustesse de la production
# - L'efficacité de la surveillance
# - La disponibilité des procédures d'urgence 