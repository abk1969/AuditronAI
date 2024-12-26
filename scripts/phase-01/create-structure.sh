#!/bin/bash
set -e

# Ce script crée la structure de répertoires pour AuditronAI
# Il met en place :
# - L'arborescence des dossiers
# - Les fichiers de configuration
# - Les répertoires de données
# - Les espaces de logs

echo "📁 Création de la structure..."

# Création des répertoires principaux
mkdir -p {src,config,data,logs,tests,docs}

# Création des sous-répertoires
mkdir -p src/{api,services,models,utils}
mkdir -p config/{env,security,database}
mkdir -p data/{raw,processed,backup}
mkdir -p logs/{app,system,audit}
mkdir -p tests/{unit,integration,e2e}
mkdir -p docs/{api,architecture,deployment}

echo "✅ Structure créée avec succès" 