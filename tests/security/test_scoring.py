import pytest
from AuditronAI.core.security_analyzer import SecurityAnalyzer

@pytest.mark.parametrize("code,expected_score,description", [
    ("", 100.0, "Code vide"),
    ("print('Hello')", 100.0, "Code simple sans problème"),
    ("exec(input())", 80.0, "Code avec un problème de sécurité"),
    ("password = 'secret123'", 90.0, "Code avec mot de passe en dur"),
    ("""
def complex_function():
    if x > 0:
        if x < 10:
            return True
    return False
    """, 70.0, "Code avec complexité élevée")
])
def test_scoring(security_analyzer, code, expected_score, description):
    """Test le système de scoring avec différents cas."""
    results = security_analyzer.analyze(code, f"test_{description}.py")
    assert abs(results['summary']['score'] - expected_score) <= 20.0, f"Score incorrect pour: {description}"
    assert not security_analyzer._temp_manager.temp_dir.exists()
