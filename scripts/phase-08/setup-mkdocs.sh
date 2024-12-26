#!/bin/bash
set -e

echo "📘 Configuration de MkDocs..."

# Installer MkDocs et les extensions
pip install mkdocs mkdocs-material mkdocs-awesome-pages-plugin

# Initialiser MkDocs
cat > mkdocs.yml << EOF
site_name: AuditronAI Documentation
site_description: Documentation complète d'AuditronAI
site_author: AuditronAI Team
repo_url: https://github.com/votre-org/auditronai

theme:
  name: material
  language: fr
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - search.suggest
    - search.highlight

plugins:
  - search
  - awesome-pages

nav:
  - Accueil: index.md
  - Installation: guides/installation.md
  - Utilisation: guides/usage.md
  - Déploiement: guides/deployment.md
  - API:
    - Core: api/core/index.md
    - Backend: api/backend/index.md
    - Frontend: api/frontend/index.md
EOF

echo "✅ MkDocs configuré avec succès" 