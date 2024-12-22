import pytest
from AuditronAI.core.security_analyzer import SecurityAnalyzer

def test_security_analysis_structure(security_analyzer):
    """Test basic security analysis structure."""
    code = """
def test():
    pass
    """
    results = security_analyzer.analyze(code, "test.py")
    
    assert 'security_issues' in results
    assert 'code_quality' in results
    assert 'summary' in results
    assert not security_analyzer._temp_manager.temp_dir.exists()

def test_empty_code_analysis(security_analyzer):
    """Test analysis of empty code."""
    results = security_analyzer.analyze("", "empty.py")
    assert results['summary']['score'] == 100.0
    assert not security_analyzer._temp_manager.temp_dir.exists()

def test_simple_code_analysis(security_analyzer):
    """Test analysis of simple code."""
    results = security_analyzer.analyze("print('Hello')", "simple.py")
    assert results['summary']['score'] == 100.0
    assert not security_analyzer._temp_manager.temp_dir.exists()
