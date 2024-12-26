#!/bin/bash
set -e

echo "📊 Configuration de SonarQube..."

# Démarrer SonarQube
docker run -d \
    --name auditronai-sonarqube \
    -p 9000:9000 \
    -e SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true \
    sonarqube:latest

# Attendre que SonarQube soit prêt
echo "Attente du démarrage de SonarQube..."
until curl -s http://localhost:9000 > /dev/null; do
    sleep 5
done

# Configuration du projet
cat > sonar-project.properties << EOF
sonar.projectKey=auditronai
sonar.projectName=AuditronAI
sonar.projectVersion=1.0
sonar.sources=AuditronAI
sonar.tests=tests
sonar.python.coverage.reportPaths=coverage.xml
sonar.python.xunit.reportPath=test-results.xml
sonar.python.bandit.reportPaths=bandit-report.json
EOF

echo "✅ SonarQube configuré avec succès" 