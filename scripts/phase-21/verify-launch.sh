#!/bin/bash
set -e

# Ce script vérifie la configuration de la validation et du lancement
# Il contrôle :
# - La validation finale
# - La procédure de lancement
# - La communication
# - Le suivi

echo "🔍 Vérification de la validation et du lancement..."

# Vérifier la validation
check_validation() {
    echo "Vérification de la validation..."
    
    if [ -f "validation/system/system-validation.yaml" ] && \
       [ -f "validation/load/load-testing.yaml" ]; then
        echo "✅ Configuration de validation présente"
    else
        echo "❌ Configuration de validation manquante"
        return 1
    fi
}

# Vérifier le lancement
check_launch() {
    echo "Vérification du lancement..."
    
    if [ -f "launch/procedure/launch-procedure.yaml" ]; then
        echo "✅ Configuration de lancement présente"
    else
        echo "❌ Configuration de lancement manquante"
        return 1
    fi
}

# Vérifier la communication
check_communication() {
    echo "Vérification de la communication..."
    
    if [ -f "launch/communication/communication-plan.yaml" ]; then
        echo "✅ Configuration de communication présente"
    else
        echo "❌ Configuration de communication manquante"
        return 1
    fi
}

# Vérifier le suivi
check_monitoring() {
    echo "Vérification du suivi..."
    
    if [ -x "launch/monitoring/post-launch-monitoring.sh" ]; then
        echo "✅ Configuration de suivi présente"
    else
        echo "❌ Configuration de suivi manquante"
        return 1
    fi
}

# Exécuter toutes les vérifications
check_validation
check_launch
check_communication
check_monitoring

echo "✅ Vérification de la validation et du lancement terminée avec succès"

# Pour utiliser ce script :
# 1. ./verify-launch.sh
# 2. Vérifier les résultats
# 3. Corriger les problèmes détectés

# Cette configuration assure :
# - Une validation complète
# - Un lancement maîtrisé
# - Une communication claire
# - Un suivi efficace 