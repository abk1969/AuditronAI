# AuditronAI

Application d'analyse de code avec support pour plusieurs langages et types d'analyse.

## Architecture

L'application suit une architecture modulaire permettant d'ajouter facilement de nouvelles fonctionnalités d'analyse :

```
AuditronAI/
├── core/
│   ├── analyzers/           # Analyseurs de code
│   │   ├── strategies/      # Stratégies d'analyse
│   │   └── repositories/    # Patterns et règles
│   └── services/
│       └── analysis_plugins/ # Plugins d'analyse
└── app/                     # Interface utilisateur
```

## Extension du Système

### 1. Ajouter un Nouvel Analyseur de Langage

Pour ajouter le support d'un nouveau langage, suivez ces étapes :

1. Créez les stratégies d'analyse dans `core/analyzers/strategies/`:
```python
class NewLanguageStrategy(ABC):
    @abstractmethod
    def analyze(self, code: str) -> Dict[str, Any]:
        pass
```

2. Implémentez l'analyseur dans `core/analyzers/`:
```python
class NewLanguageAnalyzer(BaseAnalyzer):
    def analyze(self, code: str, filename: str = None) -> Dict[str, Any]:
        # Implémentation de l'analyse
        pass
```

3. Créez le plugin dans `core/services/analysis_plugins/`:
```python
class NewLanguagePlugin(AnalysisPlugin):
    def analyze(self, code: str, filename: str) -> Dict[str, Any]:
        return self.analyzer.analyze(code, filename)
```

4. Enregistrez l'analyseur dans la factory (`core/analyzers/factory.py`):
```python
_analyzers: Dict[str, Type[BaseAnalyzer]] = {
    'new_language': NewLanguageAnalyzer
}
```

### 2. Ajouter une Nouvelle Stratégie d'Analyse

Pour ajouter un nouveau type d'analyse à un langage existant :

1. Créez une nouvelle stratégie dans le fichier approprié de `strategies/`:
```python
class NewAnalysisStrategy(AnalysisStrategy):
    def analyze(self, code: str) -> Dict[str, Any]:
        # Implémentation de la nouvelle analyse
        pass
```

2. Ajoutez la stratégie à l'analyseur correspondant:
```python
def __init__(self, config: AnalyzerConfig):
    self.strategies.append(NewAnalysisStrategy())
```

### 3. Exemple d'Utilisation

```python
from AuditronAI.core.services.code_analyzer_service import CodeAnalyzerService
from AuditronAI.core.services.analysis_plugins import NewLanguagePlugin

# Initialisation
service = CodeAnalyzerService()
service.register_plugin("new_language", NewLanguagePlugin)

# Analyse
results = service.analyze(code, "example.ext")
```

## Tests

Les tests sont organisés par fonctionnalité dans le dossier `tests/`. Pour ajouter des tests pour une nouvelle fonctionnalité :

1. Créez un nouveau fichier de test dans le dossier approprié
2. Utilisez pytest pour les tests unitaires
3. Suivez le modèle des tests existants

Exemple:
```python
def test_new_analysis_feature(analyzer):
    code = "example code"
    result = analyzer.analyze(code)
    assert "expected_key" in result
```

## Configuration

La configuration des analyseurs se fait via `AnalyzerConfig`. Pour ajouter de nouvelles options :

1. Étendez la classe `AnalyzerConfig`
2. Ajoutez les nouvelles options dans le constructeur
3. Utilisez la configuration dans votre analyseur

## Bonnes Pratiques

1. Suivez les patterns de conception existants
2. Documentez le code avec des docstrings
3. Ajoutez des tests unitaires
4. Utilisez le type hinting
5. Respectez la structure modulaire

## Contribution

1. Fork le projet
2. Créez une branche pour votre fonctionnalité
3. Ajoutez vos modifications
4. Soumettez une pull request
