"""Example d'utilisation des analyseurs de code."""
import asyncio
import json
from pathlib import Path
from typing import Dict, Any, List

from AuditronAI.core.analyzers.interfaces import AnalyzerType
from AuditronAI.core.analyzers.factory import AnalyzerFactory
from AuditronAI.core.logger import logger
from AuditronAI.core.error_handling import SecurityError

async def analyze_code(code: str, filename: str, language: str) -> Dict[str, Any]:
    """
    Analyse un fichier de code avec tous les analyseurs appropriés.
    
    Args:
        code: Code source à analyser
        filename: Nom du fichier
        language: Langage du code
        
    Returns:
        Dict contenant les résultats d'analyse
    """
    # Contexte d'analyse
    context = {
        'code': code,
        'filename': filename,
        'language': language,
        'config': {
            'max_line_length': 100,
            'strict': True,
            'debug': False
        }
    }
    
    # Sélectionner les analyseurs appropriés selon le langage
    analyzer_types = get_analyzers_for_language(language)
    
    try:
        # Créer les analyseurs
        analyzers = await AnalyzerFactory.create_analyzers(analyzer_types, context)
        
        # Exécuter les analyses
        results = {}
        for analyzer in analyzers:
            analyzer_results = await analyzer.analyze()
            results[analyzer.analyzer_type.name] = analyzer_results
            
        return results
        
    except SecurityError as e:
        logger.error(f"Erreur lors de l'analyse: {str(e)}")
        return {
            'error': True,
            'message': str(e)
        }

def get_analyzers_for_language(language: str) -> List[AnalyzerType]:
    """
    Détermine les analyseurs à utiliser selon le langage.
    
    Args:
        language: Langage du code
        
    Returns:
        Liste des types d'analyseurs à utiliser
    """
    # Analyseurs communs à tous les langages
    analyzers = [
        AnalyzerType.SCRIPT,
        AnalyzerType.UNUSED,
        AnalyzerType.QUALITY,
        AnalyzerType.COMPLEXITY
    ]
    
    # Analyseurs spécifiques au langage
    if language.lower() == 'python':
        analyzers.append(AnalyzerType.SECURITY)
    elif language.lower() == 'typescript':
        analyzers.append(AnalyzerType.TYPESCRIPT)
    elif language.lower() == 'sql':
        analyzers.append(AnalyzerType.SQL)
        
    return analyzers

def format_results(results: Dict[str, Any], output_file: str = None) -> None:
    """
    Formate et affiche les résultats d'analyse.
    
    Args:
        results: Résultats d'analyse
        output_file: Fichier de sortie optionnel
    """
    # Formater les résultats
    formatted = {
        'summary': {
            'total_issues': 0,
            'by_severity': {},
            'by_type': {}
        },
        'details': results
    }
    
    # Calculer les statistiques
    for analyzer_type, analyzer_results in results.items():
        if isinstance(analyzer_results, dict):
            # Compter les problèmes
            issues = analyzer_results.get('security_issues', [])
            issues.extend(analyzer_results.get('issues', []))
            
            formatted['summary']['total_issues'] += len(issues)
            
            # Grouper par sévérité
            for issue in issues:
                severity = issue.get('severity', 'unknown')
                formatted['summary']['by_severity'][severity] = \
                    formatted['summary']['by_severity'].get(severity, 0) + 1
                    
            # Grouper par type
            formatted['summary']['by_type'][analyzer_type] = len(issues)
    
    # Afficher ou sauvegarder les résultats
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(formatted, f, indent=2)
    else:
        print(json.dumps(formatted, indent=2))

async def main():
    """Point d'entrée principal."""
    # Exemple Python
    python_code = '''
def insecure_function(user_input):
    """Fonction avec des problèmes de sécurité."""
    # Exécution non sécurisée
    exec(user_input)
    
    # Mot de passe en dur
    password = "secret123"
    
    # SQL injection possible
    query = f"SELECT * FROM users WHERE id = {user_input}"
    
    return query
'''

    # Exemple TypeScript
    typescript_code = '''
function processData(data: any): void {
    // Évaluation non sécurisée
    eval(data);
    
    // Type any utilisé
    let result: any = {};
    
    // Injection possible
    document.innerHTML = data;
}
'''

    # Exemple SQL
    sql_code = '''
-- Requête non sécurisée
SELECT * FROM users 
WHERE username LIKE '%' + @input + '%'
ORDER BY id;

-- Suppression sans WHERE
DELETE FROM logs;
'''

    # Analyser chaque exemple
    print("Analyse du code Python...")
    python_results = await analyze_code(python_code, 'example.py', 'python')
    format_results(python_results, 'python_analysis.json')
    
    print("\nAnalyse du code TypeScript...")
    ts_results = await analyze_code(typescript_code, 'example.ts', 'typescript')
    format_results(ts_results, 'typescript_analysis.json')
    
    print("\nAnalyse du code SQL...")
    sql_results = await analyze_code(sql_code, 'example.sql', 'sql')
    format_results(sql_results, 'sql_analysis.json')

if __name__ == '__main__':
    asyncio.run(main())
