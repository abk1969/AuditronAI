FROM python:3.9-slim

# Set environment variables
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VERSION=1.7.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python -

# Add Poetry to PATH
ENV PATH="${PATH}:/root/.local/bin"

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml poetry.lock ./
COPY AuditronAI/ ./AuditronAI/
COPY PromptWizard/ ./PromptWizard/

# Install dependencies
RUN poetry install --no-dev --no-root

# Install the project
RUN poetry install --no-dev

# Expose Streamlit port
EXPOSE 8501

# Command to run the application
CMD ["poetry", "run", "run-app"]
