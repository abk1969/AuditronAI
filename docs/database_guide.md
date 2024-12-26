# Guide d'Utilisation de la Base de Données PostgreSQL

Ce guide explique comment utiliser l'architecture de base de données PostgreSQL dans votre application Streamlit.

## Architecture

L'architecture de la base de données est construite autour de plusieurs composants clés :

1. **Docker** : Gestion des conteneurs pour PostgreSQL
2. **SQLAlchemy** : ORM pour l'interaction avec la base de données
3. **Alembic** : Gestion des migrations
4. **Pattern Singleton** : Gestion efficace des connexions

## Installation

1. Assurez-vous que Docker est installé sur votre système
2. Exécutez le script d'installation :

```bash
python AuditronAI/scripts/setup_database.py
```

Ce script va :
- Vérifier l'installation de Docker
- Créer le fichier .env si nécessaire
- Démarrer le conteneur PostgreSQL
- Appliquer les migrations initiales

## Configuration

La configuration se fait via des variables d'environnement dans le fichier `.env` :

```env
DB_HOST=db
DB_PORT=5432
DB_NAME=auditronai
DB_USER=postgres
DB_PASSWORD=postgres
```

## Utilisation dans Streamlit

### 1. Initialisation

```python
from AuditronAI.core.database import init_db, get_db_session

# Au démarrage de l'application
init_db()
```

### 2. Utilisation du Context Manager

```python
with get_db_session() as session:
    # Vos opérations de base de données ici
    results = session.query(User).all()
```

### 3. Gestion des Modèles

Les modèles sont définis avec SQLAlchemy dans `models.py`. Exemple d'utilisation :

```python
from AuditronAI.core.database.models import User, Project

# Création
with get_db_session() as session:
    user = User(username="john", email="john@example.com")
    session.add(user)
    session.commit()

# Lecture
with get_db_session() as session:
    user = session.query(User).filter_by(username="john").first()

# Mise à jour
with get_db_session() as session:
    user = session.query(User).filter_by(id=user_id).first()
    user.email = "new@email.com"
    session.commit()

# Suppression
with get_db_session() as session:
    user = session.query(User).filter_by(id=user_id).first()
    session.delete(user)
    session.commit()
```

## Migrations de Base de Données

### Création d'une Migration

```bash
cd AuditronAI/core/database/migrations
python manage_migrations.py create "description de la migration"
```

### Application des Migrations

```bash
python manage_migrations.py upgrade
```

### Retour en Arrière

```bash
python manage_migrations.py downgrade -1
```

### Voir l'État Actuel

```bash
python manage_migrations.py current
```

## Bonnes Pratiques

1. **Gestion des Sessions** :
   - Toujours utiliser le context manager `get_db_session()`
   - Les sessions sont automatiquement fermées
   - Les transactions sont gérées automatiquement

2. **Migrations** :
   - Créer une migration pour chaque changement de schéma
   - Tester les migrations avant le déploiement
   - Versionner les fichiers de migration

3. **Modèles** :
   - Définir des relations explicites
   - Utiliser les types appropriés
   - Documenter les champs importants

4. **Sécurité** :
   - Ne jamais stocker de mots de passe en clair
   - Utiliser les variables d'environnement pour les informations sensibles
   - Limiter les privilèges des utilisateurs de la base de données

## Exemple Complet

Voir `examples/database_example.py` pour un exemple complet d'utilisation de la base de données dans une application Streamlit.

## Dépannage

### 1. Problèmes de Connexion

Si vous rencontrez des problèmes de connexion :
- Vérifiez que le conteneur Docker est en cours d'exécution
- Vérifiez les variables d'environnement
- Vérifiez les logs Docker : `docker-compose logs db`

### 2. Erreurs de Migration

En cas d'erreur lors des migrations :
- Vérifiez l'historique : `python manage_migrations.py history`
- Revenez à une version stable si nécessaire
- Consultez les logs pour plus de détails

### 3. Performance

Si vous rencontrez des problèmes de performance :
- Utilisez le pooling de connexions (déjà configuré)
- Optimisez vos requêtes
- Ajoutez des index appropriés

## Support

Pour plus d'aide :
1. Consultez les logs de l'application
2. Vérifiez la documentation SQLAlchemy
3. Utilisez les outils de débogage intégrés
