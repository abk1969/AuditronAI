"""
Package de tests pour AuditronAI.

Ce package contient tous les tests unitaires et d'intégration.
Les fixtures communes sont définies dans conftest.py.
"""

from pathlib import Path

# Chemins importants pour les tests
TEST_DIR = Path(__file__).parent
DATA_DIR = TEST_DIR / 'data'
FIXTURES_DIR = TEST_DIR / 'fixtures'
BANDIT_DIR = TEST_DIR / 'bandit'

# Créer les répertoires nécessaires
for dir_path in [DATA_DIR, FIXTURES_DIR, BANDIT_DIR]:
    dir_path.mkdir(exist_ok=True) 