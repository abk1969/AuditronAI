from PromptWizard.core.claude_context_manager import ClaudeContextManager

def example_task_splitting():
    """Exemple de découpage d'une grande tâche en sous-tâches."""
    
    # Initialisation du gestionnaire
    context_manager = ClaudeContextManager()
    
    # Démarrage d'une nouvelle tâche
    task_id = context_manager.start_task("Analyser et améliorer la sécurité du projet")
    
    # Définition des sous-tâches avec contexte minimal nécessaire
    context_manager.add_subtask(
        "Analyser les dépendances",
        ["requirements.txt", "pyproject.toml"]
    )
    
    context_manager.add_subtask(
        "Vérifier les configurations de sécurité",
        ["configs/security_config.yaml"]
    )
    
    context_manager.add_subtask(
        "Analyser le code source principal",
        ["core/security_analyzer.py"]
    )
    
    # Traitement séquentiel des sous-tâches
    while True:
        subtask = context_manager.get_next_subtask()
        if not subtask:
            break
            
        print(f"Exécution de la sous-tâche: {subtask['description']}")
        print(f"Contexte chargé: {list(subtask['context'].keys())}")
        
        # Simulation du traitement de la sous-tâche
        # Dans un cas réel, Claude analyserait uniquement le contexte 
        # de la sous-tâche courante
        
        context_manager.complete_subtask()
        
if __name__ == "__main__":
    example_task_splitting()
