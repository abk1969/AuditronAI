#!/bin/bash
set -e

echo "🔍 Vérification de la Phase 2..."

# Vérifier les conteneurs
check_containers() {
    echo "Vérification des conteneurs..."
    local containers=("auditronai-postgres" "auditronai-redis")
    
    for container in "${containers[@]}"; do
        if docker ps | grep -q $container; then
            echo "✅ Conteneur $container est en cours d'exécution"
        else
            echo "❌ Conteneur $container n'est pas en cours d'exécution"
            return 1
        fi
    done
}

# Vérifier les volumes
check_volumes() {
    echo "Vérification des volumes..."
    local volumes=("auditronai_postgres_data" "auditronai_redis_data")
    
    for volume in "${volumes[@]}"; do
        if docker volume inspect $volume >/dev/null 2>&1; then
            echo "✅ Volume $volume existe"
        else
            echo "❌ Volume $volume n'existe pas"
            return 1
        fi
    done
}

# Vérifier les services
check_services() {
    echo "Vérification des services..."
    
    # PostgreSQL
    if PGPASSWORD=postgres psql -h localhost -U postgres -d auditronai -c '\conninfo' >/dev/null 2>&1; then
        echo "✅ Service PostgreSQL est fonctionnel"
    else
        echo "❌ Service PostgreSQL n'est pas fonctionnel"
        return 1
    fi
    
    # Redis
    if redis-cli ping >/dev/null 2>&1; then
        echo "✅ Service Redis est fonctionnel"
    else
        echo "❌ Service Redis n'est pas fonctionnel"
        return 1
    fi
}

# Exécuter toutes les vérifications
check_containers
check_volumes
check_services

echo "✅ Phase 2 vérifiée avec succès" 