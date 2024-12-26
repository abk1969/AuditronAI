"""Script de mise à jour sécurisée des dépendances."""

import subprocess
import sys
from pathlib import Path
from typing import List, Tuple
import json
import tempfile
import shutil

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

def check_security(temp_dir: Path) -> bool:
    """Vérifie la sécurité des dépendances.
    
    Args:
        temp_dir: Répertoire temporaire
        
    Returns:
        True si les vérifications passent
    """
    print("\n🔍 Vérification des vulnérabilités...")
    code, out, err = run_command(["poetry", "run", "safety", "check"])
    if code != 0:
        print("❌ Vulnérabilités détectées :")
        print(err or out)
        return False

    print("\n🔍 Analyse statique du code...")
    code, out, err = run_command(["poetry", "run", "bandit", "-r", "auditronai"])
    if code != 0:
        print("❌ Problèmes de sécurité détectés :")
        print(err or out)
        return False

    return True

def run_tests() -> bool:
    """Exécute les tests.
    
    Returns:
        True si les tests passent
    """
    print("\n🧪 Exécution des tests...")
    code, out, err = run_command(["poetry", "run", "pytest"])
    if code != 0:
        print("❌ Échec des tests :")
        print(err or out)
        return False
    return True

def create_backup() -> Path:
    """Crée une sauvegarde des fichiers de dépendances.
    
    Returns:
        Chemin du répertoire de sauvegarde
    """
    backup_dir = Path(tempfile.mkdtemp())
    shutil.copy("pyproject.toml", backup_dir / "pyproject.toml")
    if Path("poetry.lock").exists():
        shutil.copy("poetry.lock", backup_dir / "poetry.lock")
    return backup_dir

def restore_backup(backup_dir: Path) -> None:
    """Restaure les fichiers de dépendances depuis la sauvegarde.
    
    Args:
        backup_dir: Répertoire de sauvegarde
    """
    shutil.copy(backup_dir / "pyproject.toml", "pyproject.toml")
    if (backup_dir / "poetry.lock").exists():
        shutil.copy(backup_dir / "poetry.lock", "poetry.lock")

def update_dependencies() -> bool:
    """Met à jour les dépendances de manière sécurisée.
    
    Returns:
        True si la mise à jour est réussie
    """
    print("📦 Mise à jour des dépendances...")
    
    # Crée une sauvegarde
    backup_dir = create_backup()
    print("✅ Sauvegarde créée")
    
    try:
        # Met à jour les dépendances
        code, out, err = run_command(["poetry", "update"])
        if code != 0:
            print("❌ Erreur lors de la mise à jour :")
            print(err or out)
            restore_backup(backup_dir)
            return False
            
        # Vérifie la sécurité
        if not check_security(backup_dir):
            print("\n⚠️ Problèmes de sécurité détectés, restauration de la sauvegarde...")
            restore_backup(backup_dir)
            return False
            
        # Exécute les tests
        if not run_tests():
            print("\n⚠️ Tests échoués, restauration de la sauvegarde...")
            restore_backup(backup_dir)
            return False
            
        print("\n✅ Mise à jour réussie !")
        return True
        
    finally:
        # Nettoie la sauvegarde
        shutil.rmtree(backup_dir)

def main() -> int:
    """Point d'entrée principal.
    
    Returns:
        Code de retour (0 si succès)
    """
    try:
        if update_dependencies():
            return 0
        return 1
    except Exception as e:
        print(f"\n❌ Erreur inattendue : {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 