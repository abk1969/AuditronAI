@echo off
setlocal enabledelayedexpansion

:: Couleurs pour les messages
set "GREEN=[32m"
set "YELLOW=[33m"
set "RED=[31m"
set "NC=[0m"

echo %GREEN%=== Installation automatisée de PromptWizard ===%NC%
echo.

:: Vérification de Docker
echo %GREEN%[INFO]%NC% Vérification de Docker...
docker --version > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo %RED%[ERROR]%NC% Docker n'est pas installé. Veuillez l'installer : https://docs.docker.com/get-docker/
    exit /b 1
)

:: Vérification de Docker Compose
echo %GREEN%[INFO]%NC% Vérification de Docker Compose...
docker compose version > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo %RED%[ERROR]%NC% Docker Compose n'est pas installé. Veuillez l'installer : https://docs.docker.com/compose/install/
    exit /b 1
)

:: Vérification des ports
echo %GREEN%[INFO]%NC% Vérification des ports requis...
netstat -ano | findstr ":8501" > nul
if %ERRORLEVEL% equ 0 (
    echo %RED%[ERROR]%NC% Le port 8501 est déjà utilisé. Veuillez libérer ce port avant de continuer.
    exit /b 1
)
netstat -ano | findstr ":5432" > nul
if %ERRORLEVEL% equ 0 (
    echo %RED%[ERROR]%NC% Le port 5432 est déjà utilisé. Veuillez libérer ce port avant de continuer.
    exit /b 1
)
echo %GREEN%[INFO]%NC% Les ports requis sont disponibles

:: Configuration de l'environnement
echo %GREEN%[INFO]%NC% Configuration de l'environnement...
if not exist .env (
    if exist .env.example (
        copy .env.example .env > nul
        echo %GREEN%[INFO]%NC% Fichier .env créé à partir de .env.example
    ) else (
        echo %RED%[ERROR]%NC% Fichier .env.example non trouvé
        exit /b 1
    )
) else (
    echo %YELLOW%[WARN]%NC% Le fichier .env existe déjà
)

:: Démarrage des services
echo %GREEN%[INFO]%NC% Démarrage des services...
docker compose down > nul 2>&1
docker compose pull
docker compose up -d --build

:: Attente du démarrage des services
echo %GREEN%[INFO]%NC% Attente du démarrage des services...
set /a attempt=1
set /a max_attempts=30

:wait_loop
curl -s http://localhost:8501 > nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo.
    echo %GREEN%[INFO]%NC% Application démarrée avec succès!
    echo.
    echo %GREEN%Installation terminée avec succès!%NC%
    echo Accédez à l'application : %GREEN%http://localhost:8501%NC%
    echo.
    echo Commandes utiles :
    echo - Voir les logs : %YELLOW%docker compose logs -f%NC%
    echo - Arrêter l'application : %YELLOW%docker compose down%NC%
    echo - Redémarrer l'application : %YELLOW%docker compose restart%NC%
    goto :end
)

if %attempt% geq %max_attempts% (
    echo.
    echo %RED%[ERROR]%NC% L'application n'a pas démarré dans le temps imparti
    exit /b 1
)

set /a attempt+=1
echo|set /p=".."
timeout /t 2 /nobreak > nul
goto :wait_loop

:end
endlocal
