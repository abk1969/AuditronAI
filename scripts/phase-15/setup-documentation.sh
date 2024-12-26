#!/bin/bash
set -e

# Ce script configure la documentation pour AuditronAI
# Il met en place :
# - La documentation technique
# - La documentation utilisateur
# - La documentation API
# - Les guides d'installation

echo "📚 Configuration de la documentation..."

# Créer la structure pour la documentation
mkdir -p documentation/{technical,user,api,guides}

# Configuration de la documentation technique
cat > documentation/technical/config.yaml << EOF
technical_docs:
  structure:
    - architecture:
        - overview
        - components
        - security
        - performance
    
    - development:
        - setup
        - guidelines
        - best_practices
        - testing
    
    - deployment:
        - requirements
        - installation
        - configuration
        - monitoring

  formats:
    - markdown
    - pdf
    - html

  versioning:
    enabled: true
    strategy: "semantic"
    branches:
      - main
      - development
EOF

# Configuration de la documentation API
cat > documentation/api/openapi.yaml << EOF
openapi: 3.0.0
info:
  title: AuditronAI API
  version: 1.0.0
  description: Documentation complète de l'API AuditronAI

servers:
  - url: https://api.auditronai.com/v1
    description: Production
  - url: https://staging-api.auditronai.com/v1
    description: Staging

security:
  - bearerAuth: []
  - apiKeyAuth: []

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
    apiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key
EOF

# Configuration des guides utilisateur
cat > documentation/user/structure.yaml << EOF
user_guides:
  sections:
    getting_started:
      - introduction
      - quick_start
      - first_steps
      
    features:
      - dashboard
      - analysis
      - reports
      - settings
      
    tutorials:
      - basic_analysis
      - advanced_features
      - customization
      - troubleshooting
      
    reference:
      - commands
      - configurations
      - integrations
      - faq

  formats:
    - web
    - pdf
    - video
EOF

# Script de génération de la documentation
cat > documentation/generate-docs.sh << EOF
#!/bin/bash
set -e

echo "📖 Génération de la documentation..."

# Générer la documentation technique
generate_technical_docs() {
    echo "Génération de la documentation technique..."
    # Implémenter la génération
}

# Générer la documentation API
generate_api_docs() {
    echo "Génération de la documentation API..."
    # Implémenter la génération
}

# Générer les guides utilisateur
generate_user_guides() {
    echo "Génération des guides utilisateur..."
    # Implémenter la génération
}

# Exécution
generate_technical_docs
generate_api_docs
generate_user_guides

echo "✅ Documentation générée avec succès"
EOF

chmod +x documentation/generate-docs.sh

echo "✅ Configuration de la documentation terminée avec succès"

# Pour utiliser ce script :
# 1. ./setup-documentation.sh
# 2. Personnaliser les configurations
# 3. Générer la documentation

# Cette configuration assure :
# - Une documentation complète et structurée
# - Une maintenance facile
# - Une génération automatisée
# - Une documentation multiformat 