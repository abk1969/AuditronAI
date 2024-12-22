import pytest
from AuditronAI.core.security_analyzer import SecurityAnalyzer

def test_radon_analysis(security_analyzer):
    """Test cyclomatic complexity analysis."""
    code = """
def complex_function(x):
    if x > 0:
        if x < 10:
            return True
    return False
    """
    results = security_analyzer.run_radon_analysis(code)
    assert 'average_complexity' in results
    assert 'functions' in results
    assert isinstance(results['average_complexity'], (int, float))

def test_vulture_analysis(security_analyzer):
    """Test unused code detection."""
    code = """
def unused_function():
    pass

unused_variable = 42
    """
    results = security_analyzer.run_vulture_analysis(code)
    assert 'unused_vars' in results
    assert 'unused_funcs' in results
    assert len(results['unused_vars']) > 0
    assert len(results['unused_funcs']) > 0

def test_prospector_analysis(security_analyzer):
    """Test code quality analysis."""
    code = """
def bad_function():
    x = 1
    y = 2
    z = 3
    return x
    """
    results = security_analyzer.run_prospector_analysis(code)
    assert 'messages' in results
    assert isinstance(results['messages'], list)
