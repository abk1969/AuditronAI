#!/bin/bash
set -e

echo "🔍 Vérification de la sécurité..."

# Vérifier les certificats SSL
check_ssl() {
    echo "Vérification des certificats SSL..."
    if [ -f "ssl/certs/backend.crt" ] && [ -f "ssl/certs/backend.key" ]; then
        openssl x509 -in ssl/certs/backend.crt -text -noout > /dev/null
        echo "✅ Certificats SSL valides"
    else
        echo "❌ Certificats SSL manquants ou invalides"
        return 1
    fi
}

# Vérifier Vault
check_vault() {
    echo "Vérification de Vault..."
    if curl -s http://127.0.0.1:8200/v1/sys/health | grep -q "initialized"; then
        echo "✅ Vault opérationnel"
    else
        echo "❌ Vault non disponible"
        return 1
    fi
}

# Vérifier le WAF
check_waf() {
    echo "Vérification du WAF..."
    if docker ps | grep -q "auditronai-waf"; then
        # Test d'une attaque XSS basique
        if curl -s -o /dev/null -w "%{http_code}" "http://localhost:8080/?test=<script>alert(1)</script>" | grep -q "403"; then
            echo "✅ WAF bloque correctement les attaques XSS"
        else
            echo "❌ WAF ne bloque pas les attaques XSS"
            return 1
        fi
    else
        echo "❌ WAF non démarré"
        return 1
    fi
}

# Exécuter toutes les vérifications
check_ssl
check_vault
check_waf

echo "✅ Vérification de la sécurité terminée avec succès" 