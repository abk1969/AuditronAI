#!/bin/bash

echo "🚀 Démarrage d'AuditronAI..."

# Fonction pour vérifier si une commande existe
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo "❌ $1 n'est pas installé"
        return 1
    else
        echo "✅ $1 est installé"
        return 0
    fi
}

# Détection du système d'exploitation
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    IS_WINDOWS=true
else
    IS_WINDOWS=false
fi

# Vérification de Python
check_command python3 || check_command python || {
    echo "Veuillez installer Python 3.9 ou supérieur"
    exit 1
}

# Vérification de Poetry
check_command poetry || {
    echo "Installation de Poetry..."
    if [ "$IS_WINDOWS" = true ]; then
        (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
    else
        curl -sSL https://install.python-poetry.org | python3 -
    fi
}

# Vérification de wkhtmltopdf pour l'export PDF
check_command wkhtmltopdf || {
    echo "Installation de wkhtmltopdf..."
    if [ "$IS_WINDOWS" = true ]; then
        echo "❌ Veuillez installer wkhtmltopdf manuellement : https://wkhtmltopdf.org/downloads.html"
        echo "Après l'installation, ajoutez le chemin à votre PATH système"
        exit 1
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get update && sudo apt-get install -y wkhtmltopdf
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install wkhtmltopdf
    else
        echo "❌ Veuillez installer wkhtmltopdf manuellement : https://wkhtmltopdf.org/downloads.html"
        exit 1
    fi
}

# Vérification de Redis
check_command redis-cli || {
    echo "Installation de Redis..."
    if [ "$IS_WINDOWS" = true ]; then
        echo "❌ Veuillez installer Redis pour Windows : https://github.com/microsoftarchive/redis/releases"
        echo "Après l'installation, ajoutez le chemin à votre PATH système"
        exit 1
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get update && sudo apt-get install -y redis-server
        sudo systemctl start redis-server
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install redis
        brew services start redis
    else
        echo "❌ Veuillez installer Redis manuellement : https://redis.io/download"
        exit 1
    fi
}

# Vérification de RabbitMQ
check_command rabbitmqctl || {
    echo "Installation de RabbitMQ..."
    if [ "$IS_WINDOWS" = true ]; then
        echo "❌ Veuillez installer RabbitMQ pour Windows : https://www.rabbitmq.com/install-windows.html"
        echo "Après l'installation, ajoutez le chemin à votre PATH système"
        exit 1
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get update && sudo apt-get install -y rabbitmq-server
        sudo systemctl start rabbitmq-server
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install rabbitmq
        brew services start rabbitmq
    else
        echo "❌ Veuillez installer RabbitMQ manuellement : https://www.rabbitmq.com/download.html"
        exit 1
    fi
}

# Vérification de Elasticsearch
check_command elasticsearch || {
    echo "Installation de Elasticsearch..."
    if [ "$IS_WINDOWS" = true ]; then
        echo "❌ Veuillez installer Elasticsearch pour Windows : https://www.elastic.co/downloads/elasticsearch"
        echo "Après l'installation, ajoutez le chemin à votre PATH système"
        exit 1
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
        echo "deb https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
        sudo apt-get update && sudo apt-get install -y elasticsearch
        sudo systemctl start elasticsearch
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew tap elastic/tap
        brew install elastic/tap/elasticsearch
        brew services start elasticsearch
    else
        echo "❌ Veuillez installer Elasticsearch manuellement : https://www.elastic.co/downloads/elasticsearch"
        exit 1
    fi
}

# Vérification du fichier .env
if [ ! -f .env ]; then
    echo "Création du fichier .env à partir de .env.example..."
    cp .env.example .env
    echo "⚠️ Veuillez configurer les variables dans le fichier .env"
fi

# Installation des dépendances Python
echo "Installation des dépendances Python..."
poetry install

# Vérification des services
echo "Vérification des services..."
if [ "$IS_WINDOWS" = true ]; then
    # Vérification des services Windows
    services=("Redis" "RabbitMQ" "elasticsearch-service-x64")
    for service in "${services[@]}"; do
        if sc query "$service" | grep -q "RUNNING"; then
            echo "✅ $service est en cours d'exécution"
        else
            echo "❌ $service n'est pas en cours d'exécution"
            echo "Démarrage de $service..."
            net start "$service"
        fi
    done
else
    services=("redis-server" "rabbitmq-server" "elasticsearch")
    for service in "${services[@]}"; do
        if systemctl is-active --quiet $service; then
            echo "✅ $service est en cours d'exécution"
        else
            echo "❌ $service n'est pas en cours d'exécution"
            echo "Démarrage de $service..."
            sudo systemctl start $service
        fi
    done
fi

# Création des répertoires nécessaires
echo "Création des répertoires..."
mkdir -p logs reports tmp uploads

# Démarrage de Celery
echo "Démarrage de Celery..."
if [ "$IS_WINDOWS" = true ]; then
    start /B poetry run celery -A app.workers.analysis_worker worker --loglevel=info --pool=solo
else
    poetry run celery -A app.workers.analysis_worker worker --loglevel=info &
fi

# Démarrage de l'application
echo "Démarrage de l'application..."
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload 