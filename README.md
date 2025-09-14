# 💰 Collect Service — Платформа для групповых денежных сборов

![Django](https://img.shields.io/badge/Django-5.2.6-092E20?logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.16.1-ff1709?logo=django)
![Celery](https://img.shields.io/badge/Celery-5.5.3-ff6600?logo=python)
![Redis](https://img.shields.io/badge/Redis-7.2-DC382D?logo=redis)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-4169E1?logo=postgresql)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python)
![Docker](https://img.shields.io/badge/Docker-24.0-2496ED?logo=docker)
![Nginx](https://img.shields.io/badge/Nginx-1.27-009639?logo=nginx)

> 🖥️ Веб-сервис для создания и участия в групповых денежных сборах.  
> Реализован REST API с аутентификацией, кэшированием и асинхронной отправкой писем.

---

## 🚀 Основные возможности

### 🧩 Backend (Django + DRF + Celery + Redis)
- 📡 CRUD API для пользователей, сборов и платежей
- 🔐 Авторизация через JWT (SimpleJWT)
- 📊 Кэширование GET-эндпоинтов (django-redis)
- ✉️ Отправка писем при создании сбора/платежа (Celery + Redis)
- Swagger документация `http://127.0.0.1/api/swagger/`
- 🧠 Логика:
  - Валидация суммы платежа (нельзя превысить целевую)
  - Автоматический подсчёт текущей суммы и числа донаторов
  - Возможность «бесконечных» сборов без верхней границы
  - Обложка сбора (ImageField, хранение в volume)

### ⚙️ Инфраструктура и DevOps
- 🐳 Docker + Docker Compose: сервисы (web, db, redis, celery, nginx)
- 🌐 Nginx: реверс-прокси для доступа к API
- 📂 Отдельные volume для базы данных и медиа
- 🔒 Изоляция сервисов и воспроизводимость окружения

---

## ⚙️ Установка и запуск

```bash
git clone https://github.com/KonstantinPohodyaev/pronin_team_test.git
cd pronin_team_test
```

Создайте виртуальное окружение и активируйте его:

```bash
python -m venv venv
source venv/bin/activate  # Windows: . venv\Scripts\activate
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

### 📦 Переменные окружения

Создайте `.env` файл в корне проекта:

```env
# === Django Settings ===
DEBUG=1                        # Включение режима отладки (1 = включено, 0 = выключено)
SECRET_KEY=your_secret_key     # Секретный ключ Django (обязателен для безопасности)
ALLOWED_HOSTS=localhost,127.0.0.1,web  # Разрешённые хосты для доступа к приложению

# === PostgreSQL Database ===
POSTGRES_DB=collect_db         # Имя базы данных
POSTGRES_USER=collect_user     # Имя пользователя базы
POSTGRES_PASSWORD=collect_pass # Пароль пользователя базы
POSTGRES_PORT=5432             # Порт PostgreSQL (по умолчанию 5432)
POSTGRES_HOST=db               # Хост базы данных (в docker-compose — имя сервиса)

# === Redis & Cache ===
REDIS_LOCATION=redis://redis:6379/1  # Адрес Redis для кэша (db=1 используется отдельно от Celery)

# === Celery & Broker ===
CELERY_BROKER_URL=redis://redis:6379/0       # Redis, очередь задач (db=0)
CELERY_RESULT_BACKEND=redis://redis:6379/0   # Redis для хранения результатов выполнения задач
```

## ▶️ Запуск в Docker-контейнерах
_Перед выполнением команды необходимо запустить Docker Desktop_

### Запуск контейнеров:
_В терминале перейти на уровень с файлом docker-compose.yml_

```bash
docker compose up -d
```
### Применение миграций

```bash
docker compose exec -it web python manage.py migrate
```

### Заполнение БД моковыми данными
```bash
docker compose exec -it web python manage.py full_db
```
- `--users <int>` — количество пользователей, которые будут созданы.  
  _По умолчанию_: **10**

- `--collects <int>` — количество сборов (Collect), которые будут созданы.  
  _По умолчанию_: **5**

- `--payments <int>` — количество пожертвований (Payment), которые будут созданы.  
  _По умолчанию_: **50**
- `--flush` - очистка текущих данных в базе

### Остановка контейнеров
```bash
docker compose down
```

_Сайт будет доступен по ```http://localhost```_

---

## 👨‍💻 Автор

**Походяев Константин**  
Telegram: [@kspohodyaev](https://t.me/kspohodyaev)
