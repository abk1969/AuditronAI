"""Tests pour l'analyseur SQL."""
import pytest
from AuditronAI.core.analyzers.sql_analyzer import SQLAnalyzer
from AuditronAI.core.config.analyzer_config import AnalyzerConfig

@pytest.fixture
def sql_analyzer():
    """Fixture pour créer un analyseur SQL."""
    config = AnalyzerConfig()
    return SQLAnalyzer(config)

def test_sql_security_analysis(sql_analyzer):
    """Teste l'analyse de sécurité SQL."""
    code = """
    EXECUTE 'SELECT * FROM users WHERE id = ' || user_id;
    GRANT ALL PRIVILEGES ON database_name TO user;
    """
    
    result = sql_analyzer.analyze(code)
    security_analysis = result["analyses"]["sqlsecurity"]
    
    assert len(security_analysis["security_issues"]) == 2
    assert security_analysis["risk_level"] == "high"
    assert any("EXECUTE" in issue["message"] for issue in security_analysis["security_issues"])
    assert any("privilégiée" in issue["message"] for issue in security_analysis["security_issues"])

def test_sql_performance_analysis(sql_analyzer):
    """Teste l'analyse de performance SQL."""
    code = """
    SELECT * FROM table1
    JOIN table2;
    """
    
    result = sql_analyzer.analyze(code)
    performance_analysis = result["analyses"]["sqlperformance"]
    
    assert len(performance_analysis["performance_issues"]) == 2
    assert performance_analysis["optimization_needed"] is True
    assert any("SELECT *" in issue["message"] for issue in performance_analysis["performance_issues"])
    assert any("Jointure sans condition" in issue["message"] for issue in performance_analysis["performance_issues"])

def test_sql_quality_analysis(sql_analyzer):
    """Teste l'analyse de qualité SQL."""
    code = """
    select * from users
    where id = 1;
    """
    
    result = sql_analyzer.analyze(code)
    quality_analysis = result["analyses"]["sqlquality"]
    
    assert len(quality_analysis["quality_issues"]) > 0
    assert "quality_score" in quality_analysis
    assert any("commentaires" in issue["message"] for issue in quality_analysis["quality_issues"])

def test_empty_code_analysis(sql_analyzer):
    """Teste l'analyse de code SQL vide."""
    result = sql_analyzer.analyze("")
    assert "issues" in result
    assert len(result["issues"]) == 0
    assert result["error"] is None

def test_overall_score_calculation(sql_analyzer):
    """Teste le calcul du score global."""
    code = """
    -- Requête avec plusieurs problèmes
    EXECUTE 'SELECT * FROM users';
    """
    
    result = sql_analyzer.analyze(code)
    assert "overall_score" in result
    assert isinstance(result["overall_score"], (int, float))
    assert 0 <= result["overall_score"] <= 100
