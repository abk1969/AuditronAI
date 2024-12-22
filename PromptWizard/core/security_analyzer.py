import bandit
from bandit.core import manager
import safety
from pylint import lint
import json
import os
from pathlib import Path
from typing import Dict, List, Any
from .logger import logger
import streamlit as st
from datetime import datetime

class SecurityAnalyzer:
    def __init__(self):
        """Initialise l'analyseur de sécurité."""
        self.scan_level = os.getenv('SECURITY_SCAN_LEVEL', 'high')
        self.enable_deps = os.getenv('ENABLE_DEPENDENCY_CHECK', 'true').lower() == 'true'
        self.enable_static = os.getenv('ENABLE_STATIC_ANALYSIS', 'false').lower() == 'true'  # Disabled by default on Windows
        
        # Correction du parsing JSON
        default_checks = [
            "sql-injection",
            "xss",
            "code-injection",
            "command-injection",
            "path-traversal",
            "crypto-weak",
            "secrets-exposure",
            "auth-bypass",
            "unsafe-deserialization",
            "insecure-transport"
        ]
        try:
            self.security_checks = json.loads(os.getenv('SECURITY_CHECKS', json.dumps(default_checks)))
        except json.JSONDecodeError:
            logger.warning("Format JSON invalide pour SECURITY_CHECKS, utilisation des valeurs par défaut")
            self.security_checks = default_checks

        try:
            self.ignore_patterns = json.loads(os.getenv('SECURITY_IGNORE_PATTERNS', '["test_*.py", "*_test.py"]'))
        except json.JSONDecodeError:
            logger.warning("Format JSON invalide pour SECURITY_IGNORE_PATTERNS")
            self.ignore_patterns = ["test_*.py", "*_test.py"]
        
        # Récupérer les seuils depuis la session si disponibles
        if hasattr(st.session_state, 'security_config'):
            self.thresholds = {
                'critical': st.session_state.security_config['critical_threshold'],
                'high': st.session_state.security_config['high_threshold'],
                'medium': st.session_state.security_config['medium_threshold']
            }
        else:
            # Fallback sur les valeurs de .env
            self.thresholds = {
                'critical': int(os.getenv('CRITICAL_SEVERITY_THRESHOLD', 0)),
                'high': int(os.getenv('HIGH_SEVERITY_THRESHOLD', 2)),
                'medium': int(os.getenv('MEDIUM_SEVERITY_THRESHOLD', 5))
            }
        
        # Valider les seuils
        if not self.validate_thresholds():
            logger.warning("Utilisation des seuils par défaut")
            self.thresholds = {
                'critical': 0,
                'high': 2,
                'medium': 5
            }
        
        # Nouveaux paramètres
        self.timeout = int(os.getenv('SECURITY_TIMEOUT', 30))
        self.max_issues = int(os.getenv('SECURITY_MAX_ISSUES', 100))
        self.min_confidence = float(os.getenv('SECURITY_MIN_CONFIDENCE', 0.8))
    
    def validate_thresholds(self) -> bool:
        """Valide les seuils de sécurité."""
        # Vérifier les valeurs négatives
        for level, value in self.thresholds.items():
            if value < 0:
                logger.warning(f"Seuil {level} invalide: {value} (doit être ≥ 0)")
                return False
        
        # Vérifier la cohérence des seuils
        if self.thresholds['critical'] > self.thresholds['high']:
            logger.warning("Le seuil critique ne peut pas être supérieur au seuil élevé")
            return False
        
        if self.thresholds['high'] > self.thresholds['medium']:
            logger.warning("Le seuil élevé ne peut pas être supérieur au seuil moyen")
            return False
        
        return True
    
    def run_bandit_analysis(self, code: str, filename: str) -> Dict[str, Any]:
        """Exécute l'analyse Bandit."""
        try:
            # Écrire le code dans un fichier temporaire
            temp_file = Path('temp_analysis.py')
            temp_file.write_text(code)
            
            # Configurer Bandit
            b_mgr = manager.BanditManager()
            b_mgr.discover_files([str(temp_file)])
            b_mgr.run_tests()
            
            # Récupérer les résultats
            results = {
                'issues': b_mgr.get_issue_list(),
                'metrics': b_mgr.metrics.data
            }
            
            # Nettoyer
            temp_file.unlink()
            
            return results
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse Bandit: {str(e)}")
            return {'error': str(e)}
    
    def run_safety_check(self, requirements_file: str = None) -> Dict[str, Any]:
        """Vérifie les dépendances avec Safety."""
        try:
            if not self.enable_deps:
                return {}
            
            if requirements_file and Path(requirements_file).exists():
                check = safety.check(requirement_files=[requirements_file])
            else:
                check = safety.check()
            
            return {
                'vulnerabilities': check.vulnerabilities,
                'packages_checked': check.packages_checked
            }
        except Exception as e:
            logger.error(f"Erreur lors de la vérification Safety: {str(e)}")
            return {'error': str(e)}
    
    def run_semgrep_analysis(self, code: str) -> Dict[str, Any]:
        """Semgrep analysis is not available on Windows."""
        logger.info("Semgrep analysis skipped - not available on Windows")
        return {}
    
    def run_pylint_security(self, code: str) -> Dict[str, Any]:
        """Exécute l'analyse de sécurité Pylint."""
        try:
            # Écrire le code dans un fichier temporaire
            temp_file = Path('temp_pylint.py')
            temp_file.write_text(code)
            
            # Options Pylint pour la sécurité
            options = [
                str(temp_file),
                '--disable=all',
                '--enable=security',
                '--output-format=json'
            ]
            
            # Exécuter Pylint avec la nouvelle API
            reporter = lint.Run(options, do_exit=False)
            results = reporter.linter.report_data
            
            # Nettoyer
            temp_file.unlink()
            
            return results
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse Pylint: {str(e)}")
            return {'error': str(e)}
    
    def analyze(self, code: str, filename: str = "code.py") -> Dict[str, Any]:
        """Exécute l'analyse de sécurité complète."""
        try:
            start_time = datetime.now()
            logger.info(f"Démarrage de l'analyse de sécurité pour {filename}")
            
            # Vérifications préliminaires
            if not code or not code.strip():
                return {
                    'error': "Le code à analyser est vide",
                    'summary': {
                        'severity_counts': {'critical': 0, 'high': 0, 'medium': 0, 'low': 0},
                        'thresholds_exceeded': {},
                        'recommendations': []
                    }
                }
            
            max_size = int(str(os.getenv('MAX_FILE_SIZE', '500000')).split('#')[0].strip())
            if len(code) > max_size:
                return {
                    'error': f"Fichier trop volumineux (max: {max_size} bytes)",
                    'summary': {
                        'severity_counts': {'critical': 0, 'high': 0, 'medium': 0, 'low': 0},
                        'thresholds_exceeded': {},
                        'recommendations': []
                    }
                }
            
            # Analyse complète
            results = {
                'bandit': self.run_bandit_analysis(code, filename),
                'safety': self.run_safety_check() if self.enable_deps else {},
                'semgrep': self.run_semgrep_analysis(code) if self.enable_static else {},
                'pylint': self.run_pylint_security(code)
            }
            
            # Vérifier le timeout
            if (datetime.now() - start_time).seconds > self.timeout:
                raise TimeoutError(f"L'analyse a dépassé le délai de {self.timeout} secondes")
            
            # Filtrer les résultats selon la confiance
            for tool, tool_results in results.items():
                if isinstance(tool_results, dict) and 'issues' in tool_results:
                    tool_results['issues'] = [
                        issue for issue in tool_results['issues']
                        if issue.get('confidence', 0) >= self.min_confidence
                    ][:self.max_issues]
            
            # Vérifier si des erreurs sont présentes dans les résultats
            for tool, tool_results in results.items():
                if isinstance(tool_results, dict) and 'error' in tool_results:
                    return {
                        'error': f"Erreur dans l'analyse {tool}: {tool_results['error']}",
                        'summary': {
                            'severity_counts': {'critical': 0, 'high': 0, 'medium': 0, 'low': 0},
                            'thresholds_exceeded': {},
                            'recommendations': []
                        }
                    }
            
            # Agréger les résultats
            severity_counts = {
                'critical': 0,
                'high': 0,
                'medium': 0,
                'low': 0
            }
            
            # Compter les problèmes par sévérité
            for tool, tool_results in results.items():
                if isinstance(tool_results, dict) and 'issues' in tool_results:
                    for issue in tool_results['issues']:
                        severity = issue.get('severity', 'low').lower()
                        severity_counts[severity] += 1
            
            # Vérifier les seuils
            thresholds_exceeded = {}
            for level, count in severity_counts.items():
                if level in self.thresholds:
                    exceeded = count > self.thresholds[level]
                    thresholds_exceeded[level] = exceeded
                    if exceeded:
                        logger.warning(f"Seuil {level} dépassé: {count} > {self.thresholds[level]}")
            
            # Ajouter les recommandations
            recommendations = []
            if severity_counts['critical'] > 0:
                recommendations.append({
                    'level': 'critical',
                    'message': "⚠️ Vulnérabilités critiques détectées - Action immédiate requise",
                    'details': "Ces vulnérabilités représentent un risque majeur de sécurité"
                })
            if severity_counts['high'] > 0:
                recommendations.append({
                    'level': 'high',
                    'message': "🔴 Vulnérabilités importantes trouvées",
                    'details': "Ces problèmes doivent être corrigés rapidement"
                })
            
            results['summary'] = {
                'severity_counts': severity_counts,
                'thresholds_exceeded': thresholds_exceeded,
                'recommendations': recommendations,
                'scan_info': {
                    'timestamp': datetime.now().isoformat(),
                    'filename': filename,
                    'scan_level': self.scan_level,
                    'tools_used': list(results.keys())
                }
            }
            
            logger.info(f"Analyse de sécurité terminée pour {filename}")
            return results
            
        except Exception as e:
            error_msg = f"Erreur lors de l'analyse de sécurité: {str(e)}"
            logger.error(error_msg)
            return {
                'error': error_msg,
                'summary': {
                    'severity_counts': {'critical': 0, 'high': 0, 'medium': 0, 'low': 0},
                    'thresholds_exceeded': {},
                    'recommendations': []
                },
                'scan_info': {
                    'timestamp': datetime.now().isoformat(),
                    'filename': filename,
                    'status': 'failed'
                }
            }
