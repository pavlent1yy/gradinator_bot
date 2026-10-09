#!/usr/bin/env bash
# Установка и запуск бота на чистом Ubuntu Server: sudo ./deploy/install.sh
set -euo pipefail

cd "$(dirname "$0")/.."

if [ "$(id -u)" -ne 0 ]; then
    echo "Запусти через sudo" >&2
    exit 1
fi

if [ ! -f .env ]; then
    cp .env.example .env
    echo "Создан .env — заполни BOT_TOKEN, API_BASE_URL, DB_PATH=/app/data/gradinator_bot.sqlite3 и PROXY, затем запусти скрипт снова" >&2
    exit 1
fi

if ! command -v docker >/dev/null 2>&1; then
    apt-get update
    apt-get install -y ca-certificates curl
    install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    chmod a+r /etc/apt/keyrings/docker.asc
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
        > /etc/apt/sources.list.d/docker.list
    apt-get update
    apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
fi

systemctl enable --now docker

docker compose up -d --build
docker compose ps
