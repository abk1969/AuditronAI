"""Script de vérification des dépendances obsolètes."""

import json
import subprocess
import sys
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import requests

@dataclass
class PackageInfo:
    """Informations sur un package."""
    
    name: str
    current_version: str
    latest_version: str
    latest_release_date: Optional[datetime] = None
    security_vulnerabilities: List[str] = None

    def __post_init__(self):
        """Initialise les champs par défaut."""
        if self.security_vulnerabilities is None:
            self.security_vulnerabilities = []

def run_command(cmd: List[str]) -> Tuple[int, str, str]:
    """Exécute une commande shell.
    
    Args:
        cmd: Liste des arguments de la commande
        
    Returns:
        Tuple (code retour, stdout, stderr)
    """
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate()
    return process.returncode, stdout, stderr

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

def get_outdated_packages() -> List[PackageInfo]:
    """Récupère la liste des packages obsolètes.
    
    Returns:
        Liste des packages obsolètes
    """
    code, out, err = run_command(["poetry", "show", "--outdated", "--json"])
    if code != 0:
        print(f"❌ Erreur lors de la vérification des packages : {err}")
        return []
        
    try:
        packages = json.loads(out)
    except json.JSONDecodeError:
        print("❌ Erreur lors du parsing de la sortie JSON")
        return []
        
    outdated = []
    for pkg in packages:
        name = pkg.get("name")
        current = pkg.get("version")
        latest = pkg.get("latest")
        
        if not all([name, current, latest]):
            continue
            
        # Récupère les informations supplémentaires de PyPI
        pypi_info = get_pypi_info(name)
        release_date = None
        if pypi_info:
            try:
                release_info = pypi_info["releases"][latest][0]
                release_date = datetime.fromisoformat(
                    release_info["upload_time_iso_8601"]
                )
            except (KeyError, IndexError, ValueError):
                pass
                
        package = PackageInfo(
            name=name,
            current_version=current,
            latest_version=latest,
            latest_release_date=release_date
        )
        outdated.append(package)
        
    return outdated

def check_security_vulnerabilities(package: PackageInfo) -> List[str]:
    """Vérifie les vulnérabilités de sécurité d'un package.
    
    Args:
        package: Informations du package
        
    Returns:
        Liste des vulnérabilités
    """
    code, out, err = run_command([
        "poetry", "run", "safety", "check",
        f"{package.name}=={package.current_version}",
        "--json"
    ])
    
    vulnerabilities = []
    if code != 0:
        try:
            results = json.loads(out)
            for vuln in results.get("vulnerabilities", []):
                vulnerabilities.append(
                    f"{vuln.get('vulnerability_id')}: {vuln.get('advisory')}"
                )
        except (json.JSONDecodeError, KeyError):
            pass
            
    return vulnerabilities

def main() -> int:
    """Point d'entrée principal.
    
    Returns:
        Code de retour (0 si succès)
    """
    print("🔍 Vérification des dépendances obsolètes...")
    
    outdated = get_outdated_packages()
    if not outdated:
        print("✅ Toutes les dépendances sont à jour !")
        return 0
        
    print(f"\n⚠️ {len(outdated)} dépendances obsolètes trouvées :\n")
    
    for pkg in outdated:
        # Vérifie les vulnérabilités
        vulnerabilities = check_security_vulnerabilities(pkg)
        pkg.security_vulnerabilities = vulnerabilities
        
        # Affiche les informations
        print(f"📦 {pkg.name}")
        print(f"  Version actuelle : {pkg.current_version}")
        print(f"  Dernière version : {pkg.latest_version}")
        
        if pkg.latest_release_date:
            print(
                f"  Date de sortie : "
                f"{pkg.latest_release_date.strftime('%Y-%m-%d')}"
            )
            
        if pkg.security_vulnerabilities:
            print("  ❗ Vulnérabilités :")
            for vuln in pkg.security_vulnerabilities:
                print(f"    - {vuln}")
        print()
        
    return 1

if __name__ == "__main__":
    sys.exit(main()) 