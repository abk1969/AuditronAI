from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
from .auth import AuthManager

class DatabaseManager:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def init_db(self):
        """Initialize the database by creating all tables"""
        Base.metadata.create_all(bind=self.engine)

    def get_session(self):
        """Get a new database session"""
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()

    def get_auth_manager(self):
        """Get an AuthManager instance with a new session"""
        session = next(self.get_session())
        return AuthManager(session)

# Example usage:
"""
# Initialize database and get auth manager
db_manager = DatabaseManager("postgresql://user:password@localhost:5432/dbname")
db_manager.init_db()
auth_manager = db_manager.get_auth_manager()

# Register a new user
success, message, user = auth_manager.register_user(
    email="user@example.com",
    password="secure_password",
    first_name="John",
    last_name="Doe"
)

# Authenticate user
success, message, user = auth_manager.authenticate_user(
    email="user@example.com",
    password="secure_password"
)
"""
