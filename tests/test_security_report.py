"""Tests pour le module de rapport de sécurité."""
import pytest
from unittest.mock import MagicMock, patch
import streamlit as st
from AuditronAI.app.security_report import (
    validate_results,
    show_security_report,
    show_metrics,
    show_grade
)

@pytest.fixture
def mock_streamlit():
    """Mock des fonctions Streamlit."""
    with patch('streamlit.markdown') as mock_md, \
         patch('streamlit.columns') as mock_cols, \
         patch('streamlit.metric') as mock_metric:
        yield {
            'markdown': mock_md,
            'columns': mock_cols,
            'metric': mock_metric
        }

@pytest.fixture
def valid_results():
    """Fixture pour des résultats valides."""
    return {
        'file': 'test.py',
        'explanation': '# Test Results',
        'security_issues': [],
        'code_quality': {
            'complexity': 5.0,
            'functions': []
        },
        'summary': {
            'severity_counts': {'critical': 0, 'high': 1, 'medium': 2, 'low': 3},
            'total_issues': 6,
            'score': 85.5,
            'details': 'Test details'
        }
    }

def test_validate_results_valid(valid_results):
    """Test la validation avec des résultats valides."""
    assert validate_results(valid_results) is True

def test_validate_results_invalid():
    """Test la validation avec des résultats invalides."""
    invalid_results = {
        'file': 'test.py',
        'security_issues': []
        # Manque code_quality et summary
    }
    assert validate_results(invalid_results) is False