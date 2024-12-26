#!/bin/bash
set -e

echo "🐍 Configuration de l'environnement Python..."

# Vérifier si nous sommes dans le dossier backend
if [ ! -f "requirements.txt" ]; then
    echo "❌ Erreur: Exécutez ce script depuis le dossier backend"
    exit 1
fi

# Créer l'environnement virtuel
echo "Création de l'environnement virtuel..."
python3 -m venv venv

# Activer l'environnement virtuel
source venv/bin/activate

# Mettre à jour pip
echo "Mise à jour de pip..."
pip install --upgrade pip

# Installer les dépendances
echo "Installation des dépendances..."
pip install -r requirements.txt

# Installer les dépendances de développement
echo "Installation des dépendances de développement..."
pip install -r requirements-dev.txt

# Vérifier les installations
echo "Vérification des installations..."
pip list

echo "✅ Environnement Python configuré avec succès" 