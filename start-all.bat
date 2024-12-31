@echo off
echo "🚀 Démarrage de tous les services AuditronAI..."

REM Vérification de Docker
where docker >nul 2>nul
if %errorlevel% neq 0 (
    echo "❌ Docker n'est pas installé. Veuillez l'installer : https://www.docker.com/products/docker-desktop"
    exit /b 1
)

REM Vérification de Docker Compose
where docker-compose >nul 2>nul
if %errorlevel% neq 0 (
    echo "❌ Docker Compose n'est pas installé. Veuillez l'installer avec Docker Desktop"
    exit /b 1
)

REM Vérification que Docker Desktop est en cours d'exécution
docker info >nul 2>nul
if %errorlevel% neq 0 (
    echo "❌ Docker Desktop n'est pas en cours d'exécution. Veuillez le démarrer."
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    echo "⏳ Attente du démarrage de Docker Desktop..."
    timeout /t 30
)

REM Arrêt des conteneurs existants
echo "🔄 Arrêt des conteneurs existants..."
docker-compose down

REM Démarrage des services Docker
echo "🐳 Démarrage des services Docker..."
docker-compose up -d postgres redis elasticsearch rabbitmq

REM Attente que les services soient prêts
echo "⏳ Attente que les services soient prêts..."
timeout /t 10

REM Vérification de Node.js
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo "❌ Node.js n'est pas installé. Veuillez l'installer : https://nodejs.org/"
    exit /b 1
)

REM Vérification de Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo "❌ Python n'est pas installé. Veuillez l'installer : https://www.python.org/"
    exit /b 1
)

REM Vérification de Poetry
where poetry >nul 2>nul
if %errorlevel% neq 0 (
    echo "Installation de Poetry..."
    curl -sSL https://install.python-poetry.org | python -
)

REM Configuration des variables d'environnement
if not exist backend\.env (
    echo "📝 Création du fichier .env..."
    copy backend\.env.example backend\.env
    echo "⚠️ Veuillez configurer les variables dans le fichier backend\.env"
    timeout /t 5
)

REM Installation des dépendances backend
echo "📦 Installation des dépendances backend..."
cd backend
poetry install
cd ..

REM Installation des dépendances frontend
echo "📦 Installation des dépendances frontend..."
cd frontend
call npm install
cd ..

REM Démarrage du backend
echo "🚀 Démarrage du backend..."
start cmd /k "cd backend && poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

REM Démarrage de Celery
echo "🌿 Démarrage de Celery..."
start cmd /k "cd backend && poetry run celery -A app.workers.analysis_worker worker --loglevel=info --pool=solo"

REM Démarrage du frontend
echo "🌐 Démarrage du frontend..."
start cmd /k "cd frontend && npm run dev"

echo "✨ Tous les services sont démarrés !"
echo "📊 Frontend: http://localhost:3000"
echo "🔧 Backend: http://localhost:8000"
echo "📚 Documentation API: http://localhost:8000/docs"

REM Attente de l'entrée utilisateur pour garder la fenêtre ouverte
pause 