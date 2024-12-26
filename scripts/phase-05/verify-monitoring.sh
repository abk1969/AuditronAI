#!/bin/bash
set -e

echo "🔍 Vérification du monitoring..."

# Vérifier les conteneurs
check_containers() {
    echo "Vérification des conteneurs de monitoring..."
    local containers=(
        "auditronai-prometheus"
        "auditronai-grafana"
        "auditronai-node-exporter"
        "auditronai-postgres-exporter"
        "auditronai-redis-exporter"
    )
    
    for container in "${containers[@]}"; do
        if docker ps | grep -q $container; then
            echo "✅ Conteneur $container est en cours d'exécution"
        else
            echo "❌ Conteneur $container n'est pas en cours d'exécution"
            return 1
        fi
    done
}

# Vérifier les endpoints
check_endpoints() {
    echo "Vérification des endpoints de monitoring..."
    local endpoints=(
        "http://localhost:9090/-/healthy"  # Prometheus
        "http://localhost:3001/api/health" # Grafana
        "http://localhost:9100/metrics"    # Node Exporter
        "http://localhost:9187/metrics"    # Postgres Exporter
        "http://localhost:9121/metrics"    # Redis Exporter
    )
    
    for endpoint in "${endpoints[@]}"; do
        if curl -s -f $endpoint > /dev/null; then
            echo "✅ Endpoint $endpoint est accessible"
        else
            echo "❌ Endpoint $endpoint n'est pas accessible"
            return 1
        fi
    done
}

# Vérifier les métriques
check_metrics() {
    echo "Vérification des métriques..."
    
    # Vérifier les métriques Prometheus
    if curl -s http://localhost:9090/api/v1/query?query=up | grep -q '"result":\['; then
        echo "✅ Métriques Prometheus OK"
    else
        echo "❌ Problème avec les métriques Prometheus"
        return 1
    fi
    
    # Vérifier la connexion Grafana-Prometheus
    if curl -s -u admin:admin http://localhost:3001/api/datasources/proxy/1/api/v1/query?query=up; then
        echo "✅ Connexion Grafana-Prometheus OK"
    else
        echo "❌ Problème de connexion Grafana-Prometheus"
        return 1
    fi
}

# Exécuter toutes les vérifications
check_containers
check_endpoints
check_metrics

echo "✅ Vérification du monitoring terminée avec succès" 