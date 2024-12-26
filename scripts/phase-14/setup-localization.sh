#!/bin/bash
set -e

# Ce script configure la localisation pour AuditronAI
# Il met en place :
# - Les adaptations régionales
# - Les formats spécifiques
# - Les contenus localisés
# - Les règles culturelles

echo "🌐 Configuration de la localisation..."

# Créer la structure pour la localisation
mkdir -p localization/{regions,formats,content}

# Configuration des adaptations régionales
cat > localization/regions/regional-settings.yaml << EOF
regions:
  fr_FR:
    timezone: "Europe/Paris"
    currency: "EUR"
    paper_size: "A4"
    measurement: "metric"
    week_start: "monday"
    
  en_US:
    timezone: "America/New_York"
    currency: "USD"
    paper_size: "Letter"
    measurement: "imperial"
    week_start: "sunday"
    
  es_ES:
    timezone: "Europe/Madrid"
    currency: "EUR"
    paper_size: "A4"
    measurement: "metric"
    week_start: "monday"
    
  de_DE:
    timezone: "Europe/Berlin"
    currency: "EUR"
    paper_size: "A4"
    measurement: "metric"
    week_start: "monday"

cultural_rules:
  fr_FR:
    formal_address: true
    name_format: "{first} {last}"
    
  en_US:
    formal_address: false
    name_format: "{first} {last}"
    
  es_ES:
    formal_address: true
    name_format: "{first} {last1} {last2}"
    
  de_DE:
    formal_address: true
    name_format: "{title} {last}, {first}"
EOF

# Configuration des formats spécifiques
cat > localization/formats/format-rules.yaml << EOF
formats:
  addresses:
    fr_FR:
      format: |
        {name}
        {street}
        {postal} {city}
        {country}
    
    en_US:
      format: |
        {name}
        {street}
        {city}, {state} {postal}
        {country}
  
  phones:
    fr_FR:
      format: "+33 X XX XX XX XX"
      mobile_prefix: "06,07"
    
    en_US:
      format: "+1 (XXX) XXX-XXXX"
      mobile_prefix: "none"
  
  documents:
    fr_FR:
      date_format: "long"
      number_format: "space"
    
    en_US:
      date_format: "short"
      number_format: "comma"
EOF

# Créer les contenus localisés de base
for region in fr_FR en_US es_ES de_DE; do
    mkdir -p "localization/content/$region"
    
    # Contenus spécifiques à la région
    cat > "localization/content/$region/legal.yaml" << EOF
legal:
  terms: ""
  privacy: ""
  cookies: ""
  compliance: ""
EOF
done

echo "✅ Configuration de la localisation terminée avec succès"

# Pour utiliser ce script :
# 1. ./setup-localization.sh
# 2. Adapter les paramètres régionaux
# 3. Créer les contenus localisés

# Cette configuration assure :
# - Une adaptation culturelle appropriée
# - Des formats régionaux corrects
# - Des contenus adaptés à chaque région
# - Une expérience utilisateur cohérente 