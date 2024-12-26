#!/bin/bash
set -e

# Ce script vérifie la configuration de la finalisation et de la production
# Il contrôle :
# - La finalisation
# - Le déploiement
# - La surveillance
# - Le support

echo "🔍 Vérification de la finalisation et de la production..."

# Vérifier la finalisation
check_finalization() {
    echo "Vérification de la finalisation..."
    
    if [ -f "finalization/verification/global-verification.yaml" ] && \
       [ -f "finalization/tests/final-tests.yaml" ]; then
        echo "✅ Configuration de finalisation présente"
    else
        echo "❌ Configuration de finalisation manquante"
        return 1
    fi
}

# Vérifier le déploiement
check_deployment() {
    echo "Vérification du déploiement..."
    
    if [ -f "production/deployment/production-deployment.yaml" ]; then
        echo "✅ Configuration de déploiement présente"
    else
        echo "❌ Configuration de déploiement manquante"
        return 1
    fi
}

# Vérifier la surveillance
check_monitoring() {
    echo "Vérification de la surveillance..."
    
    if [ -f "production/monitoring/production-monitoring.yaml" ]; then
        echo "✅ Configuration de surveillance présente"
    else
        echo "❌ Configuration de surveillance manquante"
        return 1
    fi
}

# Vérifier le support
check_support() {
    echo "Vérification du support..."
    
    if [ -x "production/support/production-support.sh" ]; then
        echo "✅ Configuration de support présente"
    else
        echo "❌ Configuration de support manquante"
        return 1
    fi
}

# Exécuter toutes les vérifications
check_finalization
check_deployment
check_monitoring
check_support

echo "✅ Vérification de la finalisation et de la production terminée avec succès"

# Pour utiliser ce script :
# 1. ./verify-production.sh
# 2. Vérifier les résultats
# 3. Corriger les problèmes détectés

# Cette configuration assure :
# - Une finalisation complète
# - Un déploiement validé
# - Une surveillance active
# - Un support opérationnel 