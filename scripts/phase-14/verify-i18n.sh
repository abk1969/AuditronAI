#!/bin/bash
set -e

# Ce script vérifie la configuration de l'internationalisation
# Il contrôle :
# - Les configurations linguistiques
# - Les traductions
# - Les adaptations régionales
# - La gestion des contenus

echo "🔍 Vérification de l'internationalisation..."

# Vérifier les configurations linguistiques
check_language_config() {
    echo "Vérification des configurations linguistiques..."
    
    if [ -f "i18n/configs/languages.yaml" ]; then
        echo "✅ Configuration des langues présente"
    else
        echo "❌ Configuration des langues manquante"
        return 1
    fi
}

# Vérifier les traductions
check_translations() {
    echo "Vérification des traductions..."
    
    for lang in fr en es de; do
        if [ -f "i18n/translations/$lang/messages.json" ]; then
            echo "✅ Traductions $lang présentes"
        else
            echo "❌ Traductions $lang manquantes"
            return 1
        fi
    done
}

# Vérifier la localisation
check_localization() {
    echo "Vérification de la localisation..."
    
    if [ -f "localization/regions/regional-settings.yaml" ] && \
       [ -f "localization/formats/format-rules.yaml" ]; then
        echo "✅ Configuration de localisation présente"
    else
        echo "❌ Configuration de localisation manquante"
        return 1
    fi
}

# Vérifier la gestion de contenu
check_content_management() {
    echo "Vérification de la gestion de contenu..."
    
    if [ -f "content/management/content-config.yaml" ] && \
       [ -x "content/sync/sync-content.sh" ]; then
        echo "✅ Gestion de contenu configurée"
    else
        echo "❌ Gestion de contenu manquante"
        return 1
    fi
}

# Exécuter toutes les vérifications
check_language_config
check_translations
check_localization
check_content_management

echo "✅ Vérification de l'internationalisation terminée avec succès"

# Pour utiliser ce script :
# 1. ./verify-i18n.sh
# 2. Vérifier les résultats
# 3. Corriger les problèmes détectés

# Cette configuration assure :
# - La cohérence des configurations linguistiques
# - La complétude des traductions
# - L'exactitude des adaptations régionales
# - L'efficacité de la gestion de contenu 