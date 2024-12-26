import bandit
from bandit.core import manager
import safety
from pylint import lint
import json
import os
from pathlib import Path
from typing import Dict, List, Any
from .logger import logger
from .token_manager import TokenManager
import streamlit as st
from datetime import datetime

class SecurityAnalyzer:
    def __init__(self):
        """Initialise l'analyseur de sécurité."""
        self.token_manager = TokenManager()
        self.scan_level = os.getenv('SECURITY_SCAN_LEVEL', 'high')
        self.enable_deps = os.getenv('ENABLE_DEPENDENCY_CHECK', 'true').lower() == 'true'
        self.enable_static = os.getenv('ENABLE_STATIC_ANALYSIS', 'false').lower() == 'true'
        
        # Configuration des seuils et vérifications comme avant...
        default_checks = [
            "sql-injection", "xss", "code-injection", "command-injection",
            "path-traversal", "crypto-weak", "secrets-exposure", "auth-bypass",
            "unsafe-deserialization", "insecure-transport"
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
        
        if hasattr(st.session_state, 'security_config'):
            self.thresholds = {
                'critical': st.session_state.security_config['critical_threshold'],
                'high': st.session_state.security_config['high_threshold'],
                'medium': st.session_state.security_config['medium_threshold']
            }
        else:
            self.thresholds = {
                'critical': int(os.getenv('CRITICAL_SEVERITY_THRESHOLD', 0)),
                'high': int(os.getenv('HIGH_SEVERITY_THRESHOLD', 2)),
                'medium': int(os.getenv('MEDIUM_SEVERITY_THRESHOLD', 5))
            }
        
        if not self.validate_thresholds():
            logger.warning("Utilisation des seuils par défaut")
            self.thresholds = {'critical': 0, 'high': 2, 'medium': 5}
        
        self.timeout = int(os.getenv('SECURITY_TIMEOUT', 30))
        self.max_issues = int(os.getenv('SECURITY_MAX_ISSUES', 100))
        self.min_confidence = float(os.getenv('SECURITY_MIN_CONFIDENCE', 0.8))

    def analyze(self, code: str, filename: str = "code.py") -> Dict[str, Any]:
        """Exécute l'analyse de sécurité complète avec gestion des tokens."""
        try:
            start_time = datetime.now()
            logger.info(f"Démarrage de l'analyse de sécurité pour {filename}")
            
            # Vérifications préliminaires
            if not code or not code.strip():
                return self._empty_result("Le code à analyser est vide")
            
            max_size = int(str(os.getenv('MAX_FILE_SIZE', '500000')).split('#')[0].strip())
            if len(code) > max_size:
                return self._empty_result(f"Fichier trop volumineux (max: {max_size} bytes)")

            # Réinitialiser le compteur de tokens
            self.token_manager.reset_token_count()
            
            # Découper le code en chunks si nécessaire
            code_chunks = self.token_manager.split_code_into_chunks(code)
            
            # Résultats agrégés
            aggregated_results = {
                'bandit': {'issues': []},
                'safety': {},
                'semgrep': {},
                'pylint': {'issues': []}
            }
            
            # Analyser chaque chunk selon les tâches disponibles
            for chunk in code_chunks:
                # Optimiser le chunk pour réduire les tokens
                optimized_chunk = self.token_manager.apply_token_reduction(chunk)
                
                while True:
                    task = self.token_manager.get_next_task()
                    if not task:
                        break
                        
                    # Exécuter la tâche appropriée
                    if task['name'] == 'basic_analysis':
                        pylint_results = self.run_pylint_security(optimized_chunk)
                        self._merge_results(aggregated_results['pylint'], pylint_results)
                        
                    elif task['name'] == 'security_analysis':
                        bandit_results = self.run_bandit_analysis(optimized_chunk, filename)
                        self._merge_results(aggregated_results['bandit'], bandit_results)
                        
                    elif task['name'] == 'quality_analysis':
                        if self.enable_static:
                            semgrep_results = self.run_semgrep_analysis(optimized_chunk)
                            self._merge_results(aggregated_results['semgrep'], semgrep_results)
                            
                    # Mettre à jour le compteur de tokens
                    self.token_manager.update_token_count(task['max_tokens'])
                    
                    # Vérifier le timeout
                    if (datetime.now() - start_time).seconds > self.timeout:
                        raise TimeoutError(f"L'analyse a dépassé le délai de {self.timeout} secondes")

            # Ajouter l'analyse des dépendances si activée
            if self.enable_deps:
                safety_results = self.run_safety_check()
                aggregated_results['safety'] = safety_results

            # Filtrer et limiter les résultats
            self._filter_results(aggregated_results)
            
            # Générer le résumé
            summary = self._generate_summary(aggregated_results, filename)
            aggregated_results['summary'] = summary
            
            logger.info(f"Analyse de sécurité terminée pour {filename}")
            return aggregated_results
            
        except Exception as e:
            error_msg = f"Erreur lors de l'analyse de sécurité: {str(e)}"
            logger.error(error_msg)
            return self._empty_result(error_msg)

    def _merge_results(self, target: Dict, source: Dict) -> None:
        """Fusionne les résultats d'analyse."""
        if 'issues' in target and 'issues' in source:
            target['issues'].extend(source['issues'])
        elif isinstance(source, dict):
            for key, value in source.items():
                if key not in target:
                    target[key] = value
                elif isinstance(value, list):
                    if key not in target:
                        target[key] = []
                    target[key].extend(value)

    def _filter_results(self, results: Dict[str, Any]) -> None:
        """Filtre les résultats selon la confiance et limite le nombre."""
        for tool, tool_results in results.items():
            if isinstance(tool_results, dict) and 'issues' in tool_results:
                tool_results['issues'] = [
                    issue for issue in tool_results['issues']
                    if issue.get('confidence', 0) >= self.min_confidence
                ][:self.max_issues]

    def _generate_summary(self, results: Dict[str, Any], filename: str) -> Dict[str, Any]:
        """Génère le résumé des résultats d'analyse."""
        severity_counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        
        for tool, tool_results in results.items():
            if isinstance(tool_results, dict) and 'issues' in tool_results:
                for issue in tool_results['issues']:
                    severity = issue.get('severity', 'low').lower()
                    severity_counts[severity] += 1
        
        thresholds_exceeded = {
            level: count > self.thresholds.get(level, 0)
            for level, count in severity_counts.items()
            if level in self.thresholds
        }
        
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
        
        return {
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

    def _empty_result(self, error_msg: str) -> Dict[str, Any]:
        """Crée un résultat vide avec message d'erreur."""
        return {
            'error': error_msg,
            'summary': {
                'severity_counts': {'critical': 0, 'high': 0, 'medium': 0, 'low': 0},
                'thresholds_exceeded': {},
                'recommendations': []
            }
        }

    # Les méthodes existantes run_bandit_analysis, run_safety_check, etc. restent inchangées...
    def run_bandit_analysis(self, code: str, filename: str) -> Dict[str, Any]:
        """Exécute l'analyse Bandit."""
        try:
            temp_file = Path('temp_analysis.py')
            temp_file.write_text(code)
            
            b_mgr = manager.BanditManager()
            b_mgr.discover_files([str(temp_file)])
            b_mgr.run_tests()
            
            results = {
                'issues': b_mgr.get_issue_list(),
                'metrics': b_mgr.metrics.data
            }
            
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
            temp_file = Path('temp_pylint.py')
            temp_file.write_text(code)
            
            options = [
                str(temp_file),
                '--disable=all',
                '--enable=security',
                '--output-format=json'
            ]
            
            reporter = lint.Run(options, do_exit=False)
            results = reporter.linter.report_data
            
            temp_file.unlink()
            return results
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse Pylint: {str(e)}")
            return {'error': str(e)}

    def validate_thresholds(self) -> bool:
        """Valide les seuils de sécurité."""
        for level, value in self.thresholds.items():
            if value < 0:
                logger.warning(f"Seuil {level} invalide: {value} (doit être ≥ 0)")
                return False
        
        if self.thresholds['critical'] > self.thresholds['high']:
            logger.warning("Le seuil critique ne peut pas être supérieur au seuil élevé")
            return False
        
        if self.thresholds['high'] > self.thresholds['medium']:
            logger.warning("Le seuil élevé ne peut pas être supérieur au seuil moyen")
            return False
        
        return True
