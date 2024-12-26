# Guide de Gestion du Contexte pour Claude

Ce guide explique comment optimiser l'utilisation des tokens de Claude en divisant les grandes tâches en sous-tâches plus petites et en gérant efficacement le contexte.

## Principes Clés

1. **Division des Tâches**
   - Diviser les grandes tâches en sous-tâches indépendantes
   - Chaque sous-tâche ne doit nécessiter que le contexte minimal nécessaire
   - Maintenir une progression séquentielle logique

2. **Gestion du Contexte**
   - Charger uniquement les fichiers nécessaires pour la sous-tâche courante
   - Éviter de charger des fichiers entiers quand seules certaines sections sont pertinentes
   - Utiliser des références pour maintenir la cohérence entre les sous-tâches

3. **Optimisation des Tokens**
   - Exclure les commentaires et le formatage non essentiel
   - Se concentrer sur les sections de code pertinentes
   - Utiliser des résumés et des métadonnées quand possible

## Stratégies de Découpage

### 1. Analyse de Code
```python
# Mauvais exemple - Trop de contexte chargé
context_manager.add_subtask(
    "Analyser le projet",
    ["**/*.py"]  # Charge tous les fichiers Python
)

# Bon exemple - Contexte ciblé
context_manager.add_subtask(
    "Analyser les dépendances",
    ["requirements.txt"]
)
context_manager.add_subtask(
    "Vérifier la configuration",
    ["config.yaml"]
)
context_manager.add_subtask(
    "Analyser le module principal",
    ["core/main.py"]
)
```

### 2. Refactoring
```python
# Mauvais exemple - Modification globale
context_manager.add_subtask(
    "Refactorer le code",
    ["src/"]  # Trop large
)

# Bon exemple - Modifications ciblées
context_manager.add_subtask(
    "Identifier les patterns à refactorer",
    ["src/patterns.py"]
)
context_manager.add_subtask(
    "Refactorer la gestion d'erreurs",
    ["src/error_handling.py"]
)
context_manager.add_subtask(
    "Mettre à jour les tests",
    ["tests/test_error_handling.py"]
)
```

## Bonnes Pratiques

1. **Planification**
   - Analyser la tâche globale avant de la diviser
   - Identifier les dépendances entre sous-tâches
   - Établir un ordre logique d'exécution

2. **Contexte**
   - Maintenir un état minimal entre les sous-tâches
   - Utiliser des fichiers temporaires pour les résultats intermédiaires
   - Nettoyer le contexte après chaque sous-tâche

3. **Progression**
   - Valider chaque sous-tâche avant de passer à la suivante
   - Maintenir un journal des modifications
   - Permettre la reprise en cas d'interruption

## Exemple d'Utilisation

```python
from PromptWizard.core.claude_context_manager import ClaudeContextManager

# Initialisation
context_manager = ClaudeContextManager()
task_id = context_manager.start_task("Améliorer la sécurité")

# Définition des sous-tâches
context_manager.add_subtask(
    "Audit des dépendances",
    ["requirements.txt"]
)
context_manager.add_subtask(
    "Vérification des configurations",
    ["security_config.yaml"]
)

# Exécution
while True:
    subtask = context_manager.get_next_subtask()
    if not subtask:
        break
    
    # Traitement de la sous-tâche avec contexte minimal
    process_subtask(subtask)
    context_manager.complete_subtask()
```

## Conclusion

Une bonne gestion du contexte est essentielle pour optimiser l'utilisation des tokens de Claude. En suivant ces principes et stratégies, vous pouvez traiter efficacement de grandes tâches tout en maintenant une utilisation raisonnable des tokens.
