import os
from typing import Dict, Any, Optional
import anthropic
from .logger import get_logger

logger = get_logger(__name__)

class AnthropicClient:
    """Client pour interagir avec l'API Claude d'Anthropic."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialise le client Anthropic.
        
        Args:
            config: Configuration du client Anthropic
        """
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
            
        self.model = config["model"]
        self.max_tokens = config.get("max_tokens", 80000)
        self.client = anthropic.Anthropic(api_key=self.api_key)
        
    async def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """Génère une réponse en utilisant Claude.
        
        Args:
            prompt: Le prompt à envoyer à Claude
            system_prompt: Prompt système optionnel
            temperature: Température pour la génération (0-1)
            max_tokens: Nombre maximum de tokens pour la réponse
            
        Returns:
            La réponse générée par Claude
        """
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens or self.max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            return message.content[0].text
            
        except Exception as e:
            logger.error(f"Erreur lors de l'appel à Claude: {str(e)}")
            raise
            
    def count_tokens(self, text: str) -> int:
        """Compte le nombre de tokens dans un texte.
        
        Args:
            text: Texte à analyser
            
        Returns:
            Nombre de tokens
        """
        return self.client.count_tokens(text)
        
    def validate_response(self, response: str) -> bool:
        """Valide une réponse de Claude.
        
        Args:
            response: Réponse à valider
            
        Returns:
            True si la réponse est valide
        """
        # Implémentez ici la logique de validation
        return True
