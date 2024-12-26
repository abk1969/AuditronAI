#!/bin/bash
set -e

echo "⚙️ Configuration du backend..."

# Créer le fichier de configuration principal
cat > app/core/config.py << EOF
from pydantic import BaseSettings, PostgresDsn, RedisDsn
from typing import Optional, Dict, Any
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "AuditronAI"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["*"]
    
    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "auditronai"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_URI: Optional[RedisDsn] = None
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
    
    @property
    def REDIS_URI(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
EOF

# Créer le fichier de logging
cat > app/core/logging.py << EOF
import logging
import sys
from pathlib import Path

def setup_logging():
    # Créer le dossier logs s'il n'existe pas
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configuration du logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "app.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Désactiver les logs trop verbeux
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    
    return logging.getLogger(__name__)

logger = setup_logging()
EOF

echo "✅ Configuration du backend terminée" 