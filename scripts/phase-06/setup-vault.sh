#!/bin/bash
set -e

echo "🔐 Configuration de HashiCorp Vault..."

# Démarrer Vault en mode développement
docker run -d \
    --name auditronai-vault \
    --cap-add=IPC_LOCK \
    -p 8200:8200 \
    -e 'VAULT_DEV_ROOT_TOKEN_ID=dev-token' \
    -e 'VAULT_DEV_LISTEN_ADDRESS=0.0.0.0:8200' \
    vault:latest

# Attendre que Vault soit prêt
sleep 5

# Configuration initiale de Vault
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='dev-token'

# Activer les secrets engines
vault secrets enable -path=secret kv-v2
vault secrets enable database

# Configurer les politiques de sécurité
cat > policies/app-policy.hcl << EOF
path "secret/data/auditronai/*" {
  capabilities = ["read", "list"]
}

path "database/creds/readonly" {
  capabilities = ["read"]
}
EOF

vault policy write app-policy policies/app-policy.hcl

echo "✅ Vault configuré avec succès" 