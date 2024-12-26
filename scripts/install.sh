#!/bin/bash

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Installation des dépendances AuditronAI...${NC}"

# Vérifie si Poetry est installé
if ! command -v poetry &> /dev/null; then
    echo -e "${RED}Poetry n'est pas installé. Installation en cours...${NC}"
    curl -sSL https://install.python-poetry.org | python3 -
fi

# Configure Poetry
echo -e "${YELLOW}Configuration de Poetry...${NC}"
poetry config virtualenvs.in-project true

# Installation des dépendances
echo -e "${YELLOW}Installation des dépendances du projet...${NC}"
poetry install --no-root

# Installation des hooks pre-commit
echo -e "${YELLOW}Installation des hooks pre-commit...${NC}"
poetry run pre-commit install

# Vérifie les vulnérabilités de sécurité
echo -e "${YELLOW}Vérification des vulnérabilités de sécurité...${NC}"
poetry run safety check

echo -e "${GREEN}Installation terminée avec succès !${NC}"
echo -e "${YELLOW}Pour activer l'environnement virtuel, exécutez : ${GREEN}poetry shell${NC}" 