# AI Creator — Документация

> 🇬🇧 English version: [README.md](../README.md)

**AI Creator** — прототип платформы, которая превращает описание рабочей проблемы в стартовый проект Telegram-бота или AI-ассистента, упакованный в ZIP-архив.

Статус: v0.7.1  
Тесты: 151 passing  
Docker: production-ready (non-root user, HEALTHCHECK, пиннинг зависимостей)  
CI: GitHub Actions + Gitleaks  
Стадия: VPS-ready / portfolio project

---

## Что это такое

Пользователь описывает задачу обычным языком. Бот задаёт уточняющие вопросы, определяет профессиональный домен, строит Agent Blueprint и генерирует стартовый проект — ZIP-архив с кодом, конфигами и README.

Цель: помочь перейти от «у меня есть рутинная рабочая задача» к готовому к запуску стартовому проекту без необходимости писать его с нуля.

---

## Что умеет сейчас

- Анализ свободно описанной идеи
- Интерактивное интервью (до 5 уточняющих вопросов)
- Определение домена (keyword matching)
- 7 Domain Packs с предметными знаниями
- Assistant Architect — проектирование архитектуры
- Agent Blueprint — полная продуктовая спецификация
- Генерация ZIP-проекта через Claude или OpenAI
- Fallback на встроенные шаблоны при недоступности AI
- Поддержка Python и JavaScript/TypeScript
- Защита от path traversal на двух уровнях (`path_safety.py`)
- Контроль доступа через `ALLOWED_TELEGRAM_IDS`
- Per-user generation lock (блокировка параллельной генерации)
- Generation cooldown (60 сек между генерациями, настраиваемый)
- Pipeline timeout (180 сек, защита от зависания)
- Gitleaks secret scanning на каждый push
- Docker и Docker Compose
- GitHub Actions CI
- 151 тест

---

## Как работает pipeline

```text
Проблема пользователя
        ↓
   Анализ идеи
        ↓
Уточняющее интервью
        ↓
 Определение домена
        ↓
    Domain Pack
        ↓
 Assistant Architect
        ↓
  Agent Blueprint
        ↓
AI Project Generator ──► Fallback шаблон
        ↓
   ZIP-архив
        ↓
    Telegram
```

Если AI не настроен, не отвечает, вернул некорректный JSON или вышел timeout — бот автоматически переключается на встроенный шаблон.

---

## Примеры реальных кейсов

### Zabbix Camera Monitoring Agent

**Проблема:** камеры могут лежать больше 5 дней и пропадать из отчётов.

AI Creator может сгенерировать проект агента, который:
- хранит `first_seen_down` для каждого устройства,
- показывает список long-down devices,
- отправляет Telegram summary с текущим статусом.

### Logistics Document Bot

**Поток:** DOCX шаблон → замена данных поставщика → PDF → печать/подпись.

Полезно для: накладных, счётов, актов, отгрузочных документов.

### Jira Notification Bot

**Поток:** новые задачи, смена статусов, комментарии → Telegram уведомления.

Полезно для команд, которым нужно мгновенно знать о жизненном цикле тикетов.

### Trading Assistant

**Поток:** записи сделок → расчёт RR/winrate/drawdown → недельный отчёт.

Включает: торговый журнал, prop firm risk tracker, TradingView webhook alerts.

### Internal Knowledge Assistant

**Поток:** внутренние документы, FAQ, регламенты → ответы с source references.

Полезно для: сотрудников, которым нужны быстрые ответы по процессам.

---

## Текущие Domain Packs

| Pack | Описание |
|---|---|
| **Zabbix Monitoring** | Алерты, инциденты, acknowledgement |
| **Jira Assistant** | Тикеты, статусы, уведомления |
| **Logistics** | Накладные, поставщики, документооборот |
| **Document Automation** | DOCX/PDF генерация, шаблоны |
| **Knowledge Assistant** | FAQ, внутренние знания, source references |
| **Trading Assistant** | Журнал сделок, RR/winrate, TradingView, prop firm |
| **Generic** | Fallback для неопределённого домена |

---

## Архитектура модулей

| Модуль | Что делает |
|---|---|
| `bot.py` | Telegram FSM, пользовательский flow, lock, cooldown, pipeline timeout |
| `idea_analyzer.py` | Анализ идеи, определение типа проекта |
| `interview_builder.py` | Уточняющие вопросы из Domain Pack |
| `domain_packs.py` | База доменных знаний — единый источник истины |
| `assistant_architect.py` | Проектирование архитектуры ассистента |
| `agent_blueprint.py` | Продуктовая спецификация (Agent Blueprint) |
| `ai_generator.py` | Интеграция с Claude/OpenAI, промпт, парсинг JSON |
| `project_builder.py` | Сборка файлов проекта, защищённая запись |
| `path_safety.py` | Единый источник валидации путей (path traversal protection) |
| `zip_utils.py` | Безопасное создание ZIP-архива |
| `runtime_guards.py` | Контроль доступа, GenerationLock, GenerationCooldown |
| `templates.py` | Встроенные fallback-шаблоны |

---

## Безопасность

- **`.env` не должен попадать в Git.** Файл добавлен в `.gitignore`. Никогда не коммить его.
- **Secret scanning** через Gitleaks на каждый push и pull request (`.github/workflows/secret_scanning.yml`).
- **Path traversal protection** — два независимых уровня через `path_safety.py`.
- **Safe ZIP validation** — архив создаётся только внутри разрешённого каталога.
- **Access control** — `ALLOWED_TELEGRAM_IDS` ограничивает доступ к боту по Telegram ID.
- **Generation lock** — один пользователь не может запустить параллельную генерацию.
- **Cooldown** — `GENERATION_COOLDOWN_SECONDS` (по умолчанию 60 с) между генерациями.
- **Pipeline timeout** — `GENERATION_PIPELINE_TIMEOUT_SECONDS` (по умолчанию 180 с) защищает от зависания.
- **AI response limits** — лимиты на количество файлов (12) и размер каждого (50 000 символов).
- **Prompt sanitisation** — все строки пользователя схлопываются по переносам строк перед попаданием в промпт.

---

## Запуск локально

```bash
# 1. Создать виртуальное окружение
python -m venv venv

# 2. Активировать (Windows)
.\venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Скопировать конфиг
copy .env.example .env

# 5. Заполнить .env своими значениями (TELEGRAM_BOT_TOKEN обязателен)

# 6. Запустить
python bot.py
```

Открыть бота в Telegram и отправить `/start`.

---

## Docker

```bash
# Сборка и запуск
docker compose up -d --build

# Остановка
docker compose down
```

Полная пошаговая инструкция деплоя на Ubuntu VPS: [docs/DEPLOYMENT.md](DEPLOYMENT.md).

---

## Переменные окружения

| Переменная | Обязательная | Описание |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | Да | Токен от BotFather |
| `AI_CREATOR_PROVIDER` | Нет | `anthropic` или `openai` |
| `ANTHROPIC_API_KEY` | При использовании Claude | Ключ Anthropic API |
| `OPENAI_API_KEY` | При использовании OpenAI | Ключ OpenAI API |
| `ANTHROPIC_MODEL` | Нет | Модель Anthropic (по умолчанию claude-sonnet-4-6) |
| `OPENAI_MODEL` | Нет | Модель OpenAI (по умолчанию gpt-4.1-mini) |
| `ALLOWED_TELEGRAM_IDS` | Нет | Список ID через запятую; пусто = доступ всем |
| `AI_GENERATION_TIMEOUT_SECONDS` | Нет | Таймаут AI-вызова (по умолчанию 120 с) |
| `GENERATION_COOLDOWN_SECONDS` | Нет | Cooldown между генерациями (по умолчанию 60 с, 0 = отключено) |
| `GENERATION_PIPELINE_TIMEOUT_SECONDS` | Нет | Таймаут всего pipeline (по умолчанию 180 с) |

---

## Тесты

```bash
# Проверка синтаксиса всех модулей
python -m py_compile bot.py ai_generator.py templates.py project_builder.py \
  zip_utils.py idea_analyzer.py interview_builder.py runtime_guards.py \
  domain_packs.py assistant_architect.py agent_blueprint.py path_safety.py

# Запуск тестов
python -m pytest

# На Windows через venv
.\venv\Scripts\python.exe -m pytest
```

**Текущий статус: 151 тест — все зелёные.**

Тесты покрывают: парсинг AI-ответов, безопасность путей, сборку проекта, ZIP, fallback, анализ идей, интервью, domain packs, архитектуру, agent blueprints, контроль доступа, generation lock, cooldown, промпт-энрич.

---

## Ограничения

- Generated projects нужно проверять человеком перед использованием.
- FSM state хранится в памяти (MemoryStorage) — состояние сессии теряется при перезапуске бота.
- Нет Redis FSM.
- Нет queue/worker для фоновой генерации.
- Нет полноценного мониторинга. Healthcheck контейнера добавлен в Dockerfile.
- Domain detection — rule-based keyword matching.
- Agent Blueprint — rule-based, не ML.
- Некоторые нишевые сценарии (ICT/Smart Money, Economic Calendar) генерируют generic blueprint.

---

## Roadmap

### Недавно завершено (v0.7)

- Production hardening: non-root Docker user, HEALTHCHECK, ротация логов.
- Воспроизводимые сборки: все зависимости зафиксированы.
- Инструкция деплоя на VPS добавлена (`docs/DEPLOYMENT.md`).
- Git hygiene: `pytest_tmp/` добавлен в `.gitignore`, добавлен `pytest.ini`.

### v0.8

- Новые Domain Packs: бухгалтерия, склад, HR, поддержка.
- Redis FSM (persistence при перезапуске).
- Queue / worker для фоновой генерации.
- Structured logging с request ID.
- Rate limits и user quotas.

---

## Участие в разработке

Contributions приветствуются. Прочитайте [CONTRIBUTING.md](../CONTRIBUTING.md) перед
открытием Pull Request.

По вопросам безопасности — [SECURITY.md](../SECURITY.md).

---

## Лицензия

[MIT](../LICENSE) © 2026 Yersultan Askarov
