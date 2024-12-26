#!/bin/bash
set -e

echo "🔍 Vérification de l'environnement de production..."

# Vérifier les déploiements
check_deployments() {
    echo "Vérification des déploiements..."
    
    DEPLOYMENTS=(
        "auditronai-backend"
        "auditronai-frontend"
        "prometheus"
        "grafana"
    )
    
    for deployment in "${DEPLOYMENTS[@]}"; do
        if kubectl get deployment $deployment -o jsonpath='{.status.readyReplicas}' > /dev/null; then
            echo "✅ Déploiement $deployment opérationnel"
        else
            echo "❌ Déploiement $deployment non disponible"
            return 1
        fi
    done
}

# Vérifier le monitoring
check_monitoring() {
    echo "Vérification du monitoring..."
    
    if curl -s http://prometheus:9090/-/healthy | grep -q "Prometheus"; then
        echo "✅ Prometheus opérationnel"
    else
        echo "❌ Prometheus non disponible"
        return 1
    fi
    
    if curl -s http://grafana:3000/api/health | grep -q "ok"; then
        echo "✅ Grafana opérationnel"
    else
        echo "❌ Grafana non disponible"
        return 1
    fi
}

# Vérifier les sauvegardes
check_backups() {
    echo "Vérification des sauvegardes..."
    
    if velero get backup | grep -q "Completed"; then
        echo "✅ Système de sauvegarde opérationnel"
    else
        echo "❌ Problème avec les sauvegardes"
        return 1
    fi
}

# Vérifier les métriques
check_metrics() {
    echo "Vérification des métriques..."
    
    # Vérifier le taux d'erreur
    ERROR_RATE=$(curl -s http://prometheus:9090/api/v1/query?query=sum(rate(http_requests_total{status=~"5.."}[5m]))/sum(rate(http_requests_total[5m])))
    if (( $(echo "$ERROR_RATE < 0.05" | bc -l) )); then
        echo "✅ Taux d'erreur acceptable"
    else
        echo "❌ Taux d'erreur trop élevé"
        return 1
    fi
    
    # Vérifier la latence
    LATENCY=$(curl -s http://prometheus:9090/api/v1/query?query=histogram_quantile(0.95,sum(rate(http_request_duration_seconds_bucket[5m]))by(le)))
    if (( $(echo "$LATENCY < 2" | bc -l) )); then
        echo "✅ Latence acceptable"
    else
        echo "❌ Latence trop élevée"
        return 1
    fi
}

# Exécuter toutes les vérifications
check_deployments
check_monitoring
check_backups
check_metrics

echo "✅ Vérification de l'environnement de production terminée avec succès" 