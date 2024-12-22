from pathlib import Path
import os
from typing import List, Dict
from rich.console import Console
from rich.progress import Progress
from AuditronAI.core.custom_dataset import CustomDataset
from dotenv import load_dotenv
import fnmatch

console = Console()

def should_exclude(file_path: str, exclude_patterns: List[str]) -> bool:
    """Vérifie si un fichier doit être exclu selon les patterns."""
    for pattern in exclude_patterns:
        if fnmatch.fnmatch(file_path, pattern) or any(p in file_path for p in pattern.split(',')):
            return True
    return False

def get_python_files(root_dir: str, exclude_patterns: str) -> List[Path]:
    """Récupère tous les fichiers Python du projet en excluant certains patterns."""
    python_files = []
    exclude_list = [p.strip() for p in exclude_patterns.split(',')]
    
    # Convertir le chemin en Path absolu
    root_path = Path(root_dir).resolve()
    console.print(f"[cyan]Recherche des fichiers Python dans {root_path}[/cyan]")
    
    for path in root_path.rglob('*.py'):
        str_path = str(path)
        
        # Debug: afficher le chemin trouvé
        console.print(f"[dim]Fichier trouvé: {str_path}[/dim]")
        
        # Vérifier si le fichier doit être exclu
        if should_exclude(str_path, exclude_list):
            console.print(f"[yellow]Exclu: {str_path}[/yellow]")
            continue
            
        # Vérifier la taille du fichier
        if path.stat().st_size > int(os.getenv('MAX_FILE_SIZE', 500000)):
            console.print(f"[yellow]Fichier trop grand: {str_path}[/yellow]")
            continue
            
        python_files.append(path)
        console.print(f"[green]Ajouté pour analyse: {str_path}[/green]")
    
    return python_files

def analyze_file(path: Path) -> Dict:
    """Analyse un fichier Python."""
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    dataset = CustomDataset(f"analysis_{path.stem}")
    
    analysis = dataset.generate_completion("project_analysis", {
        "file_path": str(path),
        "code": content
    })
    
    return {
        "file": str(path),
        "analysis": analysis
    }

def main():
    # Forcer le rechargement des variables d'environnement
    load_dotenv(override=True)
    
    console.print("[bold blue]Analyse du projet en cours...[/bold blue]")
    
    # Récupérer les fichiers Python avec les valeurs par défaut si non définies
    root_dir = os.getenv('PROJECT_ROOT', '.')
    exclude_patterns = os.getenv('EXCLUDE_PATTERNS', 'venv,__pycache__')
    max_file_size = os.getenv('MAX_FILE_SIZE', '500000')
    
    # Afficher la configuration actuelle
    console.print(f"[cyan]Configuration:[/cyan]")
    console.print(f"Dossier racine: {root_dir}")
    console.print(f"Patterns exclus: {exclude_patterns}")
    console.print(f"Taille max fichier: {max_file_size} bytes")
    
    files = get_python_files(root_dir, exclude_patterns)
    
    if not files:
        console.print("[red]Aucun fichier Python trouvé dans le projet![/red]")
        return
    
    console.print(f"[green]Nombre de fichiers à analyser: {len(files)}[/green]")
    
    # Analyser chaque fichier
    results = []
    with Progress() as progress:
        task = progress.add_task("[cyan]Analyse des fichiers...", total=len(files))
        
        for file in files:
            console.print(f"\n[bold green]Analyse de {file}...[/bold green]")
            result = analyze_file(file)
            results.append(result)
            progress.update(task, advance=1)
    
    # Afficher le résumé
    console.print("\n[bold blue]Résumé de l'analyse:[/bold blue]")
    for result in results:
        console.print(f"\n[bold yellow]{result['file']}[/bold yellow]")
        console.print(result['analysis'])
        console.print("-" * 80)

if __name__ == "__main__":
    main() 