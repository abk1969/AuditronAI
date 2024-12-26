#!/bin/bash

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Installation d'AuditronAI...${NC}"

# Vérifier Python
echo -e "\n${YELLOW}Vérification de Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 n'est pas installé. Veuillez l'installer d'abord.${NC}"
    exit 1
fi
echo -e "${GREEN}Python 3 trouvé.${NC}"

# Vérifier pip
echo -e "\n${YELLOW}Vérification de pip...${NC}"
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}pip n'est pas installé. Installation...${NC}"
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py
    rm get-pip.py
fi
echo -e "${GREEN}pip trouvé.${NC}"

# Créer un environnement virtuel
echo -e "\n${YELLOW}Création de l'environnement virtuel...${NC}"
python3 -m venv venv
source venv/bin/activate

# Mettre à jour pip
echo -e "\n${YELLOW}Mise à jour de pip...${NC}"
pip install --upgrade pip

# Installer les dépendances Python
echo -e "\n${YELLOW}Installation des dépendances Python...${NC}"
pip install -r requirements.txt

# Vérifier Node.js et npm
echo -e "\n${YELLOW}Vérification de Node.js et npm...${NC}"
if ! command -v node &> /dev/null; then
    echo -e "${RED}Node.js n'est pas installé. Installation via nvm...${NC}"
    
    # Installer nvm
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
    
    # Charger nvm
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    
    # Installer Node.js LTS
    nvm install --lts
    nvm use --lts
fi
echo -e "${GREEN}Node.js trouvé.${NC}"

# Installer les outils TypeScript
echo -e "\n${YELLOW}Installation des outils TypeScript...${NC}"
npm install -g typescript eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin eslint-plugin-security

# Installer les outils d'analyse Python
echo -e "\n${YELLOW}Installation des outils d'analyse Python...${NC}"
pip install bandit prospector radon vulture

# Créer les répertoires nécessaires
echo -e "\n${YELLOW}Création des répertoires...${NC}"
mkdir -p reports
mkdir -p .cache
mkdir -p plugins
mkdir -p logs

# Vérifier PostgreSQL si nécessaire
echo -e "\n${YELLOW}Vérification de PostgreSQL...${NC}"
if ! command -v psql &> /dev/null; then
    echo -e "${YELLOW}PostgreSQL n'est pas installé. Voulez-vous l'installer? (y/n)${NC}"
    read -r install_postgres
    if [[ $install_postgres =~ ^[Yy]$ ]]; then
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            sudo apt-get update
            sudo apt-get install -y postgresql postgresql-contrib
        elif [[ "$OSTYPE" == "darwin"* ]]; then
            brew install postgresql
        else
            echo -e "${YELLOW}Veuillez installer PostgreSQL manuellement pour votre système.${NC}"
        fi
    fi
fi

# Configuration post-installation
echo -e "\n${YELLOW}Configuration post-installation...${NC}"

# Créer le fichier .env s'il n'existe pas
if [ ! -f .env ]; then
    echo -e "\n${YELLOW}Création du fichier .env...${NC}"
    cp .env.example .env
    echo -e "${GREEN}Fichier .env créé. Veuillez le configurer avec vos paramètres.${NC}"
fi

# Vérifier les permissions des répertoires
echo -e "\n${YELLOW}Vérification des permissions...${NC}"
chmod -R 755 .
chmod -R 777 logs
chmod -R 777 .cache
chmod -R 777 reports

# Installation terminée
echo -e "\n${GREEN}Installation terminée avec succès!${NC}"
echo -e "\n${YELLOW}Pour commencer:${NC}"
echo -e "1. Configurez le fichier .env avec vos paramètres"
echo -e "2. Activez l'environnement virtuel: source venv/bin/activate"
echo -e "3. Lancez l'exemple: python examples/analyze_project.py"
echo -e "\n${GREEN}Bonne analyse!${NC}"
