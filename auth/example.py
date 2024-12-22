"""
Example script demonstrating how to use the authentication module.
"""
from . import DatabaseManager

def main():
    # Initialize database connection
    db_url = "postgresql://postgres:postgres@localhost:5432/auth_db"
    db_manager = DatabaseManager(db_url)
    
    # Initialize database tables
    db_manager.init_db()
    
    # Get auth manager
    auth_manager = db_manager.get_auth_manager()
    
    # Example: Register a new user
    success, message, user = auth_manager.register_user(
        email="admin@example.com",
        password="admin123",
        first_name="Admin",
        last_name="User"
    )
    print(f"Registration: {message}")
    
    if success:
        # Example: Authenticate the user
        success, message, user = auth_manager.authenticate_user(
            email="admin@example.com",
            password="admin123"
        )
        print(f"Authentication: {message}")
        
        if success:
            # Example: Update password
            success, message = auth_manager.update_password(
                user_id=user.id,
                current_password="admin123",
                new_password="newpassword123"
            )
            print(f"Password update: {message}")
            
            # Example: Deactivate user
            success, message = auth_manager.deactivate_user(user_id=user.id)
            print(f"Deactivation: {message}")

if __name__ == "__main__":
    main()
