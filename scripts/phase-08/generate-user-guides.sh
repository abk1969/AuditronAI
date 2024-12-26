#!/bin/bash
set -e

echo "📝 Génération des guides utilisateur..."

# Guide d'installation
cat > docs/guides/installation.md << EOF
# Guide d'Installation

## Prérequis

- Python 3.10+
- Docker
- Kubernetes
- Node.js 16+

## Installation

1. Cloner le dépôt :
   \`\`\`bash
   git clone https://github.com/votre-org/auditronai.git
   cd auditronai
   \`\`\`

2. Installer les dépendances :
   \`\`\`bash
   poetry install
   \`\`\`

3. Configuration :
   \`\`\`bash
   cp .env.example .env
   # Éditer .env avec vos paramètres
   \`\`\`

4. Démarrer l'application :
   \`\`\`bash
   poetry run python -m AuditronAI
   \`\`\`
EOF

# Guide d'utilisation
cat > docs/guides/usage.md << EOF
# Guide d'Utilisation

## Analyse de Code

1. Accéder à l'interface web
2. Soumettre votre code
3. Analyser les résultats

## Configuration

### Paramètres de Sécurité

- Seuils de vulnérabilité
- Règles personnalisées
- Intégrations

### Paramètres d'IA

- Modèles disponibles
- Configuration des prompts
- Optimisation des résultats
EOF

# Guide de déploiement
cat > docs/guides/deployment.md << EOF
# Guide de Déploiement

## Environnement de Production

1. Préparer l'infrastructure
2. Configurer Kubernetes
3. Déployer avec ArgoCD

## Sécurité

- Certificats SSL/TLS
- Vault pour les secrets
- WAF et monitoring

## Maintenance

- Sauvegardes
- Mises à jour
- Monitoring
EOF

echo "✅ Guides utilisateur générés avec succès" 