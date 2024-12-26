#!/bin/bash
set -e

echo "🔧 Configuration de Jenkins..."

# Démarrer Jenkins avec Docker
docker run -d \
    --name auditronai-jenkins \
    -p 8080:8080 \
    -p 50000:50000 \
    -v jenkins_home:/var/jenkins_home \
    jenkins/jenkins:lts

# Attendre que Jenkins démarre
echo "Attente du démarrage de Jenkins..."
until curl -s http://localhost:8080 > /dev/null; do
    sleep 5
done

# Créer le pipeline
cat > Jenkinsfile << EOF
pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'your-registry'
        IMAGE_NAME = 'auditronai'
        IMAGE_TAG = "\${env.BUILD_NUMBER}"
    }
    
    stages {
        stage('Test') {
            steps {
                sh 'poetry install'
                sh 'poetry run pytest'
                sh 'poetry run bandit -r AuditronAI/'
            }
        }
        
        stage('Build') {
            steps {
                sh "docker build -t \${DOCKER_REGISTRY}/\${IMAGE_NAME}:\${IMAGE_TAG} ."
            }
        }
        
        stage('Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-registry', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh "docker login -u \${DOCKER_USER} -p \${DOCKER_PASS} \${DOCKER_REGISTRY}"
                    sh "docker push \${DOCKER_REGISTRY}/\${IMAGE_NAME}:\${IMAGE_TAG}"
                }
            }
        }
        
        stage('Deploy') {
            when { branch 'main' }
            steps {
                withKubeConfig([credentialsId: 'kubernetes']) {
                    sh "kubectl apply -k k8s/overlays/production"
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
    }
}
EOF

echo "✅ Jenkins configuré avec succès" 