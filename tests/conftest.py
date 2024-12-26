import pytest
from pathlib import Path
import tempfile
import shutil
import os
from typing import Generator

@pytest.fixture(scope="session")
def test_dir() -> Path:
    """Crée un répertoire temporaire pour les tests."""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture(scope="session")
def sample_code_file(test_dir: Path) -> Path:
    """Crée un fichier Python exemple pour les tests."""
    code_file = test_dir / "sample.py"
    code_file.write_text('''
def add(a: int, b: int) -> int:
    """Additionne deux nombres."""
    return a + b

def divide(a: int, b: int) -> float:
    """Divise deux nombres."""
    return a / b  # Possible ZeroDivisionError
''')
    return code_file

@pytest.fixture(scope="session")
def sample_sql_file(test_dir: Path) -> Path:
    """Crée un fichier SQL exemple pour les tests."""
    sql_file = test_dir / "sample.sql"
    sql_file.write_text('''
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL  -- Possible security issue
);

SELECT * FROM users WHERE username = '$input';  -- Possible SQL injection
''')
    return sql_file

@pytest.fixture(scope="function")
def temp_env_vars():
    """Gère les variables d'environnement temporaires pour les tests."""
    original_env = dict(os.environ)
    yield os.environ
    os.environ.clear()
    os.environ.update(original_env)

@pytest.fixture(scope="session")
def test_config(test_dir: Path) -> dict:
    """Configuration commune pour les tests."""
    return {
        "test_dir": test_dir,
        "max_file_size": 1024 * 1024,  # 1MB
        "supported_languages": ["python", "sql", "typescript"],
        "security_levels": ["low", "medium", "high", "critical"],
        "timeout": 30,  # seconds
    }

@pytest.fixture(scope="function")
def mock_api_response():
    """Simule une réponse API pour les tests."""
    return {
        "status": "success",
        "data": {
            "issues": [
                {
                    "severity": "high",
                    "message": "Possible security vulnerability",
                    "line": 10,
                    "code": "SEC001"
                }
            ],
            "metrics": {
                "complexity": 5,
                "maintainability": 8
            }
        }
    }

@pytest.fixture(scope="session")
def sample_typescript_file(test_dir: Path) -> Path:
    """Crée un fichier TypeScript exemple pour les tests."""
    ts_file = test_dir / "sample.ts"
    ts_file.write_text('''
interface User {
    id: number;
    username: string;
    password: string;  // Sensitive data
}

function authenticate(user: string, pass: string): boolean {
    // Possible security issue
    return true;
}

const userInput = document.getElementById("user-input").value;
eval(userInput);  // Dangerous eval usage
''')
    return ts_file