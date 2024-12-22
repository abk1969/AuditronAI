# AuditronAI 🛡️

Analyseur de code Python avec IA et sécurité renforcée.

## Fonctionnalités

- 🔍 Analyse statique du code
- 🤖 Analyse IA (OpenAI GPT / Google Gemini)
- 🛡️ Vérification de sécurité
- 📊 Métriques de qualité
- 💡 Recommandations d'amélioration

## Installation

```bash
# Cloner le repo
git clone https://github.com/votre-username/auditron-ai.git
cd auditron-ai

# Installer avec Poetry
poetry install

# Créer les dossiers nécessaires
mkdir -p logs data
```

## Configuration

1. Copier le fichier d'exemple :
```bash
cp .env.example .env
```

2. Configurer les clés API :
- OpenAI : https://platform.openai.com/api-keys
- Google : https://ai.google.dev/tutorials/setup

## Utilisation

```bash
# Lancer l'application
poetry run streamlit run AuditronAI/app/streamlit_app.py
```

## Développement

```bash
# Tests
poetry run pytest

# Linting
poetry run black .
poetry run isort .
```

## Licence

MIT License - voir [LICENSE.md](LICENSE.md)
