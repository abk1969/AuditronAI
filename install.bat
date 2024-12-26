@echo off
setlocal enabledelayedexpansion

echo [92mInstallation d'AuditronAI...[0m

:: Vérifier Python
echo.
echo [93mVérification de Python...[0m
python --version >nul 2>&1
if errorlevel 1 (
    echo [91mPython n'est pas installé. Veuillez l'installer d'abord.[0m
    exit /b 1
)
echo [92mPython trouvé.[0m

:: Vérifier pip
echo.
echo [93mVérification de pip...[0m
pip --version >nul 2>&1
if errorlevel 1 (
    echo [91mpip n'est pas installé. Installation...[0m
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py
    del get-pip.py
)
echo [92mpip trouvé.[0m

:: Créer un environnement virtuel
echo.
echo [93mCréation de l'environnement virtuel...[0m
python -m venv venv
call venv\Scripts\activate.bat

:: Mettre à jour pip
echo.
echo [93mMise à jour de pip...[0m
python -m pip install --upgrade pip

:: Installer les dépendances Python
echo.
echo [93mInstallation des dépendances Python...[0m
pip install -r requirements.txt

:: Vérifier Node.js et npm
echo.
echo [93mVérification de Node.js et npm...[0m
node --version >nul 2>&1
if errorlevel 1 (
    echo [91mNode.js n'est pas installé. Installation...[0m
    echo [93mTéléchargement de Node.js...[0m
    
    :: Détecter l'architecture
    if "%PROCESSOR_ARCHITECTURE%"=="AMD64" (
        set "NODE_URL=https://nodejs.org/dist/v16.15.0/node-v16.15.0-x64.msi"
    ) else (
        set "NODE_URL=https://nodejs.org/dist/v16.15.0/node-v16.15.0-x86.msi"
    )
    
    :: Télécharger et installer Node.js
    curl -o node_installer.msi !NODE_URL!
    msiexec /i node_installer.msi /qn
    del node_installer.msi
    
    :: Rafraîchir les variables d'environnement
    refreshenv
)
echo [92mNode.js trouvé.[0m

:: Installer les outils TypeScript
echo.
echo [93mInstallation des outils TypeScript...[0m
call npm install -g typescript eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin eslint-plugin-security

:: Installer les outils d'analyse Python
echo.
echo [93mInstallation des outils d'analyse Python...[0m
pip install bandit prospector radon vulture

:: Créer les répertoires nécessaires
echo.
echo [93mCréation des répertoires...[0m
if not exist "reports" mkdir reports
if not exist ".cache" mkdir .cache
if not exist "plugins" mkdir plugins
if not exist "logs" mkdir logs

:: Vérifier PostgreSQL si nécessaire
echo.
echo [93mVérification de PostgreSQL...[0m
psql --version >nul 2>&1
if errorlevel 1 (
    echo [93mPostgreSQL n'est pas installé. Voulez-vous l'installer? (O/N)[0m
    set /p install_postgres=
    if /i "!install_postgres!"=="O" (
        echo [93mVeuillez télécharger et installer PostgreSQL depuis:[0m
        echo https://www.postgresql.org/download/windows/
        echo.
        echo [93mAppuyez sur une touche une fois l'installation terminée...[0m
        pause >nul
    )
)

:: Configuration post-installation
echo.
echo [93mConfiguration post-installation...[0m

:: Créer le fichier .env s'il n'existe pas
if not exist .env (
    echo.
    echo [93mCréation du fichier .env...[0m
    copy .env.example .env >nul
    echo [92mFichier .env créé. Veuillez le configurer avec vos paramètres.[0m
)

:: Installation terminée
echo.
echo [92mInstallation terminée avec succès![0m
echo.
echo [93mPour commencer:[0m
echo 1. Configurez le fichier .env avec vos paramètres
echo 2. Activez l'environnement virtuel: venv\Scripts\activate.bat
echo 3. Lancez l'exemple: python examples/analyze_project.py
echo.
echo [92mBonne analyse![0m

:: Pause pour voir les messages
pause

endlocal
