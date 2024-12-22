from datetime import datetime
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from .models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthManager:
    def __init__(self, db_session: Session):
        self.db = db_session

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def register_user(
        self, 
        email: str, 
        password: str, 
        first_name: Optional[str] = None, 
        last_name: Optional[str] = None
    ) -> Tuple[bool, str, Optional[User]]:
        try:
            hashed_password = self.get_password_hash(password)
            user = User(
                email=email,
                password_hash=hashed_password,
                first_name=first_name,
                last_name=last_name
            )
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return True, "User registered successfully", user
        except IntegrityError:
            self.db.rollback()
            return False, "Email already registered", None
        except Exception as e:
            self.db.rollback()
            return False, f"Registration failed: {str(e)}", None

    def authenticate_user(self, email: str, password: str) -> Tuple[bool, str, Optional[User]]:
        try:
            user = self.db.query(User).filter(User.email == email).first()
            if not user:
                return False, "User not found", None
            if not user.is_active:
                return False, "User account is disabled", None
            if not self.verify_password(password, user.password_hash):
                return False, "Incorrect password", None
            
            # Update last login
            user.last_login = datetime.utcnow()
            self.db.commit()
            
            return True, "Authentication successful", user
        except Exception as e:
            return False, f"Authentication failed: {str(e)}", None

    def update_password(self, user_id: int, current_password: str, new_password: str) -> Tuple[bool, str]:
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                return False, "User not found"
            
            if not self.verify_password(current_password, user.password_hash):
                return False, "Current password is incorrect"
            
            user.password_hash = self.get_password_hash(new_password)
            self.db.commit()
            return True, "Password updated successfully"
        except Exception as e:
            self.db.rollback()
            return False, f"Password update failed: {str(e)}"

    def deactivate_user(self, user_id: int) -> Tuple[bool, str]:
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                return False, "User not found"
            
            user.is_active = False
            self.db.commit()
            return True, "User deactivated successfully"
        except Exception as e:
            self.db.rollback()
            return False, f"Deactivation failed: {str(e)}"
