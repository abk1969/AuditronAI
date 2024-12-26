#!/bin/bash
set -e

# Ce script configure les outils d'optimisation des performances pour AuditronAI
# Il met en place :
# - Des outils de profilage
# - Des configurations optimisées
# - Des mécanismes de cache
# - Des ajustements automatiques

echo "⚡ Configuration des optimisations de performance..."

# Créer la structure pour les optimisations
mkdir -p performance/{profiling,configs,cache,reports}

# Configuration du profilage Python
cat > performance/profiling/setup_profiling.py << EOF
import cProfile
import pyinstrument
import memory_profiler

def setup_profilers():
    """Configure les différents profilers pour l'application"""
    # Configuration cProfile pour le profilage CPU
    def profile_cpu(func):
        def wrapper(*args, **kwargs):
            profiler = cProfile.Profile()
            result = profiler.runc('func(*args, **kwargs)')
            profiler.dump_stats('performance/profiling/cpu_profile.stats')
            return result
        return wrapper

    # Configuration memory_profiler pour la mémoire
    def profile_memory(func):
        @memory_profiler.profile
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

    return {
        'cpu_profiler': profile_cpu,
        'memory_profiler': profile_memory
    }
EOF

# Configuration des caches
cat > performance/cache/cache_config.yaml << EOF
redis:
  # Configuration du cache Redis
  default_timeout: 3600
  max_memory: "1gb"
  max_memory_policy: "allkeys-lru"
  databases: 16

memcached:
  # Configuration de Memcached
  memory: 512
  max_item_size: "1m"
  threads: 4
  connections: 1024

application:
  # Configuration du cache applicatif
  query_cache: true
  result_cache: true
  static_cache: true
  cache_lifetime: 3600
EOF

# Configuration des optimisations système
cat > performance/configs/system_optimizations.sh << EOF
#!/bin/bash
set -e

# Optimisations système
echo "Optimisation des paramètres système..."

# Optimisations du noyau
cat > /etc/sysctl.d/99-performance.conf << CONF
# Optimisations réseau
net.core.somaxconn = 65535
net.ipv4.tcp_max_syn_backlog = 65535
net.core.netdev_max_backlog = 65535

# Optimisations mémoire
vm.swappiness = 10
vm.dirty_ratio = 60
vm.dirty_background_ratio = 2

# Optimisations système de fichiers
fs.file-max = 2097152
fs.nr_open = 2097152
CONF

# Optimisations des limites système
cat > /etc/security/limits.d/99-performance.conf << CONF
* soft nofile 1048576
* hard nofile 1048576
* soft nproc 32768
* hard nproc 32768
CONF

sysctl -p /etc/sysctl.d/99-performance.conf
EOF

chmod +x performance/configs/system_optimizations.sh

echo "✅ Configuration des optimisations terminée avec succès"

# Pour utiliser ce script :
# 1. ./setup-performance.sh
# 2. Appliquer les configurations générées
# 3. Surveiller les métriques de performance

# Cette configuration assure :
# - Un profilage précis des performances
# - Une utilisation optimale des ressources
# - Une mise en cache efficace
# - Des optimisations système appropriées 