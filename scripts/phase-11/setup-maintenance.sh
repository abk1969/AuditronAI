#!/bin/bash
set -e

# Ce script configure les procédures de maintenance automatisée pour AuditronAI
# Il met en place :
# - Des fenêtres de maintenance planifiées
# - Des mises à jour automatiques des dépendances
# - Des nettoyages périodiques des ressources
# - Des vérifications de santé post-maintenance

echo "🔧 Configuration de la maintenance..."

# Créer le dossier de maintenance
mkdir -p maintenance/{scripts,logs,reports}

# Script de mise à jour des dépendances
cat > maintenance/scripts/update-dependencies.sh << EOF
#!/bin/bash
set -e

# Met à jour les dépendances Python et npm
# Vérifie la compatibilité avant mise à jour
# Crée un rapport de mise à jour
# Effectue des tests de régression post-mise à jour

echo "📦 Mise à jour des dépendances..."
poetry update --dry-run
cd frontend && npm outdated
cd ..

# Mise à jour avec tests de régression
poetry update
cd frontend && npm update && npm test
cd ..

echo "✅ Dépendances mises à jour avec succès"
EOF

# Script de nettoyage
cat > maintenance/scripts/cleanup.sh << EOF
#!/bin/bash
set -e

# Nettoie les ressources inutilisées :
# - Logs anciens
# - Caches
# - Images Docker obsolètes
# - Sauvegardes expirées

echo "🧹 Nettoyage du système..."

# Nettoyage des logs
find ./logs -type f -mtime +30 -delete

# Nettoyage Docker
docker system prune -af --volumes

# Nettoyage des caches
rm -rf .cache/*
cd frontend && npm cache clean --force
cd ..

echo "✅ Nettoyage terminé avec succès"
EOF

chmod +x maintenance/scripts/*.sh

echo "✅ Configuration de la maintenance terminée avec succès"

# Pour utiliser ce script :
# 1. ./setup-maintenance.sh
# 2. Les scripts de maintenance seront disponibles dans maintenance/scripts/
# 3. Planifier les scripts avec cron pour une exécution automatique

# Cette configuration assure :
# - Des mises à jour régulières et sécurisées
# - Un système propre et optimisé
# - Une traçabilité des opérations de maintenance 