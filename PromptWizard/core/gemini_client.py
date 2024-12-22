import google.generativeai as genai
import os
from dotenv import load_dotenv

class GeminiClient:
    VALID_MODELS = [
        'gemini-2.0-flash-exp',
        'gemini-pro',
        'gemini-pro-vision'
    ]
    
    def __init__(self):
        load_dotenv()
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("La variable d'environnement GOOGLE_API_KEY est requise")
            
        genai.configure(api_key=api_key)
        
        model = os.getenv("GOOGLE_MODEL", "gemini-2.0-flash-exp")
        if model not in self.VALID_MODELS:
            print(f"Warning: Modèle {model} non reconnu, utilisation de gemini-2.0-flash-exp par défaut")
            model = "gemini-2.0-flash-exp"
        self.model = model
        
    def generate_completion(self, prompt: str, system_message: str = None, **kwargs):
        try:
            model = genai.GenerativeModel(self.model)
            
            # Combiner system message et prompt si nécessaire
            full_prompt = f"{system_message}\n\n{prompt}" if system_message else prompt
            
            response = model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            print(f"Modèle utilisé : {self.model}")
            raise Exception(f"Erreur lors de la génération : {str(e)}") 