import pytest
from AuditronAI.core.security_analyzer import SecurityAnalyzer

def test_syntax_error(security_analyzer):
    """Test handling of Python syntax errors."""
    code = "def invalid_python(:"
    results = security_analyzer.analyze(code, "syntax_error.py")
    assert 'error' not in results
    assert results['summary']['score'] == 0.0
    assert not security_analyzer._temp_manager.temp_dir.exists()

def test_empty_input(security_analyzer):
    """Test handling of empty input."""
    results = security_analyzer.analyze("", "empty.py")
    assert 'error' not in results
    assert results['summary']['score'] == 100.0
    assert not security_analyzer._temp_manager.temp_dir.exists()

def test_large_file(security_analyzer):
    """Test handling of large files."""
    large_code = "x = 1\n" * 1000  # Reasonable size for testing
    results = security_analyzer.analyze(large_code, "large_file.py")
    assert 'security_issues' in results
    assert not security_analyzer._temp_manager.temp_dir.exists()

def test_concurrent_analysis(security_analyzer):
    """Test concurrent analysis of multiple small files."""
    codes = ["x = 1", "y = 2", "z = 3"]
    for i, code in enumerate(codes):
        results = security_analyzer.analyze(code, f"test_{i}.py")
        assert 'security_issues' in results
        assert not security_analyzer._temp_manager.temp_dir.exists()
