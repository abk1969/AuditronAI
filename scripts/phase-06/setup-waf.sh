#!/bin/bash
set -e

echo "🛡️ Configuration du WAF (ModSecurity)..."

# Installer ModSecurity pour Nginx
docker run -d \
    --name auditronai-waf \
    -p 8080:80 \
    -v $(pwd)/waf/rules:/etc/nginx/modsecurity/rules \
    owasp/modsecurity-crs:nginx

# Configuration des règles OWASP
cat > waf/rules/custom.conf << EOF
# Protection XSS
SecRule REQUEST_COOKIES|!REQUEST_COOKIES:/__utm/|REQUEST_COOKIES_NAMES|REQUEST_HEADERS:User-Agent|REQUEST_HEADERS:Referer|REQUEST_HEADERS|REQUEST_FILENAME|REQUEST_PROTOCOL|ARGS_NAMES|ARGS|XML:/* "@detectXSS" \
    "id:1,\
    phase:2,\
    deny,\
    status:403,\
    log,\
    msg:'XSS Attack Detected'"

# Protection Injection SQL
SecRule REQUEST_COOKIES|!REQUEST_COOKIES:/__utm/|REQUEST_COOKIES_NAMES|REQUEST_HEADERS:User-Agent|REQUEST_HEADERS:Referer|REQUEST_HEADERS|REQUEST_FILENAME|REQUEST_PROTOCOL|ARGS_NAMES|ARGS|XML:/* "@detectSQLi" \
    "id:2,\
    phase:2,\
    deny,\
    status:403,\
    log,\
    msg:'SQL Injection Attack Detected'"
EOF

echo "✅ WAF configuré avec succès" 