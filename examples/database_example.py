"""
Exemple d'utilisation de l'architecture de base de données dans une application Streamlit.
Démontre les bonnes pratiques pour l'interaction avec PostgreSQL.
"""

import streamlit as st
from uuid import UUID
import logging
from datetime import datetime

from AuditronAI.core.database import get_db_session, init_db
from AuditronAI.core.database.models import User, Project, Analysis, AnalysisResult

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_database():
    """Initialise la connexion à la base de données."""
    try:
        init_db()
        st.success("Connexion à la base de données établie avec succès")
    except Exception as e:
        st.error(f"Erreur de connexion à la base de données: {e}")
        st.stop()

def create_user(username: str, email: str, password: str) -> UUID:
    """
    Crée un nouvel utilisateur.
    
    Args:
        username: Nom d'utilisateur
        email: Adresse email
        password: Mot de passe (sera haché)
    
    Returns:
        UUID: ID de l'utilisateur créé
    """
    with get_db_session() as session:
        # Dans un cas réel, vous devriez hacher le mot de passe
        user = User(
            username=username,
            email=email,
            password_hash=password  # Utilisez une fonction de hachage appropriée
        )
        session.add(user)
        session.commit()
        return user.id

def create_project(name: str, owner_id: UUID, description: str = None) -> UUID:
    """
    Crée un nouveau projet.
    
    Args:
        name: Nom du projet
        owner_id: ID de l'utilisateur propriétaire
        description: Description du projet (optionnel)
    
    Returns:
        UUID: ID du projet créé
    """
    with get_db_session() as session:
        project = Project(
            name=name,
            owner_id=owner_id,
            description=description
        )
        session.add(project)
        session.commit()
        return project.id

def start_analysis(project_id: UUID, user_id: UUID) -> UUID:
    """
    Démarre une nouvelle analyse.
    
    Args:
        project_id: ID du projet à analyser
        user_id: ID de l'utilisateur lançant l'analyse
    
    Returns:
        UUID: ID de l'analyse créée
    """
    with get_db_session() as session:
        analysis = Analysis(
            project_id=project_id,
            created_by=user_id,
            status="running",
            configuration={"type": "security_scan"}
        )
        session.add(analysis)
        session.commit()
        return analysis.id

def add_analysis_result(analysis_id: UUID, finding: dict):
    """
    Ajoute un résultat d'analyse.
    
    Args:
        analysis_id: ID de l'analyse
        finding: Dictionnaire contenant les détails du résultat
    """
    with get_db_session() as session:
        result = AnalysisResult(
            analysis_id=analysis_id,
            analyzer_name=finding["analyzer"],
            severity=finding["severity"],
            file_path=finding["file"],
            line_number=finding.get("line"),
            message=finding["message"]
        )
        session.add(result)
        session.commit()

def complete_analysis(analysis_id: UUID, summary: dict):
    """
    Marque une analyse comme terminée.
    
    Args:
        analysis_id: ID de l'analyse
        summary: Résumé des résultats
    """
    with get_db_session() as session:
        analysis = session.query(Analysis).filter_by(id=analysis_id).first()
        if analysis:
            analysis.status = "completed"
            analysis.completed_at = datetime.now()
            analysis.result_summary = summary
            session.commit()

def main():
    st.title("Exemple d'Utilisation de la Base de Données")
    
    # Initialisation de la base de données
    initialize_database()
    
    # Interface utilisateur
    with st.form("user_form"):
        st.subheader("Créer un Utilisateur")
        username = st.text_input("Nom d'utilisateur")
        email = st.text_input("Email")
        password = st.text_input("Mot de passe", type="password")
        submit_user = st.form_submit_button("Créer")
    
    if submit_user and username and email and password:
        try:
            user_id = create_user(username, email, password)
            st.success(f"Utilisateur créé avec l'ID: {user_id}")
            
            # Création d'un projet pour l'exemple
            project_id = create_project(
                name="Projet Test",
                owner_id=user_id,
                description="Projet créé pour l'exemple"
            )
            st.info(f"Projet test créé avec l'ID: {project_id}")
            
            # Simulation d'une analyse
            analysis_id = start_analysis(project_id, user_id)
            
            # Ajout de quelques résultats d'exemple
            findings = [
                {
                    "analyzer": "security_scanner",
                    "severity": "high",
                    "file": "app.py",
                    "line": 42,
                    "message": "Vulnérabilité SQL détectée"
                },
                {
                    "analyzer": "code_quality",
                    "severity": "medium",
                    "file": "utils.py",
                    "line": 23,
                    "message": "Complexité cyclomatique élevée"
                }
            ]
            
            for finding in findings:
                add_analysis_result(analysis_id, finding)
            
            # Finalisation de l'analyse
            complete_analysis(analysis_id, {
                "total_issues": len(findings),
                "high_severity": 1,
                "medium_severity": 1
            })
            
            st.success("Exemple complet exécuté avec succès!")
            
        except Exception as e:
            st.error(f"Erreur lors de l'exécution: {e}")
            logger.exception("Erreur dans l'exemple")

if __name__ == "__main__":
    main()
