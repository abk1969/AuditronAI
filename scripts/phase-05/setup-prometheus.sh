#!/bin/bash
set -e

echo "📊 Configuration de Prometheus..."

# Créer le dossier de configuration
mkdir -p monitoring/prometheus

# Configuration de base de Prometheus
cat > monitoring/prometheus/prometheus.yml << EOF
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'backend'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'

  - job_name: 'frontend'
    static_configs:
      - targets: ['localhost:3000']
    metrics_path: '/metrics'

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['localhost:9100']

  - job_name: 'postgres-exporter'
    static_configs:
      - targets: ['localhost:9187']

  - job_name: 'redis-exporter'
    static_configs:
      - targets: ['localhost:9121']

# Règles d'alerte
rule_files:
  - 'alert.rules.yml'
EOF

# Configuration des règles d'alerte
cat > monitoring/prometheus/alert.rules.yml << EOF
groups:
  - name: AuditronAI
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: High HTTP error rate
          description: "Error rate is {{ \$value }} for the last 5 minutes"

      - alert: HighResponseTime
        expr: rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m]) > 0.5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: High response time
          description: "Average response time is {{ \$value }}s for the last 5 minutes"
EOF

# Démarrer Prometheus
docker run -d \
    --name auditronai-prometheus \
    -p 9090:9090 \
    -v $(pwd)/monitoring/prometheus:/etc/prometheus \
    prom/prometheus

echo "✅ Prometheus configuré et démarré" 