#!/bin/bash
set -e

# Fonction pour attendre que PostgreSQL soit prêt
wait_for_postgres() {
    echo "Attente de PostgreSQL..."
    while ! pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER
    do
        sleep 1
    done
    echo "PostgreSQL est prêt !"
}

# Fonction pour initialiser l'application
init_app() {
    echo "Initialisation de l'application..."

    # Créer les répertoires nécessaires
    mkdir -p /app/reports
    mkdir -p /app/logs
    mkdir -p /app/.cache
    mkdir -p /app/plugins

    # Définir les permissions
    chmod -R 755 /app
    chmod -R 777 /app/logs
    chmod -R 777 /app/.cache
    chmod -R 777 /app/reports

    # Copier les fichiers de configuration si nécessaire
    if [ ! -f /app/configs/analyzer_config.yaml ]; then
        cp /app/configs/analyzer_config.example.yaml /app/configs/analyzer_config.yaml
    fi

    # Installer les dépendances Node.js si nécessaire
    if [ ! -d "/app/node_modules" ]; then
        echo "Installation des dépendances Node.js..."
        npm install
    fi

    # Vérifier les outils d'analyse
    echo "Vérification des outils d'analyse..."
    tools=("bandit" "prospector" "radon" "vulture" "typescript" "eslint")
    for tool in "${tools[@]}"
    do
        if ! command -v $tool &> /dev/null; then
            echo "Installation de $tool..."
            if [[ "$tool" == "typescript" || "$tool" == "eslint" ]]; then
                npm install -g $tool
            else
                pip install $tool
            fi
        fi
    done
}

# Fonction principale
main() {
    # Attendre que PostgreSQL soit prêt
    wait_for_postgres

    # Initialiser l'application
    init_app

    # Exécuter les migrations si nécessaire
    if [ -f "/app/migrations/migrate.py" ]; then
        echo "Exécution des migrations..."
        python /app/migrations/migrate.py
    fi

    # Démarrer l'application
    echo "Démarrage de l'application..."
    exec "$@"
}

# Exécuter la fonction principale avec les arguments passés
main "$@"
