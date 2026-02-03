#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# Active .venv si présent (optionnel)
if [ -f .venv/bin/activate ]; then
  # shellcheck source=/dev/null
  source .venv/bin/activate
fi

# Installer les dépendances si besoin (optionnel) :
# INSTALL_REQS=1 ./run_server.sh
if [ "${INSTALL_REQS:-0}" = "1" ] && [ -f requirements.txt ]; then
  python3 -m pip install -r requirements.txt
fi

echo "Lancement du serveur..."
exec python3 -m server.server
