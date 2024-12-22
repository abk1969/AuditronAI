"""Tests pour l'analyse des fichiers TypeScript."""
import pytest
from AuditronAI.core.analyzers.typescript_analyzer import TypeScriptAnalyzer
from AuditronAI.core.config.analyzer_config import AnalyzerConfig

@pytest.fixture
def analyzer():
    """Fixture pour l'analyseur TypeScript."""
    return TypeScriptAnalyzer(AnalyzerConfig())

def test_typescript_security_analysis(analyzer):
    """Test de l'analyse de sécurité TypeScript."""
    code = """
    function unsafeCode() {
        const userInput = "malicious code";
        eval(userInput);  // Problème de sécurité
        
        const password = "secret123";  // Donnée sensible
        
        document.write(userInput);  // Vulnérabilité XSS
        
        const cmd = "rm -rf /";
        exec(cmd);  // Injection de commande
    }
    """
    
    results = analyzer.analyze(code, "test.ts")
    
    # Vérifier la présence des résultats
    assert results is not None
    assert 'security_issues' in results
    assert isinstance(results['security_issues'], list)
    
    # Vérifier la détection des problèmes de sécurité
    security_issues = results['security_issues']
    issue_types = {issue['type'] for issue in security_issues}
    
    assert 'eval_usage' in issue_types
    assert 'sensitive_data' in issue_types
    assert 'xss_vulnerable' in issue_types
    assert 'command_injection' in issue_types

def test_typescript_quality_analysis(analyzer):
    """Test de l'analyse de qualité TypeScript."""
    code = """
    function complexFunction(): any {  // Type 'any' utilisé
        let unusedVar = 42;  // Variable non utilisée
        
        // TODO: Refactorer cette partie
        if (someCondition && anotherCondition && yetAnotherCondition && 
            evenMoreConditions && stillMoreConditions) {  // Condition complexe
            console.log("Debug info");  // Console.log en production
            
            try {
                riskyOperation();
            } catch (e) {}  // Catch bloc vide
        }
        
        const magicNumber = 123456;  // Nombre magique
        
        return callback1(function(err1) {
            return callback2(function(err2) {
                return callback3(function(err3) {  // Callbacks imbriqués
                    // Code
                });
            });
        });
    }
    """
    
    results = analyzer.analyze(code, "test.ts")
    
    # Vérifier la présence des résultats
    assert results is not None
    assert 'quality_issues' in results
    assert isinstance(results['quality_issues'], list)
    
    # Vérifier la détection des problèmes de qualité
    quality_issues = results['quality_issues']
    issue_types = {issue['type'] for issue in quality_issues}
    
    assert 'any_type' in issue_types
    assert 'console_log' in issue_types
    assert 'empty_catch' in issue_types
    assert 'magic_numbers' in issue_types
    assert 'complex_condition' in issue_types
    assert 'nested_callbacks' in issue_types
    assert 'todo_comment' in issue_types

def test_typescript_complexity_analysis(analyzer):
    """Test de l'analyse de complexité TypeScript."""
    code = """
    function complexFunction() {
        if (condition1) {
            for (let i = 0; i < 10; i++) {
                while (condition2) {
                    switch (value) {
                        case 1:
                            // Code
                            break;
                        case 2:
                            // Code
                            break;
                    }
                }
            }
        }
    }
    
    function simpleFunction() {
        return true;
    }
    """
    
    results = analyzer.analyze(code, "test.ts")
    
    # Vérifier les scores de complexité et maintenabilité
    assert 'complexity_score' in results
    assert isinstance(results['complexity_score'], (int, float))
    assert results['complexity_score'] > 0
    
    assert 'maintainability_score' in results
    assert isinstance(results['maintainability_score'], (int, float))
    assert 0 <= results['maintainability_score'] <= 100

def test_typescript_error_handling(analyzer):
    """Test de la gestion des erreurs."""
    # Test avec du code vide
    results = analyzer.analyze("", "empty.ts")
    assert results.get('error') is not None
    
    # Test avec un fichier non TypeScript
    results = analyzer.analyze("var x = 1;", "test.js")
    assert results.get('error') is not None
    
    # Test avec du code invalide
    invalid_code = """
    function broken {
        const x =
        if () {
    }
    """
    results = analyzer.analyze(invalid_code, "broken.ts")
    assert results.get('error') is not None
