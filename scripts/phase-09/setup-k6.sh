#!/bin/bash
set -e

echo "⚡ Configuration de k6..."

# Installer k6
if ! command -v k6 &> /dev/null; then
    echo "Installation de k6..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
        echo "deb https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
        sudo apt-get update
        sudo apt-get install k6
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install k6
    fi
fi

# Créer les scripts de test de charge
mkdir -p tests/performance/k6

# Test de charge basique
cat > tests/performance/k6/load-test.js << EOF
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '1m', target: 50 },  // Montée à 50 utilisateurs
    { duration: '3m', target: 50 },  // Maintien à 50 utilisateurs
    { duration: '1m', target: 0 },   // Descente à 0
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% des requêtes sous 500ms
    http_req_failed: ['rate<0.01'],   // Moins de 1% d'erreurs
  },
};

const BASE_URL = 'http://localhost:8000';

export default function () {
  const responses = http.batch([
    ['GET', \`\${BASE_URL}/api/health\`],
    ['GET', \`\${BASE_URL}/api/metrics\`],
  ]);

  check(responses[0], {
    'health check status is 200': (r) => r.status === 200,
  });

  sleep(1);
}
EOF

# Test de stress
cat > tests/performance/k6/stress-test.js << EOF
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 100 },   // Montée rapide
    { duration: '5m', target: 100 },   // Stress soutenu
    { duration: '2m', target: 200 },   // Pic de charge
    { duration: '2m', target: 0 },     // Récupération
  ],
  thresholds: {
    http_req_duration: ['p(99)<1500'], // 99% des requêtes sous 1.5s
    http_req_failed: ['rate<0.05'],    // Moins de 5% d'erreurs
  },
};

export default function () {
  const payload = JSON.stringify({
    code: 'def example(): pass',
    language: 'python'
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  const res = http.post(\`\${BASE_URL}/api/analyze\`, payload, params);
  
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time OK': (r) => r.timings.duration < 2000,
  });

  sleep(1);
}
EOF

echo "✅ k6 configuré avec succès" 