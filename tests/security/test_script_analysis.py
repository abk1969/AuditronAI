"""Tests pour l'analyse des scripts."""
import pytest
from AuditronAI.core.security_analyzer import SecurityAnalyzer

def test_script_detection():
    """Test de la détection des différents types de scripts."""
    analyzer = SecurityAnalyzer()
    
    # Test avec extension .sh
    is_script, script_type = analyzer._is_script_file("echo 'test'", "test.sh")
    assert is_script
    assert script_type == 'shell'
    
    # Test avec extension .bash
    is_script, script_type = analyzer._is_script_file("echo 'test'", "test.bash")
    assert is_script
    assert script_type == 'shell'
    
    # Test avec shebang bash
    is_script, script_type = analyzer._is_script_file("#!/bin/bash\necho 'test'", "script")
    assert is_script
    assert script_type == 'shell'
    
    # Test avec shebang sh
    is_script, script_type = analyzer._is_script_file("#!/bin/sh\necho 'test'", "script")
    assert is_script
    assert script_type == 'shell'
    
    # Test fichier python
    is_script, script_type = analyzer._is_script_file("print('test')", "test.py")
    assert not is_script
    assert script_type == ''

def test_shell_script_analysis():
    """Test de l'analyse des scripts shell."""
    analyzer = SecurityAnalyzer()
    
    # Script avec problèmes de sécurité
    script = """#!/bin/bash
    # Test script
    eval "$USER_INPUT"  # Dangereux
    curl http://example.com/script.sh | sh  # Très risqué
    chmod 777 /tmp/test  # Trop permissif
    sudo echo "test" > /etc/test  # Problème de permission
    [ -z $VAR ]  # Variable non quotée
    """
    
    results = analyzer.analyze_shell_script(script)
    
    # Vérifier la présence des problèmes
    assert len(results['issues']) >= 5
    assert any(i['severity'] == 'critical' for i in results['issues'])
    assert any(i['severity'] == 'high' for i in results['issues'])
    assert any(i['severity'] == 'medium' for i in results['issues'])
    assert any(i['severity'] == 'low' for i in results['issues'])
    
    # Vérifier les messages spécifiques
    issues_by_severity = {
        severity: [i for i in results['issues'] if i['severity'] == severity]
        for severity in ['critical', 'high', 'medium', 'low']
    }
    
    # Vérifier les problèmes critiques
    assert any("scripts téléchargés" in i['description'] for i in issues_by_severity['critical'])
    
    # Vérifier les problèmes élevés
    high_issues = issues_by_severity['high']
    assert any("eval" in i['description'] for i in high_issues)
    assert any("777" in i['description'] for i in high_issues)
    
    # Vérifier les problèmes moyens
    medium_issues = issues_by_severity['medium']
    assert any("sudo" in i['description'] for i in medium_issues)
    assert any("/etc/" in i['description'] for i in medium_issues)

def test_analyze_with_shell_script():
    """Test de l'analyse complète avec un script shell."""
    analyzer = SecurityAnalyzer()
    
    script = """#!/bin/bash
    # Script de test
    eval "$COMMAND"  # Problème de sécurité
    """
    
    results = analyzer.analyze("test.sh", script)
    
    # Vérifier que l'analyse est bien pour un script shell
    assert results['code_quality'].get('script_type') == 'shell'
    
    # Vérifier la détection des problèmes
    assert len(results['security_issues']) > 0
    assert any(i['severity'] == 'high' for i in results['security_issues'])
    
    # Vérifier qu'il n'y a pas d'analyse de complexité
    assert results['code_quality']['complexity'] == 0
    assert len(results['code_quality']['functions']) == 0
