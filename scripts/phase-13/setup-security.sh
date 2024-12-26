#!/bin/bash
set -e

# Ce script configure les mécanismes de sécurité pour AuditronAI
# Il met en place :
# - La gestion des secrets avec Vault
# - Le chiffrement des données
# - Les politiques de sécurité
# - Les contrôles d'accès

echo "🔒 Configuration de la sécurité..."

# Créer la structure pour la sécurité
mkdir -p security/{vault,encryption,policies,access}

# Configuration de Vault
cat > security/vault/config.hcl << EOF
storage "file" {
  path = "/opt/vault/data"
}

listener "tcp" {
  address = "0.0.0.0:8200"
  tls_disable = 0
  tls_cert_file = "/opt/vault/tls/vault.crt"
  tls_key_file = "/opt/vault/tls/vault.key"
}

api_addr = "https://vault.auditronai.com:8200"
ui = true

seal "awskms" {
  region = "eu-west-1"
  kms_key_id = "alias/vault-key"
}
EOF

# Politiques de sécurité
cat > security/policies/security-policies.yaml << EOF
policies:
  password:
    min_length: 12
    require_uppercase: true
    require_lowercase: true
    require_numbers: true
    require_special: true
    max_age_days: 90
    prevent_reuse: 5

  access:
    max_failed_attempts: 5
    lockout_duration: 30m
    session_timeout: 60m
    require_2fa: true

  data:
    encryption_at_rest: true
    encryption_in_transit: true
    key_rotation: 30d
    backup_encryption: true
EOF

# Configuration du chiffrement
cat > security/encryption/encryption-config.yaml << EOF
encryption:
  algorithm: AES-256-GCM
  key_management:
    provider: vault
    rotation_period: 30d
    auto_rotate: true
  
  data_encryption:
    databases: true
    file_systems: true
    backups: true
    
  tls:
    min_version: "1.3"
    preferred_ciphers:
      - TLS_AES_256_GCM_SHA384
      - TLS_CHACHA20_POLY1305_SHA256
EOF

chmod +x security/vault/*.sh

echo "✅ Configuration de la sécurité terminée avec succès"

# Pour utiliser ce script :
# 1. ./setup-security.sh
# 2. Initialiser Vault
# 3. Configurer les politiques de sécurité

# Cette configuration assure :
# - Une gestion sécurisée des secrets
# - Un chiffrement robuste des données
# - Des politiques de sécurité strictes
# - Un contrôle d'accès granulaire 