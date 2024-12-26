"""Script de génération de rapport de dépendances."""

import json
import subprocess
import sys
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import requests
import toml
from jinja2 import Template

@dataclass
class DependencyInfo:
    """Informations sur une dépendance."""
    
    name: str
    version: str
    description: str
    homepage: Optional[str] = None
    license: Optional[str] = None
    dependencies: Set[str] = None
    dev_dependency: bool = False
    vulnerabilities: List[str] = None
    latest_version: Optional[str] = None
    latest_release_date: Optional[datetime] = None

    def __post_init__(self):
        """Initialise les champs par défaut."""
        if self.dependencies is None:
            self.dependencies = set()
        if self.vulnerabilities is None:
            self.vulnerabilities = []

def run_command(cmd: List[str]) -> str:
    """Exécute une commande shell.
    
    Args:
        cmd: Liste des arguments de la commande
        
    Returns:
        Sortie de la commande
    """
    return subprocess.check_output(cmd, text=True)

def get_pypi_info(package_name: str) -> Dict:
    """Récupère les informations PyPI d'un package.
    
    Args:
        package_name: Nom du package
        
    Returns:
        Informations du package
    """
    try:
        response = requests.get(
            f"https://pypi.org/pypi/{package_name}/json",
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except Exception:
        return {}

def get_dependencies() -> List[DependencyInfo]:
    """Récupère les informations sur toutes les dépendances.
    
    Returns:
        Liste des dépendances
    """
    # Charge le fichier pyproject.toml
    with open("pyproject.toml") as f:
        pyproject = toml.load(f)
        
    dependencies = []
    
    # Dépendances principales
    main_deps = pyproject["tool"]["poetry"]["dependencies"]
    for name, version in main_deps.items():
        if name == "python":
            continue
            
        if isinstance(version, dict):
            version = version.get("version", "*")
            
        dep = DependencyInfo(
            name=name,
            version=version,
            description="",
            dev_dependency=False
        )
        dependencies.append(dep)
        
    # Dépendances de développement
    dev_deps = pyproject["tool"]["poetry"]["group"]["dev"]["dependencies"]
    for name, version in dev_deps.items():
        if isinstance(version, dict):
            version = version.get("version", "*")
            
        dep = DependencyInfo(
            name=name,
            version=version,
            description="",
            dev_dependency=True
        )
        dependencies.append(dep)
        
    return dependencies

def enrich_dependency_info(dep: DependencyInfo) -> None:
    """Enrichit les informations d'une dépendance.
    
    Args:
        dep: Dépendance à enrichir
    """
    # Récupère les informations PyPI
    pypi_info = get_pypi_info(dep.name)
    if pypi_info:
        info = pypi_info["info"]
        dep.description = info.get("summary", "")
        dep.homepage = info.get("home_page")
        dep.license = info.get("license")
        
        # Dernière version
        if "version" in info:
            dep.latest_version = info["version"]
            
        # Date de dernière release
        releases = pypi_info.get("releases", {})
        if releases and dep.latest_version in releases:
            try:
                release_info = releases[dep.latest_version][0]
                dep.latest_release_date = datetime.fromisoformat(
                    release_info["upload_time_iso_8601"]
                )
            except (KeyError, IndexError, ValueError):
                pass
                
    # Récupère les dépendances
    try:
        output = run_command([
            "poetry", "show", "--tree", "--no-dev", dep.name
        ])
        for line in output.split("\n"):
            if "└──" in line or "├──" in line:
                subdep = line.split(" ")[-1]
                dep.dependencies.add(subdep)
    except subprocess.CalledProcessError:
        pass
        
    # Vérifie les vulnérabilités
    try:
        output = run_command([
            "poetry", "run", "safety", "check",
            f"{dep.name}=={dep.version}",
            "--json"
        ])
        results = json.loads(output)
        for vuln in results.get("vulnerabilities", []):
            dep.vulnerabilities.append(
                f"{vuln['vulnerability_id']}: {vuln['advisory']}"
            )
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        pass

def generate_html_report(dependencies: List[DependencyInfo]) -> str:
    """Génère un rapport HTML des dépendances.
    
    Args:
        dependencies: Liste des dépendances
        
    Returns:
        Rapport HTML
    """
    template = Template("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Rapport des dépendances AuditronAI</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 2em; }
            .dependency { margin-bottom: 2em; border: 1px solid #ddd; padding: 1em; }
            .header { background: #f5f5f5; padding: 0.5em; margin: -1em -1em 1em -1em; }
            .dev { background: #fff3e0; }
            .vulnerable { border-color: #ff5252; }
            .vulnerable .header { background: #ffebee; }
            .outdated { border-color: #ffd740; }
            .outdated .header { background: #fff8e1; }
            .deps { margin-top: 1em; }
            .vuln { color: #d32f2f; }
        </style>
    </head>
    <body>
        <h1>Rapport des dépendances AuditronAI</h1>
        <p>Généré le {{ now.strftime('%Y-%m-%d %H:%M:%S') }}</p>
        
        <h2>Résumé</h2>
        <ul>
            <li>Dépendances principales : {{ main_deps|length }}</li>
            <li>Dépendances de développement : {{ dev_deps|length }}</li>
            <li>Dépendances vulnérables : {{ vulnerable_deps|length }}</li>
            <li>Dépendances obsolètes : {{ outdated_deps|length }}</li>
        </ul>
        
        <h2>Dépendances</h2>
        {% for dep in dependencies %}
        <div class="dependency {% if dep.dev_dependency %}dev{% endif %}
                          {% if dep.vulnerabilities %}vulnerable{% endif %}
                          {% if dep.latest_version and dep.latest_version != dep.version %}outdated{% endif %}">
            <div class="header">
                <strong>{{ dep.name }}</strong> ({{ dep.version }})
                {% if dep.latest_version and dep.latest_version != dep.version %}
                    <span style="color: #f57c00;">
                        → {{ dep.latest_version }}
                        {% if dep.latest_release_date %}
                            ({{ dep.latest_release_date.strftime('%Y-%m-%d') }})
                        {% endif %}
                    </span>
                {% endif %}
            </div>
            
            {% if dep.description %}
                <p>{{ dep.description }}</p>
            {% endif %}
            
            {% if dep.homepage %}
                <p><a href="{{ dep.homepage }}" target="_blank">{{ dep.homepage }}</a></p>
            {% endif %}
            
            {% if dep.license %}
                <p>License : {{ dep.license }}</p>
            {% endif %}
            
            {% if dep.vulnerabilities %}
                <div class="vuln">
                    <strong>⚠️ Vulnérabilités :</strong>
                    <ul>
                    {% for vuln in dep.vulnerabilities %}
                        <li>{{ vuln }}</li>
                    {% endfor %}
                    </ul>
                </div>
            {% endif %}
            
            {% if dep.dependencies %}
                <div class="deps">
                    <strong>Dépendances :</strong>
                    <ul>
                    {% for subdep in dep.dependencies %}
                        <li>{{ subdep }}</li>
                    {% endfor %}
                    </ul>
                </div>
            {% endif %}
        </div>
        {% endfor %}
    </body>
    </html>
    """)
    
    # Prépare les données pour le template
    main_deps = [d for d in dependencies if not d.dev_dependency]
    dev_deps = [d for d in dependencies if d.dev_dependency]
    vulnerable_deps = [d for d in dependencies if d.vulnerabilities]
    outdated_deps = [
        d for d in dependencies
        if d.latest_version and d.latest_version != d.version
    ]
    
    return template.render(
        dependencies=dependencies,
        main_deps=main_deps,
        dev_deps=dev_deps,
        vulnerable_deps=vulnerable_deps,
        outdated_deps=outdated_deps,
        now=datetime.now()
    )

def main() -> int:
    """Point d'entrée principal.
    
    Returns:
        Code de retour (0 si succès)
    """
    try:
        print("📊 Génération du rapport de dépendances...")
        
        # Récupère les dépendances
        dependencies = get_dependencies()
        
        # Enrichit les informations
        for dep in dependencies:
            print(f"  Analyse de {dep.name}...")
            enrich_dependency_info(dep)
            
        # Génère le rapport HTML
        report = generate_html_report(dependencies)
        
        # Crée le répertoire reports s'il n'existe pas
        Path("reports").mkdir(exist_ok=True)
        
        # Sauvegarde le rapport
        report_path = Path("reports/dependencies.html")
        report_path.write_text(report, encoding="utf-8")
        
        print(f"\n✅ Rapport généré : {report_path}")
        return 0
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la génération du rapport : {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 