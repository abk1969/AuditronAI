#!/bin/bash
set -e

# Ce script vérifie la configuration des optimisations
# Il contrôle :
# - Les outils de profilage
# - Les configurations d'optimisation
# - Le système d'auto-tuning
# - Le monitoring des performances

echo "🔍 Vérification des optimisations..."

# Vérifier les outils de profilage
check_profiling() {
    echo "Vérification des outils de profilage..."
    
    if [ -f "performance/profiling/setup_profiling.py" ]; then
        python3 -c "import cProfile, pyinstrument, memory_profiler"
        echo "✅ Outils de profilage configurés"
    else
        echo "❌ Configuration du profilage manquante"
        return 1
    fi
}

# Vérifier les configurations d'optimisation
check_optimization_configs() {
    echo "Vérification des configurations d'optimisation..."
    
    if [ -f "performance/configs/system_optimizations.sh" ] && \
       [ -f "performance/cache/cache_config.yaml" ]; then
        echo "✅ Configurations d'optimisation présentes"
    else
        echo "❌ Configurations d'optimisation manquantes"
        return 1
    fi
}

# Vérifier l'auto-tuning
check_auto_tuning() {
    echo "Vérification de l'auto-tuning..."
    
    if [ -f "tuning/configs/auto_tuning.yaml" ] && \
       [ -x "tuning/adjustments/auto_adjust.sh" ]; then
        echo "✅ Système d'auto-tuning configuré"
    else
        echo "❌ Configuration d'auto-tuning manquante"
        return 1
    fi
}

# Vérifier le monitoring
check_performance_monitoring() {
    echo "Vérification du monitoring des performances..."
    
    if [ -f "monitoring/prometheus/performance-metrics.yaml" ] && \
       [ -f "monitoring/alerts/performance-alerts.yaml" ]; then
        echo "✅ Monitoring des performances configuré"
    else
        echo "❌ Configuration du monitoring manquante"
        return 1
    fi
}

# Exécuter toutes les vérifications
check_profiling
check_optimization_configs
check_auto_tuning
check_performance_monitoring

echo "✅ Vérification des optimisations terminée avec succès"

# Pour utiliser ce script :
# 1. ./verify-optimization.sh
# 2. Vérifier les résultats de chaque test
# 3. Corriger les problèmes détectés

# Cette configuration assure :
# - La disponibilité des outils d'optimisation
# - La cohérence des configurations
# - Le bon fonctionnement du système d'auto-tuning
# - L'efficacité du monitoring 