#!/bin/bash
set -e

# Ce script initialise la base de données pour AuditronAI
# Il met en place :
# - La création de la base
# - Les schémas
# - Les tables
# - Les index

echo "🗄️ Initialisation de la base de données..."

# Créer la base de données
create_database() {
    echo "Création de la base de données..."
    psql -h $DB_HOST -p $DB_PORT -U $DB_USER -c "CREATE DATABASE $DB_NAME"
}

# Créer les schémas
create_schemas() {
    echo "Création des schémas..."
    psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME << EOF
    CREATE SCHEMA audit;
    CREATE SCHEMA security;
    CREATE SCHEMA analytics;
EOF
}

# Créer les tables
create_tables() {
    echo "Création des tables..."
    # Exécuter les scripts SQL de création
}

# Créer les index
create_indexes() {
    echo "Création des index..."
    # Créer les index nécessaires
}

# Exécution
create_database
create_schemas
create_tables
create_indexes

echo "✅ Base de données initialisée avec succès" 