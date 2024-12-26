#!/bin/bash
set -e

# Ce script vérifie la configuration de la documentation et de la formation
# Il contrôle :
# - La documentation technique
# - Les supports de formation
# - Les ressources pédagogiques
# - Les évaluations

echo "🔍 Vérification de la documentation et de la formation..."

# Vérifier la documentation
check_documentation() {
    echo "Vérification de la documentation..."
    
    if [ -f "documentation/technical/config.yaml" ] && \
       [ -f "documentation/api/openapi.yaml" ]; then
        echo "✅ Documentation technique configurée"
    else
        echo "❌ Documentation technique manquante"
        return 1
    fi
}

# Vérifier la formation
check_training() {
    echo "Vérification de la formation..."
    
    if [ -f "training/courses/training-paths.yaml" ] && \
       [ -f "training/assessments/assessment-config.yaml" ]; then
        echo "✅ Système de formation configuré"
    else
        echo "❌ Système de formation manquant"
        return 1
    fi
}

# Vérifier les ressources
check_resources() {
    echo "Vérification des ressources..."
    
    if [ -f "resources/materials/materials-config.yaml" ] && \
       [ -f "resources/media/media-config.yaml" ]; then
        echo "✅ Ressources pédagogiques configurées"
    else
        echo "❌ Ressources pédagogiques manquantes"
        return 1
    fi
}

# Vérifier les scripts de génération
check_generation() {
    echo "Vérification des scripts de génération..."
    
    if [ -x "documentation/generate-docs.sh" ] && \
       [ -x "resources/generate-resources.sh" ]; then
        echo "✅ Scripts de génération configurés"
    else
        echo "❌ Scripts de génération manquants"
        return 1
    fi
}

# Exécuter toutes les vérifications
check_documentation
check_training
check_resources
check_generation

echo "✅ Vérification de la documentation et de la formation terminée avec succès"

# Pour utiliser ce script :
# 1. ./verify-documentation.sh
# 2. Vérifier les résultats
# 3. Corriger les problèmes détectés

# Cette configuration assure :
# - L'intégrité de la documentation
# - La qualité de la formation
# - La disponibilité des ressources
# - L'efficacité des outils 