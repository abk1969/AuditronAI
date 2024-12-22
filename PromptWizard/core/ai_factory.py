from .openai_client import OpenAIClient
from .gemini_client import GeminiClient
import os

def get_ai_client():
    """Factory pour obtenir le bon client AI selon la configuration."""
    service = os.getenv("AI_SERVICE", "openai").lower()
    
    if service == "openai":
        return OpenAIClient()
    elif service == "google":
        return GeminiClient()
    else:
        raise ValueError(f"Service AI non reconnu : {service}") 