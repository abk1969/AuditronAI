#!/bin/bash

# Couleurs pour les logs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Fonction de logging
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Vérification des prérequis
check_command() {
    if ! command -v $1 &> /dev/null; then
        log_error "$1 n'est pas installé"
        return 1
    fi
    log_info "$1 est disponible"
    return 0
}

# Vérification de l'environnement
check_environment() {
    if [ -z "$1" ]; then
        log_error "Variable d'environnement $1 non définie"
        return 1
    fi
    return 0
}

# Gestion des erreurs
handle_error() {
    log_error "$1"
    exit 1
}

# Vérification de la connexion à la base de données
check_db_connection() {
    local host=$1
    local port=$2
    local db=$3
    local user=$4

    if pg_isready -h $host -p $port -d $db -U $user > /dev/null 2>&1; then
        log_info "Connexion à la base de données réussie"
        return 0
    else
        log_error "Impossible de se connecter à la base de données"
        return 1
    fi
}

# Vérification des services
check_service() {
    local service=$1
    if systemctl is-active --quiet $service; then
        log_info "Service $service est actif"
        return 0
    else
        log_error "Service $service n'est pas actif"
        return 1
    fi
}

# Sauvegarde de sécurité
backup_file() {
    local file=$1
    if [ -f "$file" ]; then
        cp "$file" "${file}.bak"
        log_info "Sauvegarde créée: ${file}.bak"
        return 0
    else
        log_error "Fichier $file n'existe pas"
        return 1
    fi
}

# Vérification de l'espace disque
check_disk_space() {
    local min_space=$1  # en GB
    local available=$(df -BG / | awk 'NR==2 {print $4}' | sed 's/G//')
    if [ $available -lt $min_space ]; then
        log_warning "Espace disque faible: ${available}G disponible"
        return 1
    fi
    log_info "Espace disque suffisant: ${available}G disponible"
    return 0
}

# Nettoyage des fichiers temporaires
cleanup_temp_files() {
    local dir=$1
    find "$dir" -type f -name "*.tmp" -delete
    find "$dir" -type f -name "*.bak" -mtime +7 -delete
    log_info "Nettoyage des fichiers temporaires terminé"
}

# Vérification des permissions
check_permissions() {
    local path=$1
    local required_perm=$2
    local current_perm=$(stat -c %a "$path")
    if [ "$current_perm" != "$required_perm" ]; then
        log_error "Permissions incorrectes pour $path: $current_perm (requis: $required_perm)"
        return 1
    fi
    return 0
} 