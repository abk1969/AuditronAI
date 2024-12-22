"""Tests pour l'analyse Flake8."""
import pytest
from AuditronAI.core.security_analyzer import SecurityAnalyzer

@pytest.fixture
def analyzer():
    """Fixture pour l'analyseur de sécurité."""
    return SecurityAnalyzer()

@pytest.fixture
def code_with_style_issues():
    """Code Python avec des problèmes de style."""
    return """
def bad_function( x ):
    y=x+1
    if(y>10):
        return True
    return False

unused_variable = 42
"""

def test_flake8_basic(analyzer, code_with_style_issues):
    """Test l'analyse de base avec flake8."""
    results = analyzer.run_flake8_analysis(code_with_style_issues)
    assert 'messages' in results
    assert not results.get('error')
    assert len(results['messages']) > 0

def test_flake8_empty_code(analyzer):
    """Test l'analyse de code vide."""
    results = analyzer.run_flake8_analysis("")
    assert 'messages' in results
    assert len(results['messages']) == 0

def test_flake8_perfect_code(analyzer):
    """Test l'analyse de code parfait."""
    perfect_code = """
def calculate_sum(a: int, b: int) -> int:
    \"\"\"Calcule la somme de deux nombres.\"\"\"
    return a + b
"""
    results = analyzer.run_flake8_analysis(perfect_code)
    assert 'messages' in results
    assert len(results['messages']) == 0

def test_flake8_message_format(analyzer, code_with_style_issues):
    """Test le format des messages d'erreur."""
    results = analyzer.run_flake8_analysis(code_with_style_issues)
    for msg in results['messages']:
        assert 'type' in msg
        assert 'code' in msg
        assert 'message' in msg
        assert 'line' in msg
        assert 'column' in msg
        assert msg['type'] == 'style' 