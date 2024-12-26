from typing import List, Dict, Any
import json
from pathlib import Path

class ClaudeContextManager:
    """Gestionnaire de contexte pour optimiser l'utilisation des tokens de Claude."""
    
    def __init__(self):
        self.context_path = Path("context")
        self.context_path.mkdir(exist_ok=True)
        self.current_task_id = None
        
    def start_task(self, task_description: str) -> str:
        """Démarre une nouvelle tâche et retourne son ID."""
        task_id = self._generate_task_id()
        task_context = {
            "description": task_description,
            "subtasks": [],
            "current_subtask": 0,
            "completed": False
        }
        self._save_context(task_id, task_context)
        self.current_task_id = task_id
        return task_id
        
    def add_subtask(self, description: str, context_files: List[str] = None) -> None:
        """Ajoute une sous-tâche à la tâche courante."""
        if not self.current_task_id:
            raise RuntimeError("Aucune tâche active")
            
        context = self._load_context(self.current_task_id)
        subtask = {
            "description": description,
            "context_files": context_files or [],
            "completed": False
        }
        context["subtasks"].append(subtask)
        self._save_context(self.current_task_id, context)
        
    def get_next_subtask(self) -> Dict[str, Any]:
        """Retourne la prochaine sous-tâche à exécuter."""
        if not self.current_task_id:
            return None
            
        context = self._load_context(self.current_task_id)
        current = context["current_subtask"]
        
        if current >= len(context["subtasks"]):
            return None
            
        subtask = context["subtasks"][current]
        return {
            "description": subtask["description"],
            "context": self._load_subtask_context(subtask["context_files"])
        }
        
    def complete_subtask(self) -> None:
        """Marque la sous-tâche courante comme terminée."""
        if not self.current_task_id:
            return
            
        context = self._load_context(self.current_task_id)
        current = context["current_subtask"]
        
        if current < len(context["subtasks"]):
            context["subtasks"][current]["completed"] = True
            context["current_subtask"] += 1
            self._save_context(self.current_task_id, context)
            
    def _generate_task_id(self) -> str:
        """Génère un ID unique pour une tâche."""
        import uuid
        return str(uuid.uuid4())
        
    def _save_context(self, task_id: str, context: Dict[str, Any]) -> None:
        """Sauvegarde le contexte d'une tâche."""
        path = self.context_path / f"{task_id}.json"
        with open(path, "w") as f:
            json.dump(context, f, indent=2)
            
    def _load_context(self, task_id: str) -> Dict[str, Any]:
        """Charge le contexte d'une tâche."""
        path = self.context_path / f"{task_id}.json"
        if not path.exists():
            return None
        with open(path, "r") as f:
            return json.load(f)
            
    def _load_subtask_context(self, context_files: List[str]) -> Dict[str, Any]:
        """Charge le contexte spécifique à une sous-tâche."""
        context = {}
        for file in context_files:
            if Path(file).exists():
                with open(file, "r") as f:
                    context[file] = f.read()
        return context
