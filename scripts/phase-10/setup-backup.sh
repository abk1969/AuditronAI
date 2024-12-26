#!/bin/bash
set -e

echo "💾 Configuration des sauvegardes de production..."

# Installation de Velero
helm repo add vmware-tanzu https://vmware-tanzu.github.io/helm-charts
helm repo update

helm install velero vmware-tanzu/velero \
  --namespace velero \
  --create-namespace \
  --set configuration.provider=aws \
  --set-file credentials.secretContents.cloud=./credentials-velero

# Configuration des sauvegardes
cat > backup/schedule.yaml << EOF
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: auditronai-daily-backup
  namespace: velero
spec:
  schedule: "0 1 * * *"  # Tous les jours à 1h du matin
  template:
    includedNamespaces:
    - default
    - monitoring
    ttl: 720h  # Conservation pendant 30 jours
    storageLocation: default
    volumeSnapshotLocations:
    - default
EOF

# Script de vérification des sauvegardes
cat > backup/verify-backup.sh << EOF
#!/bin/bash
set -e

# Vérifier la dernière sauvegarde
LAST_BACKUP=\$(velero backup get --output json | jq -r '.items[0].metadata.name')
BACKUP_STATUS=\$(velero backup get \$LAST_BACKUP --output json | jq -r '.status.phase')

if [ "\$BACKUP_STATUS" != "Completed" ]; then
  echo "❌ Dernière sauvegarde échouée: \$BACKUP_STATUS"
  exit 1
fi

echo "✅ Dernière sauvegarde réussie: \$LAST_BACKUP"
EOF

chmod +x backup/verify-backup.sh

echo "✅ Système de sauvegarde configuré avec succès" 