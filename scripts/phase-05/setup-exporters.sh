#!/bin/bash
set -e

echo "📤 Configuration des exporteurs de métriques..."

# Node Exporter pour les métriques système
docker run -d \
    --name auditronai-node-exporter \
    --net="host" \
    --pid="host" \
    -v "/:/host:ro,rslave" \
    quay.io/prometheus/node-exporter \
    --path.rootfs=/host

# PostgreSQL Exporter
docker run -d \
    --name auditronai-postgres-exporter \
    -p 9187:9187 \
    -e DATA_SOURCE_NAME="postgresql://postgres:postgres@localhost:5432/auditronai?sslmode=disable" \
    wrouesnel/postgres_exporter

# Redis Exporter
docker run -d \
    --name auditronai-redis-exporter \
    -p 9121:9121 \
    oliver006/redis_exporter \
    --redis.addr=redis://localhost:6379

echo "✅ Exporteurs configurés et démarrés" 