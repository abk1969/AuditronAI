#!/bin/bash
set -e

echo "📖 Génération de la documentation API..."

# Créer la structure de documentation API
mkdir -p docs/api/{core,backend,frontend}

# Documentation API Core
cat > docs/api/core/index.rst << EOF
Core API
========

.. toctree::
   :maxdepth: 2

   security_analyzer
   prompt_manager
   ai_factory

.. automodule:: AuditronAI.core
   :members:
   :undoc-members:
   :show-inheritance:
EOF

# Documentation API Backend
cat > docs/api/backend/index.rst << EOF
Backend API
==========

.. toctree::
   :maxdepth: 2

   models
   repositories
   services

.. automodule:: AuditronAI.backend
   :members:
   :undoc-members:
   :show-inheritance:
EOF

# Documentation API Frontend
cat > docs/api/frontend/index.rst << EOF
Frontend API
===========

.. toctree::
   :maxdepth: 2

   components
   hooks
   services

Components
---------

.. js:autoclass:: Layout
   :members:

.. js:autoclass:: CodeEditor
   :members:
EOF

echo "✅ Documentation API générée avec succès" 