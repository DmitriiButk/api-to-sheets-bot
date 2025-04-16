# Проект API-to-Sheets Bot

## Описание

Telegram-бот, предназначенный для интеграции с различными открытыми API (например, JSON Placeholder) с целью извлечения,
обработки и сохранения данных в базе данных PostgreSQL и Google Sheets.

## Основные возможности

- Автоматическое обновление Google Sheets на основе полученных данных.
- Сохранение и управление данными в базе данных PostgreSQL.
- Простая настройка и интеграция благодаря использованию файла `.env`.
- Использование Alembic для управления миграциями базы данных.

## Установка

Клонируйте репозиторий:

```bash
git clone https://github.com/DmitriiButk/api-to-sheets-bot.git
```

### Настройка nginx

Пропишите в `nginx/nginx.conf` ваш домен в поле server_name.

### Настройка окружения

Создайте файл `.env` в корне проекта и добавьте следующие записи, заменив значения на свои:

```plaintext
# для работы с телеграм ботом
TG_TOKEN='ваш токен телеграм бота'

# для работы с API
WEBHOOK_URL='ваш домен'

# для работы с гугл таблицами
SPREADSHEET_ID='ваш id таблицы'
CREDENTIALS_FILE='вашу путь к файлу credentials.json(файл с настройками доступа к Google API,
если он в корне проекта, то просто 'credentials.json'')

# для работы с базой данных
DATABASE_USER='ваше имя пользователя'
DATABASE_PASSWORD='ваш пароль пользователя'
DATABASE_NAME='ваше имя базы данных'
DATABASE_HOST='ваш хост базы данных(локально - localhost, через docker-compose - db)'
```

## Запуск

### Локальный запуск

1. Установите зависимости.

```bash
pip install -r requirements.txt
```

2. Убедитесь, что база данных PostgreSQL запущена и доступна.
3. Запустите миграции базы данных:

```bash
alembic upgrade head
```

4. Запустите бота:

 ```bash
python main.py
 ```

### Запуск через Docker

1. Установите Docker и Docker Compose.
2. Скопируйте ваш файл с настройками доступа к Google API `credentials.json` в корень проекта.
3. Соберите Docker-образ:

```bash
docker-compose build
```

4. Запустите контейнеры:

```bash
docker-compose up -d
```

Если вы указали свой домен в `nginx/nginx.conf` и настроили окружение в `.env` то проект будет работать.
Бот будет запущен в Docker-контейнере, и все необходимые сервисы (например, база данных) будут автоматически настроены.

## Стек технологий

- Python
- aiogram
- Aiohttp
- PostgreSQL
- Google Sheets API
- Docker
- Alembic
- Nginx