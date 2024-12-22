import pytest
from AuditronAI.core.security_analyzer import SecurityAnalyzer

def test_exec_security_issue(security_analyzer):
    """Test detection of exec security issue."""
    code = "exec(user_input)"
    results = security_analyzer.analyze(code, "exec_test.py")
    assert results['summary']['score'] < 100.0
    assert any('B102' in str(issue) for issue in results['security_issues'])

def test_hardcoded_password(security_analyzer):
    """Test detection of hardcoded password."""
    code = "password = 'secret123'"
    results = security_analyzer.analyze(code, "password_test.py")
    assert results['summary']['score'] < 100.0
    assert any('B105' in str(issue) for issue in results['security_issues'])

def test_eval_security_issue(security_analyzer):
    """Test detection of eval security issue."""
    code = "eval(user_input)"
    results = security_analyzer.analyze(code, "eval_test.py")
    assert results['summary']['score'] < 100.0
    assert any('B307' in str(issue) for issue in results['security_issues'])
