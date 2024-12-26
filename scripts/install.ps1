# Script d'installation pour Windows
Write-Host "Installation des dépendances AuditronAI..." -ForegroundColor Yellow

# Vérifie si Poetry est installé
if (!(Get-Command poetry -ErrorAction SilentlyContinue)) {
    Write-Host "Poetry n'est pas installé. Installation en cours..." -ForegroundColor Red
    (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
}

# Configure Poetry
Write-Host "Configuration de Poetry..." -ForegroundColor Yellow
poetry config virtualenvs.in-project true

# Installation des dépendances
Write-Host "Installation des dépendances du projet..." -ForegroundColor Yellow
poetry install --no-root

# Installation des hooks pre-commit
Write-Host "Installation des hooks pre-commit..." -ForegroundColor Yellow
poetry run pre-commit install

# Vérifie les vulnérabilités de sécurité
Write-Host "Vérification des vulnérabilités de sécurité..." -ForegroundColor Yellow
poetry run safety check

Write-Host "Installation terminée avec succès !" -ForegroundColor Green
Write-Host "Pour activer l'environnement virtuel, exécutez : " -ForegroundColor Yellow -NoNewline
Write-Host "poetry shell" -ForegroundColor Green 