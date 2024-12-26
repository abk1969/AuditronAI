#!/bin/bash
set -e

echo "📈 Configuration de Grafana..."

# Créer le dossier de configuration
mkdir -p monitoring/grafana/{dashboards,provisioning}

# Configuration des sources de données
cat > monitoring/grafana/provisioning/datasources/prometheus.yml << EOF
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
EOF

# Dashboard pour les métriques système
cat > monitoring/grafana/dashboards/system.json << EOF
{
  "dashboard": {
    "id": null,
    "title": "System Metrics",
    "tags": ["auditronai"],
    "timezone": "browser",
    "panels": [
      {
        "title": "CPU Usage",
        "type": "graph",
        "datasource": "Prometheus",
        "targets": [
          {
            "expr": "rate(process_cpu_seconds_total[5m])",
            "legendFormat": "CPU Usage"
          }
        ]
      },
      {
        "title": "Memory Usage",
        "type": "graph",
        "datasource": "Prometheus",
        "targets": [
          {
            "expr": "process_resident_memory_bytes",
            "legendFormat": "Memory Usage"
          }
        ]
      }
    ]
  }
}
EOF

# Dashboard pour les métriques d'application
cat > monitoring/grafana/dashboards/application.json << EOF
{
  "dashboard": {
    "id": null,
    "title": "Application Metrics",
    "tags": ["auditronai"],
    "timezone": "browser",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "datasource": "Prometheus",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{path}}"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph",
        "datasource": "Prometheus",
        "targets": [
          {
            "expr": "rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])",
            "legendFormat": "{{method}} {{path}}"
          }
        ]
      }
    ]
  }
}
EOF

# Démarrer Grafana
docker run -d \
    --name auditronai-grafana \
    -p 3001:3000 \
    -v $(pwd)/monitoring/grafana:/var/lib/grafana \
    grafana/grafana

echo "✅ Grafana configuré et démarré" 