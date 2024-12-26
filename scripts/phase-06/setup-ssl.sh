#!/bin/bash
set -e

echo "🔒 Configuration SSL/TLS..."

# Créer le dossier pour les certificats
mkdir -p ssl/certs
cd ssl

# Générer une autorité de certification privée
openssl genrsa -out certs/ca.key 4096
openssl req -x509 -new -nodes -key certs/ca.key -sha256 -days 1024 -out certs/ca.crt \
    -subj "/C=FR/ST=IDF/L=Paris/O=AuditronAI/CN=AuditronAI CA"

# Générer le certificat pour le backend
openssl genrsa -out certs/backend.key 2048
openssl req -new -key certs/backend.key -out certs/backend.csr \
    -subj "/C=FR/ST=IDF/L=Paris/O=AuditronAI/CN=api.auditronai.local"

# Signer le certificat
openssl x509 -req -in certs/backend.csr \
    -CA certs/ca.crt -CAkey certs/ca.key -CAcreateserial \
    -out certs/backend.crt -days 365 -sha256

echo "✅ Certificats SSL générés avec succès" 