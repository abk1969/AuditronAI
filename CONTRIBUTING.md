# Guide de Contribution

Merci de votre intérêt pour contribuer à AuditronAI ! Ce guide vous aidera à comprendre le processus de contribution.

## Code de Conduite

En participant à ce projet, vous vous engagez à maintenir un environnement respectueux et professionnel. Nous attendons de tous les contributeurs qu'ils :
- Soient respectueux et bienveillants dans leurs communications
- Acceptent les critiques constructives
- Se concentrent sur ce qui est le mieux pour la communauté
- Fassent preuve d'empathie envers les autres membres

## Comment Contribuer

### Signaler des Bugs

1. Vérifiez que le bug n'a pas déjà été signalé
2. Créez une issue avec un titre clair et descriptif
3. Incluez :
   - Les étapes pour reproduire le bug
   - Le comportement attendu vs observé
   - Des captures d'écran si pertinent
   - Votre environnement (OS, version Python, etc.)

### Proposer des Améliorations

1. Créez une issue décrivant votre proposition
2. Incluez :
   - Le problème que vous souhaitez résoudre
   - Comment votre solution l'améliorerait
   - Des exemples d'utilisation si possible

### Soumettre des Modifications

1. Fork le projet
2. Créez une branche (`git checkout -b feature/amazing-feature`)
3. Committez vos changements (`git commit -m 'Add amazing feature'`)
4. Push la branche (`git push origin feature/amazing-feature`)
5. Ouvrez une Pull Request

## Standards de Code

### Style de Code

- Suivez PEP 8 pour Python
- Utilisez des noms descriptifs en français
- Commentez le code complexe
- Documentez les fonctions avec docstrings
- Maintenez une couverture de tests > 80%

### Structure du Projet

```
AuditronAI/
├── core/               # Logique métier
│   ├── analyzers/     # Analyseurs de code
│   ├── services/      # Services
│   └── utils/         # Utilitaires
├── app/               # Interface utilisateur
├── tests/             # Tests
└── docs/              # Documentation
```

### Tests

- Écrivez des tests pour tout nouveau code
- Utilisez pytest pour les tests
- Incluez des tests unitaires et d'intégration
- Vérifiez que tous les tests passent avant de soumettre

## Processus de Développement

1. **Planification**
   - Discutez des changements majeurs dans les issues
   - Obtenez un consensus sur l'approche

2. **Développement**
   - Créez une branche pour vos modifications
   - Suivez les standards de code
   - Committez fréquemment avec des messages clairs

3. **Tests**
   - Ajoutez/modifiez les tests appropriés
   - Vérifiez la couverture de tests
   - Exécutez la suite de tests complète

4. **Documentation**
   - Mettez à jour la documentation si nécessaire
   - Incluez des commentaires de code pertinents
   - Documentez les nouvelles fonctionnalités

5. **Review**
   - Demandez une review via Pull Request
   - Répondez aux commentaires de manière constructive
   - Faites les modifications demandées

## Ajout d'Analyseurs

Pour ajouter un nouvel analyseur :

1. Créez une classe héritant de `BaseAnalyzer`
2. Implémentez les méthodes requises
3. Ajoutez le type dans `AnalyzerType`
4. Enregistrez l'analyseur dans `AnalyzerRegistry`
5. Ajoutez les tests appropriés
6. Documentez l'analyseur

Exemple :
```python
from AuditronAI.core.analyzers.base_analyzer import BaseAnalyzer
from AuditronAI.core.analyzers.interfaces import AnalyzerType

class CustomAnalyzer(BaseAnalyzer):
    @property
    def analyzer_type(self) -> AnalyzerType:
        return AnalyzerType.CUSTOM

    async def _analyze_impl(self) -> Dict[str, Any]:
        # Implémentation...
        return results
```

## Release Process

1. **Versioning**
   - Suivez le Semantic Versioning (MAJOR.MINOR.PATCH)
   - Documentez les changements dans CHANGELOG.md

2. **Testing**
   - Exécutez la suite de tests complète
   - Testez sur différents environnements
   - Vérifiez la documentation

3. **Release**
   - Créez un tag de version
   - Générez les notes de release
   - Publiez sur PyPI si applicable

## Support

- Utilisez les issues GitHub pour les questions
- Consultez la documentation existante
- Rejoignez notre canal de discussion

## Licence

En contribuant, vous acceptez que vos contributions soient sous la même licence que le projet (MIT).
