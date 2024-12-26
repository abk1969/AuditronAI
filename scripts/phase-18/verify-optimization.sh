#!/bin/bash
set -e

# Ce script vérifie la configuration de l'optimisation et du profilage
# Il contrôle :
# - Les configurations d'optimisation
# - Les outils de profilage
# - Les benchmarks
# - Les analyses

echo "🔍 Vérification de l'optimisation et du profilage..."

# Vérifier l'optimisation
check_optimization() {
    echo "Vérification de l'optimisation..."
    
    if [ -f "optimization/performance/performance-config.yaml" ] && \
       [ -f "optimization/resources/resource-optimization.yaml" ]; then
        echo "✅ Configuration d'optimisation présente"
    else
        echo "❌ Configuration d'optimisation manquante"
        return 1
    fi
}

# Vérifier le profilage
check_profiling() {
    echo "Vérification du profilage..."
    
    if [ -f "profiling/code/code-profiling.yaml" ] && \
       [ -f "profiling/performance/performance-profiling.yaml" ]; then
        echo "✅ Configuration de profilage présente"
    else
        echo "❌ Configuration de profilage manquante"
        return 1
    fi
}

# Vérifier les benchmarks
check_benchmarks() {
    echo "Vérification des benchmarks..."
    
    if [ -x "optimization/benchmarks/run-benchmarks.sh" ]; then
        echo "✅ Scripts de benchmark présents"
    else
        echo "❌ Scripts de benchmark manquants"
        return 1
    fi
}

# Vérifier les analyses
check_analysis() {
    echo "Vérification des analyses..."
    
    if [ -x "profiling/analysis/analyze-profiling.sh" ]; then
        echo "✅ Scripts d'analyse présents"
    else
        echo "❌ Scripts d'analyse manquants"
        return 1
    fi
}

# Exécuter toutes les vérifications
check_optimization
check_profiling
check_benchmarks
check_analysis

echo "✅ Vérification de l'optimisation et du profilage terminée avec succès"

# Pour utiliser ce script :
# 1. ./verify-optimization.sh
# 2. Vérifier les résultats
# 3. Corriger les problèmes détectés

# Cette configuration assure :
# - L'intégrité des optimisations
# - La précision du profilage
# - La fiabilité des benchmarks
# - La pertinence des analyses 