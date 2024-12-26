#!/bin/bash
set -e

echo "🔑 Configuration de l'authentification..."

# Générer une clé secrète pour JWT
JWT_SECRET=$(openssl rand -base64 32)

# Configuration de l'authentification
cat > auth/config.yaml << EOF
jwt:
  secret: ${JWT_SECRET}
  expiration: 3600  # 1 heure
  refresh_expiration: 604800  # 1 semaine

oauth2:
  providers:
    google:
      client_id: ${GOOGLE_CLIENT_ID}
      client_secret: ${GOOGLE_CLIENT_SECRET}
    github:
      client_id: ${GITHUB_CLIENT_ID}
      client_secret: ${GITHUB_CLIENT_SECRET}

password:
  min_length: 12
  require_uppercase: true
  require_lowercase: true
  require_numbers: true
  require_special: true
  max_attempts: 5
  lockout_duration: 300  # 5 minutes
EOF

echo "✅ Configuration de l'authentification terminée" 