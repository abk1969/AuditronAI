import pytest
from AuditronAI.core.prompt_manager import PromptManager

def test_prompt_manager_initialization():
    manager = PromptManager()
    assert manager.default_config is not None
    assert 'temperature' in manager.default_config

def test_get_prompt():
    manager = PromptManager()
    prompt = manager.get_prompt('code_review', code="def hello(): pass")
    assert 'system' in prompt
    assert 'expert en revue de code' in prompt['system']
    assert 'def hello(): pass' in prompt['user']

def test_invalid_prompt():
    manager = PromptManager()
    with pytest.raises(ValueError):
        manager.get_prompt('non_existant_prompt') 