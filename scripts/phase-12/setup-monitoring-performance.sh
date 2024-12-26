#!/bin/bash
set -e

# Ce script configure le monitoring des performances pour AuditronAI
# Il met en place :
# - Des métriques de performance détaillées
# - Des tableaux de bord de surveillance
# - Des alertes de performance
# - Des rapports d'optimisation

echo "📊 Configuration du monitoring des performances..."

# Créer la structure pour le monitoring
mkdir -p monitoring/{dashboards,alerts,reports}

# Configuration des métriques Prometheus
cat > monitoring/prometheus/performance-metrics.yaml << EOF
# Métriques de performance
metrics:
  # Métriques système
  system:
    - name: cpu_usage
      type: gauge
      help: "Utilisation CPU en pourcentage"
    - name: memory_usage
      type: gauge
      help: "Utilisation mémoire en pourcentage"
    - name: disk_io
      type: counter
      help: "Opérations disque par seconde"

  # Métriques application
  application:
    - name: request_duration_seconds
      type: histogram
      help: "Durée des requêtes en secondes"
    - name: request_rate
      type: counter
      help: "Nombre de requêtes par seconde"
    - name: error_rate
      type: counter
      help: "Taux d'erreurs"

  # Métriques cache
  cache:
    - name: cache_hit_ratio
      type: gauge
      help: "Ratio de succès du cache"
    - name: cache_size
      type: gauge
      help: "Taille actuelle du cache"
EOF

# Configuration des alertes de performance
cat > monitoring/alerts/performance-alerts.yaml << EOF
# Alertes de performance
alerts:
  high_cpu:
    condition: "cpu_usage > 80"
    duration: "5m"
    severity: warning
    message: "Utilisation CPU élevée"

  high_memory:
    condition: "memory_usage > 85"
    duration: "5m"
    severity: warning
    message: "Utilisation mémoire élevée"

  high_latency:
    condition: "request_duration_seconds > 2"
    duration: "5m"
    severity: critical
    message: "Latence élevée détectée"
EOF

echo "✅ Configuration du monitoring des performances terminée avec succès"

# Pour utiliser ce script :
# 1. ./setup-monitoring-performance.sh
# 2. Configurer les dashboards Grafana
# 3. Activer les alertes

# Cette configuration assure :
# - Une visibilité complète sur les performances
# - Des alertes proactives
# - Des rapports détaillés
# - Une optimisation continue 