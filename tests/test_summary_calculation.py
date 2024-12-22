"""Tests pour le calcul des résumés et des scores."""
import pytest
from AuditronAI.core.security_analyzer import SecurityAnalyzer

@pytest.fixture
def analyzer():
    """Fixture pour l'analyseur de sécurité."""
    return SecurityAnalyzer()

@pytest.fixture
def sample_results():
    """Fixture pour des résultats d'analyse."""
    return {
        'security_issues': [
            {'severity': 'HIGH', 'test_name': 'test1'},
            {'severity': 'HIGH', 'test_name': 'test2'},
            {'severity': 'MEDIUM', 'test_name': 'test3'},
            {'severity': 'LOW', 'test_name': 'test4'},
        ],
        'code_quality': {
            'complexity': 12.0,
            'functions': [{'name': 'test', 'complexity': 12}]
        }
    }

def test_severity_counting(analyzer, sample_results):
    """Test le comptage des sévérités."""
    summary = analyzer._calculate_summary(sample_results)
    assert summary['severity_counts']['high'] == 2
    assert summary['severity_counts']['medium'] == 1
    assert summary['severity_counts']['low'] == 1
    assert summary['total_issues'] == 4

def test_score_calculation(analyzer, sample_results):
    """Test le calcul du score."""
    summary = analyzer._calculate_summary(sample_results)
    assert 0 <= summary['score'] <= 100
    assert isinstance(summary['score'], float)

def test_complexity_penalty(analyzer):
    """Test la pénalité de complexité."""
    results = {
        'security_issues': [],
        'code_quality': {'complexity': 15.0}
    }
    summary = analyzer._calculate_summary(results)
    assert summary['score'] < 100  # La complexité élevée devrait réduire le score

def test_summary_details(analyzer, sample_results):
    """Test la génération des détails du résumé."""
    summary = analyzer._calculate_summary(sample_results)
    details = summary['details']
    assert isinstance(details, str)
    assert "⚠️" in details  # Devrait contenir des avertissements
    assert "HIGH" in details  # Devrait mentionner les problèmes HIGH

def test_perfect_score(analyzer):
    """Test un code parfait sans problèmes."""
    results = {
        'security_issues': [],
        'code_quality': {
            'complexity': 5.0,  # Bien en dessous du seuil
            'functions': [{'name': 'test', 'complexity': 5}]
        }
    }
    summary = analyzer._calculate_summary(results)
    assert summary['score'] == 100.0
    assert "✅" in summary['details']
    assert "Aucun problème" in summary['details']

def test_critical_issues(analyzer):
    """Test avec des problèmes critiques."""
    results = {
        'security_issues': [
            {'severity': 'CRITICAL', 'test_name': 'critical_test'},
            {'severity': 'CRITICAL', 'test_name': 'critical_test2'}
        ],
        'code_quality': {'complexity': 8.0}
    }
    summary = analyzer._calculate_summary(results)
    assert summary['severity_counts']['critical'] == 2
    assert summary['score'] < 60  # Score fortement pénalisé

def test_threshold_handling(analyzer):
    """Test la gestion des seuils de sévérité."""
    # Modifier les seuils pour le test
    analyzer.severity_thresholds['high'] = 1
    
    results = {
        'security_issues': [
            {'severity': 'HIGH', 'test_name': 'test1'},
            {'severity': 'HIGH', 'test_name': 'test2'}  # Dépasse le seuil
        ],
        'code_quality': {'complexity': 7.0}
    }
    summary = analyzer._calculate_summary(results)
    details = summary['details']
    assert "seuil: 1" in details

def test_multiple_issues(analyzer):
    """Test avec plusieurs types de problèmes."""
    results = {
        'security_issues': [
            {'severity': 'HIGH', 'test_name': 'high_test'},
            {'severity': 'MEDIUM', 'test_name': 'medium_test'},
            {'severity': 'LOW', 'test_name': 'low_test'}
        ],
        'code_quality': {'complexity': 11.0}  # Dépasse le seuil
    }
    summary = analyzer._calculate_summary(results)
    details = summary['details']
    assert "Complexité" in details
    assert len(details.split('\n')) > 1  # Plusieurs lignes de détails