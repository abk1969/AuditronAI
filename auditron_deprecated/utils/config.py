import os
from dotenv import load_dotenv
from typing import Optional

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        load_dotenv()
        self.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.azure_key = os.getenv("AZURE_OPENAI_KEY")
        self.model = os.getenv("AZURE_OPENAI_MODEL")
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION")

    @property
    def is_configured(self) -> bool:
        return all([
            self.azure_endpoint,
            self.azure_key,
            self.model,
            self.api_version
        ]) 