#!/usr/bin/env bash
# Раз в пару минут (systemd-таймер): подтягивает master и пересобирает бота, если CI по коммиту зелёный
set -euo pipefail

cd "$(dirname "$0")/.."

REPO="pavlent1yy/gradinator_bot"
BRANCH="master"

git fetch -q origin "$BRANCH"

current=$(git rev-parse HEAD)
target=$(git rev-parse "origin/$BRANCH")

[ "$current" = "$target" ] && exit 0

ci=$(curl -fsS "https://api.github.com/repos/$REPO/commits/$target/check-runs" | python3 -c '
import json, sys
runs = json.load(sys.stdin)["check_runs"]
done = runs and all(r["status"] == "completed" for r in runs)
print("success" if done and all(r["conclusion"] == "success" for r in runs) else "failure" if done else "pending")
')

if [ "$ci" != "success" ]; then
    echo "CI для ${target:0:7}: $ci, деплой пропущен"
    exit 0
fi

git merge -q --ff-only "origin/$BRANCH"
docker compose up -d --build --remove-orphans
docker image prune -f >/dev/null
echo "Задеплоен ${target:0:7}"
