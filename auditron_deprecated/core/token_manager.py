from pathlib import Path
import yaml
from typing import List, Dict, Any
import os

class TokenManager:
    """Gestionnaire pour contrôler l'utilisation des tokens lors de l'analyse."""
    
    def __init__(self, config_path: str = "configs/token_management.yaml"):
        """Initialise le gestionnaire de tokens.
        
        Args:
            config_path: Chemin vers le fichier de configuration
        """
        self.config = self._load_config(config_path)
        self.current_tokens = 0
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Charge la configuration depuis le fichier YAML.
        
        Args:
            config_path: Chemin vers le fichier de configuration
            
        Returns:
            Dict contenant la configuration
        """
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            raise RuntimeError(f"Erreur lors du chargement de la configuration: {str(e)}")
            
    def split_code_into_chunks(self, code: str) -> List[str]:
        """Découpe le code en chunks analysables.
        
        Args:
            code: Code source à découper
            
        Returns:
            Liste des chunks de code
        """
        lines = code.split('\n')
        chunk_size = self.config['token_management']['code_chunking']['max_chunk_size']
        overlap = self.config['token_management']['code_chunking']['overlap']
        
        chunks = []
        start = 0
        while start < len(lines):
            end = min(start + chunk_size, len(lines))
            chunk = '\n'.join(lines[start:end])
            chunks.append(chunk)
            start = end - overlap
            
        return chunks
        
    def get_next_task(self) -> Dict[str, Any]:
        """Retourne la prochaine tâche d'analyse à effectuer.
        
        Returns:
            Dict contenant les informations de la tâche
        """
        tasks = self.config['token_management']['analysis_tasks']
        for task in sorted(tasks, key=lambda x: x['priority']):
            if self.current_tokens + task['max_tokens'] <= 80000:
                return task
        return None
        
    def apply_token_reduction(self, code: str) -> str:
        """Applique les stratégies de réduction de tokens.
        
        Args:
            code: Code source à optimiser
            
        Returns:
            Code optimisé
        """
        strategies = self.config['token_management']['token_reduction']
        
        if strategies['exclude_comments']:
            code = self._remove_comments(code)
            
        if strategies['simplify_formatting']:
            code = self._simplify_formatting(code)
            
        if strategies['focus_relevant_sections']:
            code = self._extract_relevant_sections(code)
            
        return code
        
    def _remove_comments(self, code: str) -> str:
        """Supprime les commentaires du code."""
        # Implémentation de la suppression des commentaires
        return code
        
    def _simplify_formatting(self, code: str) -> str:
        """Simplifie le formatage du code."""
        # Implémentation de la simplification du formatage
        return code
        
    def _extract_relevant_sections(self, code: str) -> str:
        """Extrait les sections pertinentes du code."""
        # Implémentation de l'extraction des sections pertinentes
        return code
        
    def update_token_count(self, tokens: int) -> None:
        """Met à jour le compteur de tokens.
        
        Args:
            tokens: Nombre de tokens à ajouter
        """
        self.current_tokens += tokens
        
    def reset_token_count(self) -> None:
        """Réinitialise le compteur de tokens."""
        self.current_tokens = 0
