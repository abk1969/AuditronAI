FROM python:3.11-slim

WORKDIR /app

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Installation de Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copie des fichiers de dépendances
COPY pyproject.toml poetry.lock ./

# Installation des dépendances
RUN /root/.local/bin/poetry config virtualenvs.create false \
    && /root/.local/bin/poetry install --no-interaction --no-ansi

# Copie du code source
COPY . .

# Exposition du port
EXPOSE 8000

# Commande de démarrage
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 