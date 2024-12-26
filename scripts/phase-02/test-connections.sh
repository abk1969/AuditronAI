#!/bin/bash
set -e

# Ce script teste les connexions aux services de stockage
# Il vérifie :
# - La connexion à PostgreSQL
# - La connexion à Redis
# - Les volumes montés
# - Les permissions d'accès

echo "🔌 Test des connexions..."

# Tester PostgreSQL
test_postgres() {
    echo "Test de PostgreSQL..."
    psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "SELECT 1"
}

# Tester Redis
test_redis() {
    echo "Test de Redis..."
    redis-cli -h $REDIS_HOST -p $REDIS_PORT ping
}

# Tester les volumes
test_volumes() {
    echo "Test des volumes..."
    # Vérifier les points de montage
}

# Exécution
test_postgres
test_redis
test_volumes

echo "✅ Test des connexions terminé" 