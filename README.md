# Gradinator Bot

Telegram-бот (aiogram 3) — клиент для G-API Gradinator. Показывает актуальное
расписание, тип недели и справочники по преподавателям/предметам/аудиториям.

## Установка

```bash
pip install -r requirements.txt
cp .env.example .env
```

Заполни `.env`:

```
BOT_TOKEN=токен от @BotFather
API_BASE_URL=http://localhost:9090
```

## Запуск

```bash
python bot.py
```

## Структура

```
bot.py            точка входа
config.py         загрузка .env
api/              клиент G-API (все эндпоинты из API_ENDPOINTS.md)
keyboards/        inline-клавиатуры и callback_data
handlers/         обработчики апдейтов
storage/          sqlite-хранилище group_name по user_id
utils/            форматирование сообщений (HTML, таблицы, blockquote)
```

## Заметки

- Эндпоинты `/api/admin/*` сейчас отдают 401 — клиент их поддерживает
  (`get_admin_snapshots`, `get_heartbeat_*`, `get_parser_change_date`), но
  бот их не использует, пока доступ не открыт.
- Группа пользователя хранится локально в sqlite, не на стороне G-API.
- Расписание рендерится через `<pre>`-таблицу + expandable blockquote для
  списка преподавателей — работает в актуальных клиентах Telegram.
