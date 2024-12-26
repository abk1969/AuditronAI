#!/bin/bash
set -e

echo "🔍 Vérification du backend..."

# Vérifier l'environnement Python
check_python_env() {
    echo "Vérification de l'environnement Python..."
    
    if [ ! -d "venv" ]; then
        echo "❌ Environnement virtuel manquant"
        return 1
    fi
    
    source venv/bin/activate
    
    if ! python -c "import fastapi" 2>/dev/null; then
        echo "❌ FastAPI n'est pas installé"
        return 1
    fi
    
    echo "✅ Environnement Python OK"
}

# Vérifier la base de données
check_database() {
    echo "Vérification de la base de données..."
    
    if ! PGPASSWORD=postgres psql -h localhost -U postgres -d auditronai -c '\dt' >/dev/null 2>&1; then
        echo "❌ Impossible de se connecter à la base de données"
        return 1
    fi
    
    # Vérifier les migrations
    if ! alembic current >/dev/null 2>&1; then
        echo "❌ Problème avec les migrations Alembic"
        return 1
    fi
    
    echo "✅ Base de données OK"
}

# Vérifier l'API
check_api() {
    echo "Démarrage du serveur de test..."
    python -m uvicorn app.main:app --host localhost --port 8000 --reload &
    PID=$!
    
    # Attendre le démarrage du serveur
    sleep 5
    
    # Tester l'API
    if curl -s http://localhost:8000/health | grep -q "ok"; then
        echo "✅ API OK"
    else
        echo "❌ API ne répond pas correctement"
        kill $PID
        return 1
    fi
    
    kill $PID
}

# Exécuter toutes les vérifications
check_python_env
check_database
check_api

echo "✅ Vérification du backend terminée avec succès" 