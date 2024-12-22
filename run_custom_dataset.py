import sys
import os

from AuditronAI.glue.promptopt.instantiate import GluePromptOpt
from custom_dataset import CustomMathDataset
from dotenv import load_dotenv

def main():
    # Charger les variables d'environnement
    load_dotenv(override=True)
    
    # Chemins de configuration
    config_dir = "configs"
    prompt_config_path = os.path.join(config_dir, "promptopt_config.yaml")
    setup_config_path = os.path.join(config_dir, "setup_config.yaml")
    dataset_jsonl = os.path.join("data", "train.jsonl")
    
    # Créer l'instance PromptOpt avec notre configuration
    prompt_opt = GluePromptOpt(
        prompt_config_path=prompt_config_path,
        setup_config_path=setup_config_path,
        dataset=CustomMathDataset(dataset_jsonl)
    )
    
    # Obtenir le meilleur prompt
    best_prompt, expert_profile = prompt_opt.get_best_prompt()

if __name__ == "__main__":
    main()
