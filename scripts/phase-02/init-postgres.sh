#!/bin/bash
set -e

echo "🐘 Initialisation de PostgreSQL..."

# Vérifier si le volume existe déjà
if docker volume inspect auditronai_postgres_data >/dev/null 2>&1; then
    echo "Le volume PostgreSQL existe déjà"
else
    echo "Création du volume PostgreSQL..."
    docker volume create auditronai_postgres_data
fi

# Créer le conteneur PostgreSQL
docker run -d \
    --name auditronai-postgres \
    -e POSTGRES_DB=auditronai \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=postgres \
    -v auditronai_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    postgres:13

# Attendre que PostgreSQL soit prêt
echo "Attente du démarrage de PostgreSQL..."
until PGPASSWORD=postgres psql -h localhost -U postgres -d postgres -c '\q' 2>/dev/null; do
    echo "PostgreSQL n'est pas encore prêt - attente..."
    sleep 1
done

echo "✅ PostgreSQL est initialisé et prêt" 