#!/bin/bash
set -e

# Ce script vérifie la configuration de la sécurité avancée et de l'audit
# Il contrôle :
# - Les configurations de sécurité
# - Les mécanismes d'audit
# - La détection des menaces
# - Les rapports de sécurité

echo "🔍 Vérification de la sécurité avancée et de l'audit..."

# Vérifier la sécurité
check_security() {
    echo "Vérification de la sécurité..."
    
    if [ -f "security/hardening/security-hardening.yaml" ] && \
       [ -f "security/threats/threat-detection.yaml" ]; then
        echo "✅ Configuration de sécurité présente"
    else
        echo "❌ Configuration de sécurité manquante"
        return 1
    fi
}

# Vérifier l'audit
check_audit() {
    echo "Vérification de l'audit..."
    
    if [ -f "audit/system/system-audit.yaml" ] && \
       [ -f "audit/application/application-audit.yaml" ]; then
        echo "✅ Configuration d'audit présente"
    else
        echo "❌ Configuration d'audit manquante"
        return 1
    fi
}

# Vérifier la prévention
check_prevention() {
    echo "Vérification de la prévention..."
    
    if [ -x "security/prevention/intrusion-prevention.sh" ]; then
        echo "✅ Scripts de prévention présents"
    else
        echo "❌ Scripts de prévention manquants"
        return 1
    fi
}

# Vérifier les rapports
check_reports() {
    echo "Vérification des rapports..."
    
    if [ -x "audit/reports/generate-audit-report.sh" ]; then
        echo "✅ Scripts de rapport présents"
    else
        echo "❌ Scripts de rapport manquants"
        return 1
    fi
}

# Exécuter toutes les vérifications
check_security
check_audit
check_prevention
check_reports

echo "✅ Vérification de la sécurité et de l'audit terminée avec succès"

# Pour utiliser ce script :
# 1. ./verify-security.sh
# 2. Vérifier les résultats
# 3. Corriger les problèmes détectés

# Cette configuration assure :
# - L'intégrité de la sécurité
# - La complétude de l'audit
# - L'efficacité de la prévention
# - La qualité des rapports 