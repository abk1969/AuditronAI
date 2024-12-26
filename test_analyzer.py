import asyncio
from AuditronAI.core.security_analyzer import SecurityAnalyzer

async def test_analyzer():
    # Créer une instance de l'analyseur
    analyzer = SecurityAnalyzer()
    
    # Lire le fichier de test
    with open('test_security.py', 'r') as f:
        code = f.read()
    
    # Analyser le code
    results = await analyzer.analyze(code, 'test_security.py')
    
    # Afficher les résultats
    print("\nRésultats de l'analyse de sécurité :")
    print("-" * 50)
    
    # Afficher les problèmes de sécurité
    print("\nProblèmes de sécurité détectés :")
    for issue in results.security_issues:
        print(f"\nType: {issue.type}")
        print(f"Sévérité: {issue.severity}")
        print(f"Message: {issue.message}")
        print(f"Ligne: {issue.line}")
        print(f"Code: {issue.code}")
    
    # Afficher le score
    print(f"\nScore de sécurité: {results.summary.get('score', 0)}/100")
    print(f"Total des problèmes: {results.summary.get('total_issues', 0)}")

if __name__ == "__main__":
    asyncio.run(test_analyzer())
