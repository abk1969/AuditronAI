#!/bin/bash
set -e

echo "🔍 Vérification de la documentation..."

# Vérifier Sphinx
check_sphinx() {
    echo "Vérification de Sphinx..."
    if [ -f "docs/conf.py" ] && [ -f "docs/Makefile" ]; then
        cd docs
        make html
        if [ -d "_build/html" ]; then
            echo "✅ Documentation Sphinx générée avec succès"
        else
            echo "❌ Erreur lors de la génération Sphinx"
            return 1
        fi
        cd ..
    else
        echo "❌ Configuration Sphinx manquante"
        return 1
    fi
}

# Vérifier MkDocs
check_mkdocs() {
    echo "Vérification de MkDocs..."
    if [ -f "mkdocs.yml" ]; then
        mkdocs build --strict
        if [ -d "site" ]; then
            echo "✅ Documentation MkDocs générée avec succès"
        else
            echo "❌ Erreur lors de la génération MkDocs"
            return 1
        fi
    else
        echo "❌ Configuration MkDocs manquante"
        return 1
    fi
}

# Vérifier la couverture de la documentation
check_coverage() {
    echo "Vérification de la couverture de la documentation..."
    
    # Vérifier les guides essentiels
    local required_guides=(
        "docs/guides/installation.md"
        "docs/guides/usage.md"
        "docs/guides/deployment.md"
    )
    
    for guide in "${required_guides[@]}"; do
        if [ ! -f "$guide" ]; then
            echo "❌ Guide manquant: $guide"
            return 1
        fi
    done
    
    echo "✅ Couverture de la documentation validée"
}

# Exécuter toutes les vérifications
check_sphinx
check_mkdocs
check_coverage

echo "✅ Vérification de la documentation terminée avec succès" 