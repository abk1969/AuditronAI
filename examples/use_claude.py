import os
import asyncio
from dotenv import load_dotenv
from PromptWizard.core.anthropic_client import AnthropicClient

async def example_claude_usage():
    """Exemple d'utilisation du client Claude."""
    
    # Chargement des variables d'environnement
    load_dotenv()
    
    # Configuration du client
    config = {
        "model": "claude-3-sonnet-20241022",
        "max_tokens": 80000,
        "context_window": 200000
    }
    
    # Initialisation du client
    client = AnthropicClient(config)
    
    # Exemple de prompt avec contexte
    system_prompt = """Tu es un assistant expert en programmation Python."""
    
    user_prompt = """
    Peux-tu m'expliquer comment implémenter un décorateur de mise en cache en Python ?
    Je voudrais pouvoir mettre en cache le résultat des fonctions pour éviter de recalculer
    les mêmes valeurs plusieurs fois.
    """
    
    try:
        # Génération de la réponse
        response = await client.generate_response(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.7
        )
        print("Réponse de Claude:")
        print(response)
        
        # Exemple de comptage de tokens
        tokens = client.count_tokens(user_prompt)
        print(f"\nNombre de tokens dans le prompt: {tokens}")
        
    except Exception as e:
        print(f"Erreur: {str(e)}")

if __name__ == "__main__":
    # Exécution de l'exemple
    asyncio.run(example_claude_usage())
