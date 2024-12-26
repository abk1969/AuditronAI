#!/bin/bash
set -e

# Ce script configure le système de monitoring et d'alertes pour la maintenance
# Il met en place :
# - Des alertes de maintenance préventive
# - Des notifications de mise à jour
# - Des rapports de santé système
# - Des métriques de maintenance

echo "🔔 Configuration du monitoring de maintenance..."

# Créer la structure pour le monitoring
mkdir -p monitoring/{alerts,reports,metrics}

# Configuration des alertes
cat > monitoring/alerts/maintenance-alerts.yaml << EOF
# Définition des alertes de maintenance
alerts:
  # Alerte de maintenance préventive
  preventive_maintenance:
    condition: "uptime > 30d"
    severity: warning
    message: "Maintenance préventive recommandée"

  # Alerte de mise à jour disponible
  update_available:
    condition: "updates_pending > 0"
    severity: info
    message: "Mises à jour disponibles"

  # Alerte de performance
  performance_degradation:
    condition: "response_time > 2s"
    severity: warning
    message: "Dégradation des performances détectée"
EOF

# Script de génération de rapports
cat > monitoring/reports/generate-report.sh << EOF
#!/bin/bash
set -e

# Génère des rapports détaillés sur :
# - L'état du système
# - Les maintenances effectuées
# - Les mises à jour appliquées
# - Les métriques de performance

echo "📊 Génération du rapport de maintenance..."

# Collecter les métriques
./collect-metrics.sh

# Générer le rapport
./format-report.sh

echo "✅ Rapport généré avec succès"
EOF

chmod +x monitoring/reports/*.sh

echo "✅ Configuration du monitoring de maintenance terminée avec succès"

# Pour utiliser ce script :
# 1. ./setup-monitoring-alerts.sh
# 2. Configurer les destinataires des alertes
# 3. Planifier la génération des rapports

# Cette configuration assure :
# - Une surveillance proactive du système
# - Des alertes précoces sur les besoins de maintenance
# - Une traçabilité complète des opérations 