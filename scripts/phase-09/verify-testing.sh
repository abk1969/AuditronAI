#!/bin/bash
set -e

echo "🔍 Vérification de la configuration des tests..."

# Vérifier PyTest
check_pytest() {
    echo "Vérification de PyTest..."
    if [ -f "pytest.ini" ]; then
        pytest --collect-only
        echo "✅ Configuration PyTest validée"
    else
        echo "❌ Configuration PyTest manquante"
        return 1
    fi
}

# Vérifier Cypress
check_cypress() {
    echo "Vérification de Cypress..."
    if [ -f "frontend/cypress.config.ts" ]; then
        cd frontend
        npx cypress verify
        echo "✅ Configuration Cypress validée"
        cd ..
    else
        echo "❌ Configuration Cypress manquante"
        return 1
    fi
}

# Vérifier k6
check_k6() {
    echo "Vérification de k6..."
    if [ -f "tests/performance/k6/load-test.js" ]; then
        k6 inspect tests/performance/k6/load-test.js
        echo "✅ Configuration k6 validée"
    else
        echo "❌ Configuration k6 manquante"
        return 1
    fi
}

# Vérifier Lighthouse CI
check_lighthouse() {
    echo "Vérification de Lighthouse CI..."
    if [ -f "lighthouserc.js" ]; then
        lhci healthcheck
        echo "✅ Configuration Lighthouse CI validée"
    else
        echo "❌ Configuration Lighthouse CI manquante"
        return 1
    fi
}

# Vérifier la couverture des tests
check_coverage() {
    echo "Vérification de la couverture des tests..."
    
    # Tests unitaires
    pytest --cov=AuditronAI tests/unit/
    
    # Tests d'intégration
    pytest tests/integration/
    
    # Tests E2E
    cd frontend && npx cypress run
    
    # Tests de performance
    k6 run tests/performance/k6/load-test.js --duration 30s --vus 10
    
    echo "✅ Couverture des tests validée"
}

# Exécuter toutes les vérifications
check_pytest
check_cypress
check_k6
check_lighthouse
check_coverage

echo "✅ Vérification des tests terminée avec succès" 