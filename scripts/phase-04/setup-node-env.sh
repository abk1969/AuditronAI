#!/bin/bash
set -e

echo "📦 Configuration de l'environnement Node.js..."

# Vérifier si nous sommes dans le dossier frontend
if [ ! -f "package.json" ]; then
    echo "❌ Erreur: Exécutez ce script depuis le dossier frontend"
    exit 1
fi

# Nettoyer l'installation précédente si elle existe
if [ -d "node_modules" ]; then
    echo "Nettoyage de l'installation précédente..."
    rm -rf node_modules
    rm -f package-lock.json
fi

# Installer les dépendances
echo "Installation des dépendances..."
npm install

# Installer les dépendances de développement
echo "Installation des dépendances de développement..."
npm install --save-dev \
    @testing-library/react \
    @testing-library/jest-dom \
    @testing-library/user-event \
    @types/jest \
    @types/node \
    @types/react \
    @types/react-dom \
    @typescript-eslint/eslint-plugin \
    @typescript-eslint/parser \
    eslint \
    eslint-config-prettier \
    eslint-plugin-react \
    prettier \
    typescript

# Vérifier les installations
echo "Vérification des installations..."
npm list --depth=0

echo "✅ Environnement Node.js configuré avec succès" 