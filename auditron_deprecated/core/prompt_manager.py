import yaml
from pathlib import Path
from typing import Dict, Any, Optional

class PromptManager:
    def __init__(self, template_path: Optional[str] = None):
        if template_path is None:
            template_path = Path(__file__).parent.parent / "templates" / "prompts.yaml"
        
        with open(template_path, 'r', encoding='utf-8') as f:
            self.templates = yaml.safe_load(f)
            
        self.default_config = self.templates.get('default', {})
    
    def get_prompt(self, prompt_name: str, **kwargs) -> Dict[str, Any]:
        if prompt_name not in self.templates.get('custom_prompts', {}):
            raise ValueError(f"Prompt '{prompt_name}' non trouvé")
            
        prompt_config = self.templates['custom_prompts'][prompt_name].copy()
        
        # Formatter le prompt avec les variables fournies
        if 'user' in prompt_config:
            prompt_config['user'] = prompt_config['user'].format(**kwargs)
            
        # Fusionner avec les paramètres par défaut
        return {**self.default_config, **prompt_config} 