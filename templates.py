# -*- coding: utf-8 -*-
import json
# Шаблоны файлов, которые попадают в zip-архив пользователя.

TEACHER_PROMPT = '''Ты — Teacher (Учитель) в AI-команде разработки.

Твоя роль: объяснять простыми словами, без излишнего жаргона.
Когда пользователь просит реализовать функцию или объяснить код:
1. Сначала дай простое объяснение "для человека", как будто рассказываешь другу.
2. Затем покажи код с подробными комментариями.
3. Укажи частые ошибки новичков именно в этой теме.
'''

REVIEWER_PROMPT = '''Ты — Senior Reviewer в AI-команде разработки.

Твоя роль: находить ошибки, уязвимости и места для улучшения в коде.

Проверяй по чек-листу:
- Есть ли необработанные исключения / edge cases?
- Нет ли утечек секретов?
- Достаточно ли читаемый код?
- Есть ли узкие места по производительности?
'''

ARBITER_PROMPT = '''Ты — Arbiter (Арбитр) в AI-команде разработки.

Твоя роль: когда Teacher и Reviewer предлагают разные решения —
сравнить оба варианта и выдать финальное решение с обоснованием.
'''

PROMPTS = {
    "teacher_prompt.txt": TEACHER_PROMPT,
    "reviewer_prompt.txt": REVIEWER_PROMPT,
    "arbiter_prompt.txt": ARBITER_PROMPT,
}


def build_requirements(data: dict) -> str:
    language = data.get("language", "Python")
    model = data.get("model", "Пока не знаю")
    project_type = data.get("project_type", "Telegram-бот")

    if language == "JavaScript / TypeScript":
        deps = ["dotenv"]
        if project_type == "Telegram-бот":
            deps.append("node-telegram-bot-api")
        if model in ("GPT", "GPT + Claude", "Пока не знаю"):
            deps.append("openai")
        if model in ("Claude", "GPT + Claude", "Пока не знаю"):
            deps.append("@anthropic-ai/sdk")
        return "\n".join(deps)

    deps = ["python-dotenv"]

    if project_type == "Telegram-бот":
        deps.append("aiogram")
    elif project_type == "AI-агент":
        deps.append("requests")
    elif project_type == "SaaS-сервис":
        deps += ["fastapi", "uvicorn"]
    elif project_type == "iOS-приложение":
        deps += ["fastapi", "uvicorn"]
    elif project_type == "Свободная идея":
        deps.append("aiogram")

    if model in ("GPT", "GPT + Claude", "Пока не знаю"):
        deps.append("openai")
    if model in ("Claude", "GPT + Claude", "Пока не знаю"):
        deps.append("anthropic")

    return "\n".join(deps)


def _package_name(name: str) -> str:
    allowed = "abcdefghijklmnopqrstuvwxyz0123456789"
    safe = "".join(c.lower() if c.lower() in allowed else "-" for c in name)
    safe = "-".join(part for part in safe.split("-") if part)
    return safe or "ai-creator-project"


def build_package_json(data: dict) -> str:
    project_type = data.get("project_type", "Telegram-бот")
    dependencies = {"dotenv": "^16.4.7"}

    if project_type == "Telegram-бот":
        dependencies["node-telegram-bot-api"] = "^0.66.0"

    package = {
        "name": _package_name(data.get("project_name", "ai-creator-project")),
        "version": "0.1.0",
        "private": True,
        "scripts": {
            "start": "node main.js"
        },
        "dependencies": dependencies,
    }
    return json.dumps(package, ensure_ascii=False, indent=2) + "\n"


def build_env_example(data: dict) -> str:
    project_type = data.get("project_type", "Telegram-бот")
    model = data.get("model", "Пока не знаю")

    lines = []

    if project_type in ("Telegram-бот", "Свободная идея"):
        lines.append("TELEGRAM_BOT_TOKEN=")

    if model in ("GPT", "GPT + Claude", "Пока не знаю"):
        lines.append("OPENAI_API_KEY=")

    if model in ("Claude", "GPT + Claude", "Пока не знаю"):
        lines.append("ANTHROPIC_API_KEY=")

    return "\n".join(lines) + "\n"


_PY_TELEGRAM_BOT = '''import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "Привет! Я бот, созданный через AI Creator. 🤖\\n"
        "Напиши мне что-нибудь, и я отвечу."
    )


@dp.message()
async def handle_message(message: types.Message):
    await message.answer(f"Я получил сообщение: {message.text}")


async def main():
    print("Бот запущен. Остановить — Ctrl+C")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
'''

_PY_AI_AGENT = '''import os
from dotenv import load_dotenv

load_dotenv()


class Agent:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role

    def run(self, task: str) -> str:
        return f"[{self.name}] получил задачу: {task}\\n(заглушка — подключите API)"


def main():
    agent = Agent(name="MainAgent", role="Ты полезный ассистент.")
    task = input("Введите задачу для агента: ")
    result = agent.run(task)
    print(result)


if __name__ == "__main__":
    main()
'''

_PY_SAAS = '''from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AI Creator SaaS Starter")


class TaskRequest(BaseModel):
    prompt: str


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Сервис запущен"}


@app.post("/run")
def run_task(request: TaskRequest):
    return {"result": f"Получен запрос: {request.prompt} (заглушка — подключите API)"}


# Запуск: uvicorn main:app --reload
'''

_PY_IOS_BACKEND = '''from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AI Creator — backend для iOS-приложения")


class TaskRequest(BaseModel):
    prompt: str


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Backend запущен"}


@app.post("/run")
def run_task(request: TaskRequest):
    return {"result": f"Получен запрос: {request.prompt} (заглушка — подключите API)"}
'''

_JS_TELEGRAM_BOT = '''require("dotenv").config();
const TelegramBot = require("node-telegram-bot-api");

const token = process.env.TELEGRAM_BOT_TOKEN;
const bot = new TelegramBot(token, { polling: true });

bot.onText(/\\/start/, (msg) => {
  const chatId = msg.chat.id;
  bot.sendMessage(chatId, "Привет! Я бот, созданный через AI Creator. 🤖");
});

bot.on("message", (msg) => {
  if (msg.text && msg.text.startsWith("/start")) return;
  const chatId = msg.chat.id;
  bot.sendMessage(chatId, `Я получил сообщение: ${msg.text}`);
});

console.log("Бот запущен. Остановить — Ctrl+C");
'''

_JS_TODO_STUB = '''require("dotenv").config();

console.log("AI Creator JavaScript starter");
console.log("TODO: replace this stub with the real project logic.");

function main() {
  console.log("Project is ready for JavaScript development.");
}

main();
'''

_MAIN_BY_COMBO = {
    ("Telegram-бот", "Python"): _PY_TELEGRAM_BOT,
    ("Telegram-бот", "JavaScript / TypeScript"): _JS_TELEGRAM_BOT,
    ("Telegram-бот", "Не уверен"): _PY_TELEGRAM_BOT,
    ("AI-агент", "Python"): _PY_AI_AGENT,
    ("AI-агент", "JavaScript / TypeScript"): _JS_TODO_STUB,
    ("AI-агент", "Не уверен"): _PY_AI_AGENT,
    ("SaaS-сервис", "Python"): _PY_SAAS,
    ("SaaS-сервис", "JavaScript / TypeScript"): _JS_TODO_STUB,
    ("SaaS-сервис", "Не уверен"): _PY_SAAS,
    ("iOS-приложение", "Python"): _PY_IOS_BACKEND,
    ("iOS-приложение", "JavaScript / TypeScript"): _JS_TODO_STUB,
    ("iOS-приложение", "Не уверен"): _PY_IOS_BACKEND,
    ("Свободная идея", "Python"): _PY_TELEGRAM_BOT,
    ("Свободная идея", "JavaScript / TypeScript"): _JS_TELEGRAM_BOT,
    ("Свободная идея", "Не уверен"): _PY_TELEGRAM_BOT,
}


def build_main_file(data: dict) -> tuple[str, str]:
    project_type = data.get("project_type", "Telegram-бот")
    language = data.get("language", "Python")

    content = _MAIN_BY_COMBO.get((project_type, language), _PY_TELEGRAM_BOT)
    filename = "main.js" if language == "JavaScript / TypeScript" else "main.py"
    return filename, content


def build_readme(data: dict, main_filename: str) -> str:
    name = data.get("project_name", "my_project")
    project_type = data.get("project_type", "Telegram-бот")
    custom_idea = data.get("custom_idea") or ""
    goal = data.get("goal", "")
    experience = data.get("experience", "Начинающий")
    model = data.get("model", "")
    language = data.get("language", "Python")

    detailed = experience in ("Нет опыта", "Начинающий")

    if language == "JavaScript / TypeScript":
        install_block = (
            "```bash\n"
            "npm install\n"
            "node main.js\n"
            "```"
        )
    else:
        install_block = (
            "```bash\n"
            "python -m venv venv\n"
            "venv\\Scripts\\activate   # Windows\n"
            "# source venv/bin/activate   # macOS/Linux\n"
            "pip install -r requirements.txt\n"
            f"python {main_filename}\n"
            "```"
        )

    idea_block = ""
    if custom_idea:
        idea_block = f"\n## Идея пользователя\n\n{custom_idea}\n"

    beginner_notes = ""
    if detailed:
        beginner_notes = (
            "\n## Если вы новичок — на что обратить внимание\n\n"
            "- Перед запуском скопируйте `.env.example` в файл `.env`.\n"
            "- Файл `main.py` или `main.js` — это входная точка программы.\n"
            "- Места с TODO или заглушками — это точки для доработки.\n"
        )

    return (
        f"# {name}\n\n"
        "## Описание\n\n"
        f"{project_type} для задачи: {goal}.\n"
        f"{idea_block}\n"
        f"## AI-модели\n\n- {model}\n\n"
        f"## Язык\n\n- {language}\n\n"
        f"## Установка и запуск\n\n{install_block}\n\n"
        "## Роли AI-команды\n\n"
        "- **Teacher** — объясняет простыми словами.\n"
        "- **Senior Reviewer** — проверяет решение и ищет ошибки.\n"
        "- **Arbiter** — сравнивает варианты и выдаёт финальное решение.\n"
        f"{beginner_notes}"
    )
