#!/bin/bash
set -e

# Ce script vérifie la configuration de maintenance
# Il contrôle :
# - Les scripts de maintenance
# - Les mises à jour automatiques
# - Le système de monitoring
# - Les procédures de rollback

echo "🔍 Vérification de la configuration de maintenance..."

# Vérifier les scripts de maintenance
check_maintenance_scripts() {
    echo "Vérification des scripts de maintenance..."
    
    REQUIRED_SCRIPTS=(
        "maintenance/scripts/update-dependencies.sh"
        "maintenance/scripts/cleanup.sh"
        "updates/scripts/security-updates.sh"
        "updates/scripts/component-updates.sh"
    )
    
    for script in "${REQUIRED_SCRIPTS[@]}"; do
        if [ -x "$script" ]; then
            echo "✅ Script $script présent et exécutable"
        else
            echo "❌ Script $script manquant ou non exécutable"
            return 1
        fi
    done
}

# Vérifier la configuration des alertes
check_alerts() {
    echo "Vérification des alertes..."
    
    if [ -f "monitoring/alerts/maintenance-alerts.yaml" ]; then
        echo "✅ Configuration des alertes présente"
    else
        echo "❌ Configuration des alertes manquante"
        return 1
    fi
}

# Vérifier les procédures de rollback
check_rollback() {
    echo "Vérification des procédures de rollback..."
    
    if [ -d "updates/rollback" ]; then
        echo "✅ Système de rollback configuré"
    else
        echo "❌ Système de rollback manquant"
        return 1
    fi
}

# Vérifier les rapports
check_reports() {
    echo "Vérification des rapports..."
    
    if [ -x "monitoring/reports/generate-report.sh" ]; then
        echo "✅ Système de rapports configuré"
    else
        echo "❌ Système de rapports manquant"
        return 1
    fi
}

# Exécuter toutes les vérifications
check_maintenance_scripts
check_alerts
check_rollback
check_reports

echo "✅ Vérification de la maintenance terminée avec succès"

# Pour utiliser ce script :
# 1. ./verify-maintenance.sh
# 2. Vérifier les résultats de chaque test
# 3. Corriger les problèmes détectés si nécessaire

# Cette configuration assure :
# - L'intégrité du système de maintenance
# - La disponibilité des outils nécessaires
# - La cohérence des configurations 