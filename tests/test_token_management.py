import pytest
from pathlib import Path
from PromptWizard.core.token_manager import TokenManager
from PromptWizard.core.security_analyzer import SecurityAnalyzer

def test_token_manager_initialization():
    """Teste l'initialisation du gestionnaire de tokens."""
    token_manager = TokenManager()
    assert token_manager.current_tokens == 0
    assert token_manager.config is not None

def test_code_chunking():
    """Teste le découpage du code en chunks."""
    token_manager = TokenManager()
    
    # Code de test avec plusieurs lignes
    test_code = "\n".join([f"line_{i}" for i in range(3000)])
    
    chunks = token_manager.split_code_into_chunks(test_code)
    assert len(chunks) > 1
    
    # Vérifier que la taille des chunks respecte la configuration
    max_size = token_manager.config['token_management']['code_chunking']['max_chunk_size']
    for chunk in chunks:
        assert len(chunk.split('\n')) <= max_size

def test_token_reduction():
    """Teste les stratégies de réduction de tokens."""
    token_manager = TokenManager()
    
    test_code = """
    # Commentaire à supprimer
    def test_function():
        '''Docstring à conserver'''
        # Autre commentaire
        print("Hello")  # Commentaire inline
    """
    
    optimized_code = token_manager.apply_token_reduction(test_code)
    assert len(optimized_code) < len(test_code)

def test_security_analyzer_with_token_management():
    """Teste l'intégration du gestionnaire de tokens dans l'analyseur de sécurité."""
    analyzer = SecurityAnalyzer()
    
    # Code de test volumineux
    test_code = """
    def vulnerable_function(user_input):
        '''Fonction avec des vulnérabilités pour le test'''
        # SQL Injection vulnerability
        query = f"SELECT * FROM users WHERE id = {user_input}"
        
        # Command injection vulnerability
        import os
        os.system(f"echo {user_input}")
        
        # Path traversal vulnerability
        with open(f"/tmp/{user_input}", "r") as f:
            data = f.read()
            
        return data
    """
    
    # Multiplier le code pour dépasser la limite de tokens
    large_code = test_code * 50
    
    results = analyzer.analyze(large_code)
    
    # Vérifier que l'analyse s'est bien déroulée
    assert 'error' not in results
    assert 'summary' in results
    assert results['summary']['severity_counts']['high'] > 0

def test_task_prioritization():
    """Teste la priorisation des tâches d'analyse."""
    token_manager = TokenManager()
    
    # Simuler l'utilisation de tokens
    token_manager.update_token_count(30000)
    
    # Obtenir la prochaine tâche
    task = token_manager.get_next_task()
    assert task is not None
    assert task['max_tokens'] + token_manager.current_tokens <= 80000

def test_error_handling():
    """Teste la gestion des erreurs."""
    analyzer = SecurityAnalyzer()
    
    # Tester avec un code vide
    results = analyzer.analyze("")
    assert 'error' in results
    assert "vide" in results['error'].lower()
    
    # Tester avec un code trop grand
    huge_code = "x = 1\n" * 1000000
    results = analyzer.analyze(huge_code)
    assert 'error' in results
    assert "volumineux" in results['error'].lower()

if __name__ == '__main__':
    pytest.main([__file__])
