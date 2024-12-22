from AuditronAI.core.custom_dataset import CustomDataset
from AuditronAI.core.security_analyzer import SecurityAnalyzer
from AuditronAI.core.logger import logger
import os

def analyze_code(code: str, filename: str = "code.py", history=None, usage_stats=None) -> dict:
    """Analyse un code Python donné."""
    try:
        # Analyse IA
        dataset = CustomDataset("streamlit_analysis")
        result = dataset.generate_completion("project_analysis", {
            "file_path": filename,
            "code": code
        })
        
        # Analyse de sécurité
        security_analyzer = SecurityAnalyzer()
        security_results = security_analyzer.analyze(code, filename)
        
        # Statistiques de base
        lines = code.split('\n')
        stats = {
            'Lignes de code': len(lines),
            'Caractères': len(code),
            'Fonctions': len([l for l in lines if l.strip().startswith('def ')]),
            'Classes': len([l for l in lines if l.strip().startswith('class ')])
        }
        
        analysis_result = {
            "file": filename,
            "code": code,
            "analysis": result,
            "stats": stats,
            "security": security_results
        }
        
        # Enregistrer dans l'historique si fourni
        if history:
            history.add_entry(analysis_result)
        
        # Enregistrer les stats si fournies
        if usage_stats:
            usage_stats.record_analysis(os.getenv('AI_SERVICE', 'openai'))
        
        logger.info(f"Analyse réussie pour {filename}")
        return analysis_result
        
    except Exception as e:
        logger.error(f"Erreur lors de l'analyse: {str(e)}")
        if usage_stats:
            usage_stats.record_error()
        raise 