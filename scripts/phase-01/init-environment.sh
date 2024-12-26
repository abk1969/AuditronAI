#!/bin/bash
set -e

# Ce script initialise l'environnement de base pour AuditronAI
# Il met en place :
# - Les variables d'environnement
# - Les dépendances système
# - Les configurations de base
# - Les permissions nécessaires

echo "🚀 Initialisation de l'environnement..."

# Créer la structure de base
mkdir -p {config,data,logs,temp}

# Configuration des variables d'environnement
cat > .env << EOF
# Configuration de l'environnement
APP_ENV=development
APP_PORT=3000
APP_HOST=localhost

# Configuration de la base de données
DB_HOST=localhost
DB_PORT=5432
DB_NAME=auditronai
DB_USER=admin
DB_PASSWORD=secure_password

# Configuration Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Configuration des logs
LOG_LEVEL=debug
LOG_PATH=./logs
EOF

# Installation des dépendances système
install_dependencies() {
    echo "Installation des dépendances..."
    # Liste des dépendances à installer
}

# Configuration des permissions
setup_permissions() {
    echo "Configuration des permissions..."
    chmod 755 config data logs temp
    chmod 600 .env
}

# Exécution
install_dependencies
setup_permissions

echo "✅ Initialisation de l'environnement terminée" 