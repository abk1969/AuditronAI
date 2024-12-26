#!/bin/bash
set -e

# Ce script vérifie la configuration de la maintenance et de l'évolution
# Il contrôle :
# - Les procédures de maintenance
# - Les processus d'évolution
# - Le système de retours
# - Les analyses d'impact

echo "🔍 Vérification de la maintenance et de l'évolution..."

# Vérifier la maintenance
check_maintenance() {
    echo "Vérification de la maintenance..."
    
    if [ -f "maintenance/procedures/maintenance-procedures.yaml" ] && \
       [ -f "maintenance/backups/backup-config.yaml" ]; then
        echo "✅ Configuration de maintenance présente"
    else
        echo "❌ Configuration de maintenance manquante"
        return 1
    fi
}

# Vérifier l'évolution
check_evolution() {
    echo "Vérification de l'évolution..."
    
    if [ -f "evolution/versions/version-management.yaml" ] && \
       [ -f "evolution/improvements/improvement-tracking.yaml" ]; then
        echo "✅ Configuration d'évolution présente"
    else
        echo "❌ Configuration d'évolution manquante"
        return 1
    fi
}

# Vérifier les retours
check_feedback() {
    echo "Vérification des retours..."
    
    if [ -f "feedback/collection/feedback-collection.yaml" ] && \
       [ -f "feedback/analysis/feedback-analysis.yaml" ]; then
        echo "✅ Système de retours configuré"
    else
        echo "❌ Système de retours manquant"
        return 1
    fi
}

# Vérifier les analyses
check_analysis() {
    echo "Vérification des analyses..."
    
    if [ -x "evolution/analysis/impact-analysis.sh" ] && \
       [ -x "feedback/tracking/track-improvements.sh" ]; then
        echo "✅ Outils d'analyse configurés"
    else
        echo "❌ Outils d'analyse manquants"
        return 1
    fi
}

# Exécuter toutes les vérifications
check_maintenance
check_evolution
check_feedback
check_analysis

echo "✅ Vérification de la maintenance et de l'évolution terminée avec succès"

# Pour utiliser ce script :
# 1. ./verify-maintenance.sh
# 2. Vérifier les résultats
# 3. Corriger les problèmes détectés

# Cette configuration assure :
# - L'intégrité de la maintenance
# - La cohérence de l'évolution
# - L'efficacité des retours
# - La pertinence des analyses 