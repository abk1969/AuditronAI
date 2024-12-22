import pytest
from AuditronAI.core.security_analyzer import SecurityAnalyzer
from AuditronAI.core.history import AnalysisHistory
from pathlib import Path
import json

@pytest.fixture
def sample_code():
    return """
def insecure_function(user_input):
    # Exemple de code avec des problèmes de sécurité
    exec(user_input)  # Bandit: B102
    password = "hardcoded_password"  # Bandit: B105
    return eval(user_input)  # Bandit: B307
"""

@pytest.fixture
def security_analyzer():
    return SecurityAnalyzer()

def test_security_analysis(security_analyzer, sample_code):
    """Test l'analyse de sécurité complète."""
    results = security_analyzer.analyze(sample_code, "test.py")
    
    assert 'security_issues' in results
    assert 'code_quality' in results
    assert 'summary' in results
    assert results['summary']['score'] < 100  # Le score devrait être réduit à cause des problèmes

def test_bandit_analysis(security_analyzer, sample_code):
    """Test l'analyse Bandit."""
    results = security_analyzer.run_bandit_analysis(sample_code, "test.py")
    
    assert 'issues' in results
    assert len(results['issues']) > 0
    assert any(issue['test_name'] == 'B102' for issue in results['issues'])

def test_radon_analysis(security_analyzer, sample_code):
    """Test l'analyse Radon."""
    results = security_analyzer.run_radon_analysis(sample_code)
    
    assert 'average_complexity' in results
    assert 'functions' in results
    assert isinstance(results['average_complexity'], (int, float)) 

def test_vulture_analysis(security_analyzer, sample_code):
    """Test l'analyse Vulture."""
    results = security_analyzer.run_vulture_analysis(sample_code)
    
    assert 'unused_vars' in results
    assert 'unused_funcs' in results
    assert isinstance(results['unused_vars'], list)
    assert isinstance(results['unused_funcs'], list)

def test_prospector_analysis(security_analyzer, sample_code):
    """Test l'analyse Prospector."""
    results = security_analyzer.run_prospector_analysis(sample_code)
    
    assert 'messages' in results
    assert isinstance(results['messages'], list)

def test_error_handling(security_analyzer):
    """Test la gestion des erreurs."""
    # Test avec du code invalide
    invalid_code = "def invalid_python(:"
    
    results = security_analyzer.analyze(invalid_code, "invalid.py")
    assert 'error' not in results  # Ne devrait pas planter
    assert results['summary']['score'] == 0.0  # Score minimum en cas d'erreur

@pytest.mark.parametrize("code,expected_score", [
    ("", 100.0),  # Code vide
    ("print('Hello')", 100.0),  # Code simple sans problème
    ("exec(input())", 80.0),  # Code avec un problème de sécurité
])
def test_scoring(security_analyzer, code, expected_score):
    """Test le système de scoring."""
    results = security_analyzer.analyze(code, "test.py")
    assert abs(results['summary']['score'] - expected_score) <= 20.0