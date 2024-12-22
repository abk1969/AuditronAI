"""Example d'utilisation de l'analyseur SQL."""
from AuditronAI.core.services.code_analyzer_service import CodeAnalyzerService
from AuditronAI.core.services.analysis_plugins.sql_plugin import SQLAnalysisPlugin

def main():
    """Démontre l'utilisation de l'analyseur SQL."""
    
    # Initialise le service d'analyse
    analyzer_service = CodeAnalyzerService()
    
    # Enregistre le plugin SQL
    analyzer_service.register_plugin("sql", SQLAnalysisPlugin)
    
    # Example de code SQL à analyser
    sql_code = """
    -- Cette requête nécessite une optimisation
    SELECT * FROM users u
    JOIN orders o
    WHERE u.status = 'active';
    
    -- Opération sensible
    GRANT ALL PRIVILEGES ON database_name TO user;
    """
    
    # Analyse le code
    results = analyzer_service.analyze(sql_code, "example.sql")
    
    # Affiche les résultats
    print("\nRésultats de l'analyse SQL:")
    print("-" * 50)
    
    if "sql" in results:
        analyses = results["sql"]["analyses"]
        
        # Affiche les problèmes de sécurité
        if "sqlsecurity" in analyses:
            security = analyses["sqlsecurity"]
            print("\nProblèmes de sécurité:")
            for issue in security.get("security_issues", []):
                print(f"- {issue['message']} (Sévérité: {issue['severity']})")
                
        # Affiche les problèmes de performance
        if "sqlperformance" in analyses:
            performance = analyses["sqlperformance"]
            print("\nProblèmes de performance:")
            for issue in performance.get("performance_issues", []):
                print(f"- {issue['message']} (Sévérité: {issue['severity']})")
                
        # Affiche les problèmes de qualité
        if "sqlquality" in analyses:
            quality = analyses["sqlquality"]
            print("\nProblèmes de qualité:")
            for issue in quality.get("quality_issues", []):
                print(f"- {issue['message']} (Sévérité: {issue['severity']})")
            print(f"\nScore de qualité: {quality.get('quality_score', 0)}/100")
            
        # Affiche le score global
        if "overall_score" in results["sql"]:
            print(f"\nScore global: {results['sql']['overall_score']}/100")
    
if __name__ == "__main__":
    main()
