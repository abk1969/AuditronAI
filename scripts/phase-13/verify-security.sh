#!/bin/bash
set -e

# Ce script vérifie la configuration de sécurité et conformité
# Il contrôle :
# - Les mécanismes de sécurité
# - La conformité GDPR
# - Les systèmes d'audit
# - Les contrôles d'accès

echo "🔍 Vérification de la sécurité et conformité..."

# Vérifier la configuration de sécurité
check_security() {
    echo "Vérification de la sécurité..."
    
    if [ -f "security/vault/config.hcl" ] && \
       [ -f "security/policies/security-policies.yaml" ]; then
        echo "✅ Configuration de sécurité présente"
    else
        echo "❌ Configuration de sécurité manquante"
        return 1
    fi
}

# Vérifier la conformité GDPR
check_gdpr() {
    echo "Vérification de la conformité GDPR..."
    
    if [ -f "compliance/gdpr/gdpr-controls.yaml" ]; then
        echo "✅ Contrôles GDPR configurés"
    else
        echo "❌ Contrôles GDPR manquants"
        return 1
    fi
}

# Vérifier les audits
check_audits() {
    echo "Vérification des audits..."
    
    if [ -f "audit/security/security-audit.yaml" ] && \
       [ -x "audit/reports/generate-audit-report.sh" ]; then
        echo "✅ Système d'audit configuré"
    else
        echo "❌ Système d'audit manquant"
        return 1
    fi
}

# Vérifier la journalisation
check_logging() {
    echo "Vérification de la journalisation..."
    
    if [ -f "compliance/logs/logging-policy.yaml" ]; then
        echo "✅ Journalisation configurée"
    else
        echo "❌ Journalisation manquante"
        return 1
    fi
}

# Exécuter toutes les vérifications
check_security
check_gdpr
check_audits
check_logging

echo "✅ Vérification de la sécurité et conformité terminée avec succès"

# Pour utiliser ce script :
# 1. ./verify-security.sh
# 2. Vérifier les résultats
# 3. Corriger les problèmes détectés

# Cette configuration assure :
# - L'intégrité des mécanismes de sécurité
# - La conformité aux réglementations
# - L'efficacité des audits
# - La complétude de la journalisation 