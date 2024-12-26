# Test de sécurité avec différents cas
import os

# Problème potentiel : utilisation de eval
def unsafe_eval(user_input):
    return eval(user_input)

# Problème potentiel : mot de passe en dur
PASSWORD = "secret123"

# Problème potentiel : commande shell
def run_command(cmd):
    os.system(cmd)

# Code normal
def safe_function(x):
    return x * 2
