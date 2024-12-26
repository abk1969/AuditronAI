# Utiliser une image Python officielle comme base
FROM python:3.11-slim

# Définir les variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.4.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv" \
    PYTHONPATH="/app"

# Ajouter poetry au PATH
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Installer les dépendances système nécessaires
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        build-essential \
        git \
        nodejs \
        npm \
        postgresql-client \
        libpq-dev \
        ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    # Installer poetry
    && curl -sSL https://install.python-poetry.org | python3 - \
    # Installer les outils TypeScript globalement
    && npm install -g typescript eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin eslint-plugin-security

# Créer le répertoire de travail
WORKDIR /app

# Copier d'abord les fichiers de dépendances
COPY pyproject.toml poetry.lock package*.json ./

# Installer les dépendances Python et Node.js
RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --only main \
    && pip install --no-cache-dir sqlparse \
    && npm ci --only=production

# Copier le reste du code source
COPY . .

# Créer les répertoires nécessaires
RUN mkdir -p reports logs .cache plugins

# Exposer le port pour l'interface web
EXPOSE 8501

# Définir les volumes pour la persistance
VOLUME ["/app/reports", "/app/logs", "/app/.cache", "/app/plugins"]

# Script d'entrée
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["docker-entrypoint.sh"]

# Commande par défaut
CMD ["python", "-m", "streamlit", "run", "AuditronAI/app/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]

# Labels
LABEL maintainer="AuditronAI Team <contact@auditronai.com>" \
      version="1.0.0" \
      description="Système d'analyse de code multi-langage" \
      org.opencontainers.image.source="https://github.com/votre-username/AuditronAI"
