from pydantic import BaseSettings, AnyHttpUrl, EmailStr, validator
from typing import List, Optional, Dict, Any
from pathlib import Path
import os

class Settings(BaseSettings):
    """Configuration de l'application."""
    
    # Configuration générale
    BASE_URL: str
    DEBUG: bool = False
    SECRET_KEY: str
    
    # Base de données
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    
    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # Redis et RabbitMQ
    REDIS_URL: str
    RABBITMQ_URL: str
    
    # Elasticsearch
    ELASTICSEARCH_URL: str
    
    # Email (SMTP)
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    SMTP_FROM_EMAIL: EmailStr
    SMTP_USE_TLS: bool = True
    
    # Slack
    SLACK_ENABLED: bool = False
    SLACK_WEBHOOK_URL: Optional[str]
    SLACK_BOT_TOKEN: Optional[str]
    SLACK_DEFAULT_CHANNEL: str = "#auditronai-alerts"
    SLACK_ALERTS_CHANNEL: str = "#auditronai-critical"
    
    @validator("SLACK_WEBHOOK_URL", "SLACK_BOT_TOKEN")
    def validate_slack_config(cls, v: Optional[str], values: Dict[str, Any]) -> Optional[str]:
        if values.get("SLACK_ENABLED", False) and not v:
            raise ValueError("Slack est activé mais l'URL du webhook ou le token du bot n'est pas configuré")
        return v
    
    # Rapports
    REPORTS_DIR: Path
    MAX_REPORT_AGE_DAYS: int = 30
    REPORT_CLEANUP_ENABLED: bool = True
    
    @validator("REPORTS_DIR")
    def validate_reports_dir(cls, v: Path) -> Path:
        os.makedirs(v, exist_ok=True)
        return v
    
    # Stockage
    TEMP_DIR: Path
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5MB par défaut
    
    @validator("TEMP_DIR")
    def validate_temp_dir(cls, v: Path) -> Path:
        os.makedirs(v, exist_ok=True)
        return v
    
    # Sécurité
    ALLOWED_HOSTS: List[str]
    CORS_ORIGINS: List[AnyHttpUrl]
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    @validator("ALLOWED_HOSTS", pre=True)
    def validate_allowed_hosts(cls, v: str) -> List[str]:
        return v.split(",")
    
    @validator("CORS_ORIGINS", pre=True)
    def validate_cors_origins(cls, v: str) -> List[AnyHttpUrl]:
        return v.split(",")
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Path
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    @validator("LOG_FILE")
    def validate_log_file(cls, v: Path) -> Path:
        os.makedirs(os.path.dirname(v), exist_ok=True)
        return v
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 