"""Tests pour le client Azure."""
import pytest
from unittest.mock import patch, MagicMock
from PromptWizard.core.azure_client import OpenAIClient

@pytest.fixture
def mock_openai():
    with patch('PromptWizard.core.azure_client.OpenAI') as mock:
        yield mock

def test_client_initialization(mock_openai):
    """Test l'initialisation du client."""
    client = OpenAIClient()
    assert client.client is not None

@pytest.mark.integration
def test_generate_completion():
    """Test la génération de complétion."""
    client = OpenAIClient()
    response = client.generate_completion("Dis bonjour")
    assert isinstance(response, str)
    assert len(response) > 0