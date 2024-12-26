#!/bin/bash
set -e

echo "📚 Configuration de Sphinx..."

# Créer la structure de documentation
mkdir -p docs/{_static,_templates,api,guides,deployment}

# Installer Sphinx et les extensions
pip install sphinx sphinx-rtd-theme sphinx-autodoc-typehints myst-parser

# Initialiser Sphinx
cd docs
sphinx-quickstart -q -p AuditronAI -a "AuditronAI Team" -v 1.0 -r 1.0 -l fr --ext-autodoc --ext-viewcode --makefile --batchfile

# Configuration de Sphinx
cat > conf.py << EOF
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'AuditronAI'
copyright = '2024, AuditronAI Team'
author = 'AuditronAI Team'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints',
    'myst_parser'
]

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
templates_path = ['_templates']

language = 'fr'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
EOF

echo "✅ Sphinx configuré avec succès" 