# Развёртывание AI Creator на Ubuntu VPS

Это пошаговая инструкция для деплоя AI Creator на Ubuntu 22.04 (или 24.04) с нуля.
Рассчитана на начинающего разработчика.

---

## Что потребуется

- Сервер Ubuntu 22.04 или 24.04 (минимум 1 CPU, 512 MB RAM, 5 GB диска).
- SSH-доступ к серверу.
- Telegram Bot Token от [@BotFather](https://t.me/BotFather).
- API-ключ Anthropic или OpenAI (опционально; без него бот работает на шаблонах).

---

## Шаг 1 — Подключиться к серверу

```bash
ssh your_user@your_server_ip
```

---

## Шаг 2 — Обновить пакеты

```bash
sudo apt update && sudo apt upgrade -y
```

---

## Шаг 3 — Установить Docker

```bash
# Добавить официальный GPG-ключ Docker
sudo apt install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Добавить репозиторий Docker
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
  https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Установить Docker и Compose plugin
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Разрешить запуск Docker без sudo
sudo usermod -aG docker $USER
newgrp docker

# Проверить установку
docker --version
docker compose version
```

---

## Шаг 4 — Клонировать репозиторий

```bash
git clone https://github.com/yersaskarov/ai-creator.git
cd ai-creator
```

---

## Шаг 5 — Создать файл .env

```bash
cp .env.example .env
nano .env
```

Заполните значения:

```env
# Обязательно:
TELEGRAM_BOT_TOKEN=123456789:ABC-ваш-токен-от-BotFather

# Ограничить доступ конкретными Telegram ID (рекомендуется):
# Оставьте пустым, чтобы разрешить всем:
ALLOWED_TELEGRAM_IDS=123456789,987654321

# Выберите провайдера AI (или оставьте пустым для работы на шаблонах):
AI_CREATOR_PROVIDER=anthropic

# Ключи провайдеров (нужен только один):
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
```

Сохраните файл: `Ctrl+O`, `Enter`, `Ctrl+X`.

> **Важно**: не копируйте `.env` в репозиторий. Он добавлен в `.gitignore` именно для этого.

---

## Шаг 6 — Первый запуск

```bash
docker compose up -d --build
```

Docker соберёт образ (~2-3 минуты при первой сборке) и запустит контейнер.

Проверить статус:

```bash
docker compose ps
```

Ожидаемый вывод:

```
NAME              IMAGE             COMMAND           SERVICE          STATUS
ai-creator-bot    ai-creator-bot    "python bot.py"   ai-creator-bot   Up (healthy)
```

Статус `Up (healthy)` означает, что бот запущен и HEALTHCHECK пройден.

---

## Шаг 7 — Открыть бота в Telegram

Найдите вашего бота в Telegram и отправьте `/start`.

Если бот отвечает — деплой прошёл успешно.

---

## Просмотр логов

Последние 100 строк:

```bash
docker compose logs --tail=100
```

Следить в реальном времени:

```bash
docker compose logs -f
```

---

## Перезапуск бота

```bash
docker compose restart
```

---

## Остановка

```bash
docker compose down
```

Данные в `generated_projects` сохраняются в Docker volume и не удаляются.

Чтобы также удалить volume с данными:

```bash
docker compose down -v
```

---

## Обновление проекта

```bash
# Получить изменения
git pull

# Пересобрать образ и перезапустить
docker compose up -d --build
```

---

## Резервное копирование

Сгенерированные проекты хранятся в Docker-managed volume `ai-creator_generated_projects`.

Посмотреть, где находится volume:

```bash
docker volume inspect ai-creator_generated_projects
```

Сделать резервную копию volume:

```bash
docker run --rm \
  -v ai-creator_generated_projects:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/generated_projects_backup.tar.gz -C /data .
```

Восстановить из резервной копии:

```bash
docker run --rm \
  -v ai-creator_generated_projects:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/generated_projects_backup.tar.gz -C /data
```

---

## Мониторинг ресурсов

Использование CPU и памяти:

```bash
docker stats ai-creator-bot
```

---

## Типичные ошибки

### Бот не запускается — нет TELEGRAM_BOT_TOKEN

```
RuntimeError: Не найден TELEGRAM_BOT_TOKEN.
```

**Решение**: Проверьте, что файл `.env` создан и содержит корректный токен:

```bash
cat .env | grep TELEGRAM_BOT_TOKEN
```

### Ошибка "permission denied" при docker compose

```
permission denied while trying to connect to the Docker daemon
```

**Решение**: Добавьте пользователя в группу docker и перезайдите:

```bash
sudo usermod -aG docker $USER
newgrp docker
```

### Контейнер запустился, но статус unhealthy

```bash
docker inspect ai-creator-bot | grep -A5 '"Health"'
```

Посмотрите логи:

```bash
docker compose logs --tail=50
```

Убедитесь, что в `.env` нет опечаток.

### Бот работает в режиме template (не AI)

Это нормально, если провайдер не настроен или API-ключ отсутствует. Бот автоматически
переключается на встроенные шаблоны. Добавьте `AI_CREATOR_PROVIDER` и ключ провайдера
в `.env` и перезапустите: `docker compose restart`.

### Как полностью удалить и начать заново

```bash
docker compose down -v
docker rmi ai-creator-bot
git pull
docker compose up -d --build
```

---

## Структура файлов на сервере

```
ai-creator/
├── .env                  ← ваши секреты (не в git!)
├── docker-compose.yml
├── Dockerfile
└── ...
```

Docker volume `ai-creator_generated_projects` хранится отдельно, управляется Docker.

---

## Автозапуск после перезагрузки сервера

Docker daemon настроен на автозапуск по умолчанию при установке через `apt`.
Директива `restart: unless-stopped` в `docker-compose.yml` гарантирует, что контейнер
перезапустится автоматически после перезагрузки сервера.

Убедитесь, что Docker daemon включён:

```bash
sudo systemctl enable docker
sudo systemctl status docker
```
