#!/bin/bash
set -e

echo "🏗️ Initialisation de la structure frontend..."

# Créer la structure des dossiers
mkdir -p src/{components,pages,services,utils,hooks,assets,styles,types}

# Créer les fichiers de base
cat > src/App.tsx << EOF
import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import Layout from './components/Layout';
import Routes from './Routes';

const App: React.FC = () => {
  return (
    <Router>
      <Layout>
        <Routes />
      </Layout>
    </Router>
  );
};

export default App;
EOF

# Créer le fichier de routes
cat > src/Routes.tsx << EOF
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import CodeAnalysis from './pages/CodeAnalysis';
import Settings from './pages/Settings';

const AppRoutes: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<Dashboard />} />
      <Route path="/analysis" element={<CodeAnalysis />} />
      <Route path="/settings" element={<Settings />} />
    </Routes>
  );
};

export default AppRoutes;
EOF

# Créer le fichier de styles global
cat > src/styles/global.css << EOF
:root {
  --primary-color: #007bff;
  --secondary-color: #6c757d;
  --success-color: #28a745;
  --danger-color: #dc3545;
  --warning-color: #ffc107;
  --info-color: #17a2b8;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
    Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
EOF

echo "✅ Structure frontend initialisée avec succès" 