# OAuth Service

Сервис для авторизации через Google OAuth 2.0 с интеграцией Google Calendar.

## Описание

Приложение на FastAPI, которое предоставляет:
- Авторизацию пользователей через Google OAuth 2.0
- Получение информации о ближайшем событии из Google Calendar
- Простой веб-интерфейс для взаимодействия с сервисом

## Технологии

- **Python 3.11+**
- **FastAPI** - веб-фреймворк
- **Uvicorn** - ASGI сервер
- **aiohttp** - асинхронный HTTP клиент для Google API
- **Pydantic** - валидация данных и настроек
- **uv** - менеджер зависимостей
- **Docker** - контейнеризация

## Установка и запуск

### Локальный запуск

1. Установите зависимости:
```bash
pip install uv
uv sync
```

2. Настройте переменные окружения (см. раздел "Настройка")

3. Запустите приложение:
```bash
python src/main.py
```

4. Откройте в браузере: http://127.0.0.1:8000

### Запуск через Docker

1. Настройте переменные окружения в файле `.env`

2. Запустите контейнер:
```bash
docker-compose -f docker-compose.local.yml up
```

3. Откройте в браузере: http://localhost:8000

## Настройка

Скопируйте `.env.template` в `.env` и заполните следующие параметры:

### Google OAuth

Для работы приложения необходимо создать OAuth 2.0 credentials в [Google Cloud Console](https://console.cloud.google.com/):

1. Создайте проект или выберите существующий
2. Включите Google Calendar API
3. Создайте OAuth 2.0 Client ID (тип: Web application)
4. Добавьте authorized redirect URI: `http://127.0.0.1:8000/api/google/auth/callback`
5. Скопируйте Client ID и Client Secret

```bash
# Google OAuth credentials
GOOGLE__OAUTH__CLIENT_ID=your_client_id_here
GOOGLE__OAUTH__CLIENT_SECRET=your_client_secret_here
GOOGLE__OAUTH__REDIRECT_URI=http://127.0.0.1:8000/api/google/auth/callback
```

### Настройки сервера

```bash
# Автоперезагрузка при изменении кода (для разработки)
SERVER__RELOAD=True
```

### Настройки безопасности

```bash
# CORS: разрешенные origins
SECURITY__ALLOWED_ORIGINS=["http://localhost:8000","http://127.0.0.1:8000"]

# Cookie settings (в production используйте Secure=True с HTTPS)
SECURITY__COOKIE_SECURE=False
SECURITY__COOKIE_SAMESITE=strict
```

## API Endpoints

### Авторизация

- `GET /` - главная страница с интерфейсом
- `GET /api/google/auth/login` - инициирует OAuth flow с Google
- `GET /api/google/auth/callback` - callback endpoint для обработки ответа от Google

### Google Calendar

- `GET /api/google/calendar/next-event` - получить ближайшее событие из календаря (требует авторизации)

## Использование

1. Откройте главную страницу приложения
2. Нажмите "Войти через Google"
3. Предоставьте доступ к Google Calendar
4. После успешной авторизации нажмите "Получить событие календаря"
5. Приложение отобразит информацию о ближайшем событии

## Структура проекта

```
oauth-service/
├── src/
│   ├── main.py              # Точка входа приложения
│   ├── api/
│   │   ├── router.py        # Главный API роутер
│   │   ├── routes/
│   │   │   └── google.py    # Google OAuth endpoints
│   │   └── deps/            # Dependency injection
│   ├── core/
│   │   ├── settings.py      # Конфигурация приложения
│   │   └── constants.py     # Константы (имена cookies)
│   ├── integrations/
│   │   └── google/
│   │       ├── client.py    # Google API клиент
│   │       ├── schemas.py   # Pydantic модели
│   │       └── exceptions.py
│   └── static/
│       └── html/
│           └── index.html   # Веб-интерфейс
├── .env                      # Переменные окружения (не в git)
├── .env.template             # Шаблон конфигурации
├── pyproject.toml            # Зависимости проекта
├── Dockerfile                # Docker образ
└── docker-compose.local.yml  # Docker Compose конфигурация
```

## Безопасность

Приложение использует следующие механизмы безопасности:
- CSRF защита через OAuth state parameter
- HTTPOnly и Secure cookies для хранения токенов
- CORS middleware с whitelist origins
- Security headers (X-Content-Type-Options, X-Frame-Options, CSP)
- Валидация входных данных через Pydantic

## Разработка

Приложение использует современные практики разработки:
- Асинхронный код (async/await)
- Dependency Injection через FastAPI
- Singleton pattern для API клиентов
- Pydantic для валидации и конфигурации
- Типизация (type hints)
