def vulnerable_function(user_input):
    """Fonction avec des vulnérabilités pour les tests."""
    exec(user_input)  # Bandit: B102
    password = "hardcoded_password"  # Bandit: B105
    return eval(user_input)  # Bandit: B307

def unused_function():
    """Fonction non utilisée pour les tests."""
    pass

UNUSED_VARIABLE = "test" 