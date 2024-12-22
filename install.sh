#!/bin/bash

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Fonction pour afficher les messages
log() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

# Vérification de Docker
check_docker() {
    log "Vérification de Docker..."
    if ! command -v docker &> /dev/null; then
        error "Docker n'est pas installé. Veuillez l'installer : https://docs.docker.com/get-docker/"
    fi
    if ! docker info &> /dev/null; then
        error "Le service Docker n'est pas démarré ou vous n'avez pas les permissions nécessaires"
    fi
    log "Docker est correctement installé et configuré"
}

# Vérification de Docker Compose
check_docker_compose() {
    log "Vérification de Docker Compose..."
    if ! command -v docker compose &> /dev/null; then
        error "Docker Compose n'est pas installé. Veuillez l'installer : https://docs.docker.com/compose/install/"
    fi
    log "Docker Compose est correctement installé"
}

# Vérification des ports
check_ports() {
    log "Vérification des ports requis..."
    if lsof -Pi :8501 -sTCP:LISTEN -t &> /dev/null; then
        error "Le port 8501 est déjà utilisé. Veuillez libérer ce port avant de continuer."
    fi
    if lsof -Pi :5432 -sTCP:LISTEN -t &> /dev/null; then
        error "Le port 5432 est déjà utilisé. Veuillez libérer ce port avant de continuer."
    fi
    log "Les ports requis sont disponibles"
}

# Configuration de l'environnement
setup_environment() {
    log "Configuration de l'environnement..."
    if [ ! -f .env ]; then
        if [ -f .env.example ]; then
            cp .env.example .env
            log "Fichier .env créé à partir de .env.example"
        else
            error "Fichier .env.example non trouvé"
        fi
    else
        warn "Le fichier .env existe déjà"
    fi
}

# Démarrage des services
start_services() {
    log "Démarrage des services..."
    docker compose down &> /dev/null || true
    docker compose pull
    docker compose up -d --build

    # Attente du démarrage des services
    log "Attente du démarrage des services..."
    attempt=1
    max_attempts=30
    while [ $attempt -le $max_attempts ]; do
        if curl -s http://localhost:8501 &> /dev/null; then
            log "Application démarrée avec succès!"
            echo -e "\n${GREEN}Installation terminée avec succès!${NC}"
            echo -e "Accédez à l'application : ${GREEN}http://localhost:8501${NC}"
            echo -e "\nCommandes utiles :"
            echo -e "- Voir les logs : ${YELLOW}docker compose logs -f${NC}"
            echo -e "- Arrêter l'application : ${YELLOW}docker compose down${NC}"
            echo -e "- Redémarrer l'application : ${YELLOW}docker compose restart${NC}"
            return 0
        fi
        echo -n "."
        sleep 2
        attempt=$((attempt + 1))
    done
    error "L'application n'a pas démarré dans le temps imparti"
}

# Fonction principale
main() {
    echo -e "${GREEN}=== Installation automatisée de PromptWizard ===${NC}\n"
    
    # Vérifications
    check_docker
    check_docker_compose
    check_ports
    setup_environment
    
    # Démarrage
    start_services
}

# Exécution du script
main
