#!/bin/bash
set -e

echo "🧪 Configuration de PyTest..."

# Installer les dépendances de test
pip install pytest pytest-cov pytest-asyncio pytest-mock pytest-xdist pytest-bdd pytest-benchmark

# Configuration de PyTest
cat > pytest.ini << EOF
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --verbose
    --cov=AuditronAI
    --cov-report=html
    --cov-report=term
    --cov-branch
    --durations=10
    --maxfail=10
    -n auto

markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    security: Security tests
    performance: Performance tests
    api: API tests
    slow: Tests that take longer than 1s
EOF

# Créer la structure des tests
mkdir -p tests/{unit,integration,e2e,security,performance}

echo "✅ PyTest configuré avec succès" 