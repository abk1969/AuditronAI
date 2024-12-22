import pytest
import os
from pathlib import Path
from dotenv import load_dotenv
import tempfile
import json

@pytest.fixture(autouse=True)
def setup_test_env():
    """Configure l'environnement de test."""
    # Charger les variables d'environnement de test
    load_dotenv(Path(__file__).parent / 'test.env')
    
    # Configuration spécifique aux tests
    os.environ['SECURITY_SCAN_LEVEL'] = 'high'
    os.environ['ENABLE_DEPENDENCY_CHECK'] = 'true'
    os.environ['ENABLE_STATIC_ANALYSIS'] = 'true'
    os.environ['SECURITY_TIMEOUT'] = '30'
    
    yield
    
    # Nettoyage après les tests
    if Path('test.py').exists():
        Path('test.py').unlink()

@pytest.fixture
def test_data_dir(tmp_path):
    """Crée un répertoire temporaire pour les données de test."""
    return tmp_path / "test_data"

@pytest.fixture
def sample_python_code():
    """Retourne du code Python pour les tests."""
    return """
def insecure_function(user_input):
    exec(user_input)  # Vulnérabilité de sécurité

def unused_function():
    pass

password = "hardcoded_password"  # Problème de sécurité
"""

@pytest.fixture
def sample_analysis_results():
    """Retourne des résultats d'analyse pour les tests."""
    return {
        'file': 'test.py',
        'security_issues': [
            {
                'severity': 'HIGH',
                'confidence': 'HIGH',
                'test_name': 'B102',
                'description': 'exec() used',
                'line_number': 2
            }
        ],
        'code_quality': {
            'complexity': 1.5,
            'functions': [
                {'name': 'insecure_function', 'complexity': 1},
                {'name': 'unused_function', 'complexity': 1}
            ],
            'unused_code': {
                'functions': ['unused_function'],
                'variables': []
            }
        },
        'summary': {
            'severity_counts': {'critical': 0, 'high': 1, 'medium': 0, 'low': 0},
            'total_issues': 1,
            'score': 90.0,
            'details': 'Test details'
        }
    }