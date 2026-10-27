#!/usr/bin/env bash
# Push portfolija na GitHub (deploy key je vezan SAMO za xdimix18/portfolio).
# Koristi se iz Odysseusa:  bash /app/data/portfolio-site/push.sh
set -euo pipefail

cd "$(dirname "$0")"
export GIT_SSH_COMMAND="ssh -i /app/data/.ssh/id_ed25519_portfolio -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new -o ConnectTimeout=10"

git add -A
if ! git diff --cached --quiet; then
  git -c commit.gpgsign=false commit -m "${1:-chore(portfolio): azuriranje sadrzaja}"
fi

git push -u origin main
echo "OK — push prošao. Cloudflare Pages će sam pokrenuti novi deploy."
