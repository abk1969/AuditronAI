#!/bin/bash
set -e

echo "🔍 Vérification du frontend..."

# Vérifier l'environnement Node.js
check_node_env() {
    echo "Vérification de l'environnement Node.js..."
    
    if [ ! -d "node_modules" ]; then
        echo "❌ node_modules manquant"
        return 1
    fi
    
    if ! npm list react >/dev/null 2>&1; then
        echo "❌ React n'est pas installé"
        return 1
    fi
    
    echo "✅ Environnement Node.js OK"
}

# Vérifier la compilation TypeScript
check_typescript() {
    echo "Vérification de TypeScript..."
    
    if npm run tsc --noEmit; then
        echo "✅ Compilation TypeScript OK"
    else
        echo "❌ Erreurs de compilation TypeScript"
        return 1
    fi
}

# Vérifier le linting
check_linting() {
    echo "Vérification du linting..."
    
    if npm run lint; then
        echo "✅ Linting OK"
    else
        echo "❌ Erreurs de linting"
        return 1
    fi
}

# Vérifier le serveur de développement
check_dev_server() {
    echo "Démarrage du serveur de développement..."
    npm start &
    PID=$!
    
    # Attendre le démarrage du serveur
    sleep 10
    
    # Tester l'accès
    if curl -s http://localhost:3000 | grep -q "react"; then
        echo "✅ Serveur de développement OK"
        kill $PID
    else
        echo "❌ Serveur de développement ne répond pas"
        kill $PID
        return 1
    fi
}

# Exécuter toutes les vérifications
check_node_env
check_typescript
check_linting
check_dev_server

echo "✅ Vérification du frontend terminée avec succès" 