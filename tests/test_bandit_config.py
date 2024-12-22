"""Tests pour la configuration de Bandit."""
import pytest
from AuditronAI.core.bandit_config import (
    get_bandit_config,
    BanditProfile,
    ScanLevel
)


@pytest.fixture
def default_profile():
    """Retourne le profil par défaut."""
    return BanditProfile.default()


def test_scan_level_enum():
    """Test les valeurs de l'énumération ScanLevel."""
    assert ScanLevel.LOW.value == 'low'
    assert ScanLevel.MEDIUM.value == 'medium'
    assert ScanLevel.HIGH.value == 'high'


def test_default_profile(default_profile):
    """Test le profil par défaut."""
    assert default_profile.name == 'default'
    assert len(default_profile.tests) > 0
    assert default_profile.confidence_threshold == 0.8
    assert default_profile.severity_threshold == ScanLevel.HIGH


def test_bandit_config_basic():
    """Test la configuration de base de Bandit."""
    config = get_bandit_config('high', 0.8, 100)
    assert config['level'] == 'HIGH'
    assert config['confidence'] == 8
    assert not config['recursive']
    assert config['output_format'] == 'json'


def test_bandit_config_with_profile():
    """Test la configuration avec un profil spécifique."""
    config = get_bandit_config('medium', 0.8, 100, profile='custom')
    assert config['profile'] == 'custom'


def test_bandit_config_with_tests():
    """Test la configuration avec des tests spécifiques."""
    tests = ['B102', 'B103', 'B104']
    config = get_bandit_config('high', 0.8, 100, tests=tests)
    assert config['tests'] == tests


@pytest.mark.parametrize("invalid_level", ['invalid', '', 'CRITICAL', None])
def test_invalid_scan_level(invalid_level):
    """Test les niveaux de scan invalides."""
    with pytest.raises(ValueError) as exc:
        get_bandit_config(invalid_level, 0.8, 100)
    assert "Niveau de scan invalide" in str(exc.value)


@pytest.mark.parametrize("invalid_confidence", [-0.1, 1.1, 2.0, None])
def test_invalid_confidence(invalid_confidence):
    """Test les niveaux de confiance invalides."""
    with pytest.raises(ValueError) as exc:
        get_bandit_config('high', invalid_confidence, 100)
    assert "niveau de confiance" in str(exc.value)


@pytest.mark.parametrize("invalid_issues", [0, -1, -100])
def test_invalid_max_issues(invalid_issues):
    """Test les nombres de problèmes invalides."""
    with pytest.raises(ValueError) as exc:
        get_bandit_config('high', 0.8, invalid_issues)
    assert "maximum de problèmes" in str(exc.value)


def test_clean_test_list():
    """Test le nettoyage de la liste des tests."""
    tests = [' B102 ', 'B103', ' ', 'B104 ']
    config = get_bandit_config('high', 0.8, 100, tests=tests)
    assert config['tests'] == ['B102', 'B103', 'B104']


def test_config_immutability():
    """Test l'immutabilité de la configuration."""
    config1 = get_bandit_config('high', 0.8, 100)
    config2 = get_bandit_config('high', 0.8, 100)
    
    # Les configurations doivent être indépendantes
    config1['level'] = 'MODIFIED'
    assert config2['level'] == 'HIGH'