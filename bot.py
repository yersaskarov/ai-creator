# -*- coding: utf-8 -*-
import os
import asyncio
import logging
import shutil
from pathlib import Path
from typing import Any, Awaitable, Callable

from dotenv import load_dotenv
from aiogram import BaseMiddleware, Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, FSInputFile

import ai_generator
from agent_blueprint import build_agent_blueprint
from assistant_architect import build_assistant_architecture
from domain_packs import detect_domain_pack, get_domain_pack
from idea_analyzer import analyze_project_idea
from interview_builder import build_interview_questions
from project_builder import (
    build_static_files,
    make_safe_filename,
    write_files,
)
from runtime_guards import GenerationCooldown, GenerationLock, is_user_allowed, parse_allowed_ids
from zip_utils import create_project_zip

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAX_CUSTOM_IDEA_LENGTH = 1500
MAX_INTERVIEW_ANSWER_LENGTH = 1500
MAX_PROJECT_NAME_LENGTH = 80
DEFAULT_AI_GENERATION_TIMEOUT_SECONDS = 120
DEFAULT_GENERATION_COOLDOWN_SECONDS = 60
DEFAULT_GENERATION_PIPELINE_TIMEOUT_SECONDS = 180

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError(
        "Не найден TELEGRAM_BOT_TOKEN. Создайте файл .env рядом с этим "
        "файлом и добавьте строку TELEGRAM_BOT_TOKEN=ваш_токен"
    )

def load_allowed_telegram_ids() -> set[int]:
    try:
        return parse_allowed_ids(os.getenv("ALLOWED_TELEGRAM_IDS"))
    except ValueError as error:
        logger.error("Invalid ALLOWED_TELEGRAM_IDS configuration; bot startup aborted.")
        raise RuntimeError("Invalid ALLOWED_TELEGRAM_IDS configuration") from error


bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
ALLOWED_TELEGRAM_IDS = load_allowed_telegram_ids()
generation_lock = GenerationLock()

BASE_DIR = Path(__file__).parent
GENERATED_DIR = BASE_DIR / "generated_projects"


class AccessControlMiddleware(BaseMiddleware):
    def __init__(self, allowed_ids: set[int]) -> None:
        self.allowed_ids = allowed_ids

    async def __call__(
        self,
        handler: Callable[[types.Message, dict[str, Any]], Awaitable[Any]],
        event: types.Message,
        data: dict[str, Any],
    ) -> Any:
        user = data.get("event_from_user") or event.from_user
        if user and not is_user_allowed(user.id, self.allowed_ids):
            await event.answer("⛔ Доступ к этому боту ограничен.")
            return None
        return await handler(event, data)


dp.message.middleware(AccessControlMiddleware(ALLOWED_TELEGRAM_IDS))


def get_int_env(name: str, default: int) -> int:
    value = os.getenv(name)
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        logger.warning("Invalid integer value for %s; using default %s", name, default)
        return default


AI_GENERATION_TIMEOUT_SECONDS = get_int_env(
    "AI_GENERATION_TIMEOUT_SECONDS",
    DEFAULT_AI_GENERATION_TIMEOUT_SECONDS,
)
GENERATION_COOLDOWN_SECONDS = get_int_env(
    "GENERATION_COOLDOWN_SECONDS",
    DEFAULT_GENERATION_COOLDOWN_SECONDS,
)
GENERATION_PIPELINE_TIMEOUT_SECONDS = get_int_env(
    "GENERATION_PIPELINE_TIMEOUT_SECONDS",
    DEFAULT_GENERATION_PIPELINE_TIMEOUT_SECONDS,
)
generation_cooldown = GenerationCooldown(GENERATION_COOLDOWN_SECONDS)


def keyboard(buttons: list[str]) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=b)] for b in buttons],
        resize_keyboard=True,
    )


def should_block_start_for_generation(user_id: int, lock: GenerationLock) -> bool:
    return lock.is_active(user_id)


def is_valid_project_name_input(text: str | None) -> bool:
    return bool(text and text.strip())


def prepare_interview_data(custom_idea: str) -> dict[str, Any]:
    idea_analysis = analyze_project_idea(custom_idea)
    interview_questions = build_interview_questions(idea_analysis)
    return {
        "idea_analysis": idea_analysis,
        "interview_questions": interview_questions,
        "interview_answers": [],
        "interview_question_index": 0,
    }


def build_interview_answer(
    question: str,
    answer: str,
) -> dict[str, str]:
    return {
        "question": str(question).strip(),
        "answer": answer,
    }


def get_interview_question(data: dict[str, Any]) -> str | None:
    questions = data.get("interview_questions")
    index = data.get("interview_question_index", 0)
    if not isinstance(questions, list) or not isinstance(index, int):
        return None
    if index < 0 or index >= len(questions):
        return None
    question = questions[index]
    if not isinstance(question, str) or not question.strip():
        return None
    return question.strip()


def format_interview_question_prompt(index: int, total: int, question: str) -> str:
    return (
        f"Уточняющий вопрос {index + 1} из {total}:\n\n"
        f"{question}\n\n"
        "Ответьте одним сообщением."
    )


class Survey(StatesGroup):
    project_type = State()
    custom_idea = State()
    interview_question = State()
    goal = State()
    experience = State()
    target_user = State()
    model = State()
    language = State()
    hosting = State()
    extra_question = State()
    readme_detail = State()
    project_name = State()


PROJECT_TYPES = [
    "Telegram-бот",
    "AI-агент",
    "SaaS-сервис",
    "iOS-приложение",
    "Опишу идею сам",
]
GOALS = [
    "Автоматизация рутины",
    "Общение с пользователем",
    "Обработка данных",
    "Творческая генерация",
    "Другое",
]
EXPERIENCE = ["Нет опыта", "Начинающий", "Есть pet-проекты", "Профессионал"]
TARGET_USERS = [
    "Личный проект для себя",
    "Хочу попробовать монетизировать",
    "Учебный проект / портфолио",
    "Для компании / работы",
]
MODELS = ["GPT", "Claude", "GPT + Claude", "Пока не знаю"]
LANGUAGES = ["Python", "JavaScript / TypeScript", "Не уверен"]
HOSTING = ["Свой компьютер", "Локально, потом решу", "Есть сервер/VPS", "Облако (Vercel/Render и т.п.)"]
YES_NO = ["Да", "Нет"]
README_DETAIL = ["Да, максимально подробно", "Нет, я разберусь сам"]


@dp.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    user = message.from_user
    if user and should_block_start_for_generation(user.id, generation_lock):
        await message.answer("⏳ Ваш проект уже генерируется. Дождитесь завершения.")
        return

    await state.clear()
    await state.set_state(Survey.project_type)
    await message.answer(
        "Привет! Я AI Creator 🤖\n\n"
        "Отвечу на несколько вопросов и соберу для тебя готовый "
        "к запуску стартовый проект — архивом с кодом, а не просто текстом.\n\n"
        "Что хотите создать?",
        reply_markup=keyboard(PROJECT_TYPES),
    )


@dp.message(Survey.project_type, F.text.in_(PROJECT_TYPES))
async def set_project_type(message: types.Message, state: FSMContext):
    if message.text == "Опишу идею сам":
        await state.update_data(project_type="Свободная идея")
        await state.set_state(Survey.custom_idea)
        await message.answer(
            "Опишите идею одним сообщением.\n\n"
            "Пример:\n"
            "Хочу Telegram-бота для фитнес-тренера, который отвечает клиентам, "
            "записывает их на тренировки и отправляет напоминания.",
            reply_markup=types.ReplyKeyboardRemove(),
        )
        return

    await state.update_data(project_type=message.text, custom_idea="")
    await state.set_state(Survey.goal)
    await message.answer(
        "Какую главную задачу решает продукт?",
        reply_markup=keyboard(GOALS),
    )


@dp.message(Survey.custom_idea)
async def set_custom_idea(message: types.Message, state: FSMContext):
    custom_idea = message.text or ""
    if len(custom_idea) > MAX_CUSTOM_IDEA_LENGTH:
        await message.answer(
            f"Описание идеи слишком длинное. Максимум {MAX_CUSTOM_IDEA_LENGTH} символов. "
            "Пожалуйста, сократите текст и отправьте ещё раз."
        )
        return

    interview_data = prepare_interview_data(custom_idea)
    await state.update_data(custom_idea=custom_idea, **interview_data)

    first_question = get_interview_question(interview_data)
    if first_question:
        await state.set_state(Survey.interview_question)
        await message.answer(
            format_interview_question_prompt(
                interview_data["interview_question_index"],
                len(interview_data["interview_questions"]),
                first_question,
            ),
            reply_markup=types.ReplyKeyboardRemove(),
        )
        return

    await state.update_data(custom_idea=custom_idea)
    await state.set_state(Survey.goal)
    await message.answer(
        "Какую главную задачу решает эта идея?",
        reply_markup=keyboard(GOALS),
    )


@dp.message(Survey.interview_question)
async def set_interview_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    question = get_interview_question(data)
    questions = data.get("interview_questions", [])
    answers = data.get("interview_answers", [])
    index = data.get("interview_question_index", 0)

    if not question or not isinstance(questions, list) or not isinstance(index, int):
        await state.set_state(Survey.goal)
        await message.answer(
            "РљР°РєСѓСЋ РіР»Р°РІРЅСѓСЋ Р·Р°РґР°С‡Сѓ СЂРµС€Р°РµС‚ СЌС‚Р° РёРґРµСЏ?",
            reply_markup=keyboard(GOALS),
        )
        return

    answer_text = (message.text or "").strip()
    if not answer_text:
        await message.answer(
            "Ответьте текстом, чтобы я мог учесть это при генерации проекта."
        )
        return
    if len(answer_text) > MAX_INTERVIEW_ANSWER_LENGTH:
        await message.answer(
            f"Ответ слишком длинный. Сократите его до {MAX_INTERVIEW_ANSWER_LENGTH} символов."
        )
        return

    if not isinstance(answers, list):
        answers = []

    answers = [item for item in answers if isinstance(item, dict)]
    answers.append(build_interview_answer(question, answer_text))
    next_index = index + 1

    await state.update_data(
        interview_answers=answers,
        interview_question_index=next_index,
    )

    if next_index < len(questions):
        next_question = get_interview_question(
            {
                "interview_questions": questions,
                "interview_question_index": next_index,
            }
        )
        if next_question:
            await message.answer(
                format_interview_question_prompt(
                    next_index,
                    len(questions),
                    next_question,
                ),
                reply_markup=types.ReplyKeyboardRemove(),
            )
            return

    await state.set_state(Survey.goal)
    await message.answer(
        "РЎРїР°СЃРёР±Рѕ, СѓС‚РѕС‡РЅРµРЅРёСЏ СЃРѕС…СЂР°РЅРёР».\n\n"
        "РљР°РєСѓСЋ РіР»Р°РІРЅСѓСЋ Р·Р°РґР°С‡Сѓ СЂРµС€Р°РµС‚ СЌС‚Р° РёРґРµСЏ?",
        reply_markup=keyboard(GOALS),
    )


@dp.message(Survey.goal, F.text.in_(GOALS))
async def set_goal(message: types.Message, state: FSMContext):
    await state.update_data(goal=message.text)
    await state.set_state(Survey.experience)
    await message.answer(
        "Какой у вас опыт в программировании?",
        reply_markup=keyboard(EXPERIENCE),
    )


@dp.message(Survey.experience, F.text.in_(EXPERIENCE))
async def set_experience(message: types.Message, state: FSMContext):
    await state.update_data(experience=message.text)
    await state.set_state(Survey.target_user)
    await message.answer(
        "Это для вас...?",
        reply_markup=keyboard(TARGET_USERS),
    )


@dp.message(Survey.target_user, F.text.in_(TARGET_USERS))
async def set_target_user(message: types.Message, state: FSMContext):
    await state.update_data(target_user=message.text)
    await state.set_state(Survey.model)
    await message.answer(
        "Какие AI-модели хотите использовать?",
        reply_markup=keyboard(MODELS),
    )


@dp.message(Survey.model, F.text.in_(MODELS))
async def set_model(message: types.Message, state: FSMContext):
    await state.update_data(model=message.text)
    await state.set_state(Survey.language)
    await message.answer(
        "На чём удобнее писать проект?",
        reply_markup=keyboard(LANGUAGES),
    )


@dp.message(Survey.language, F.text.in_(LANGUAGES))
async def set_language(message: types.Message, state: FSMContext):
    await state.update_data(language=message.text)
    await state.set_state(Survey.hosting)
    await message.answer(
        "Где будет жить проект?",
        reply_markup=keyboard(HOSTING),
    )


@dp.message(Survey.hosting, F.text.in_(HOSTING))
async def set_hosting(message: types.Message, state: FSMContext):
    await state.update_data(hosting=message.text)
    await state.set_state(Survey.extra_question)

    data = await state.get_data()
    project_type = data["project_type"]

    if project_type == "Telegram-бот":
        await message.answer(
            "Бот будет...",
            reply_markup=keyboard([
                "Отвечать на сообщения по запросу",
                "Делать что-то по расписанию (рассылка)",
                "И то, и другое",
            ]),
        )
    elif project_type == "AI-агент":
        await message.answer(
            "Агенту нужны 'руки' (доступ к внешним инструментам)?",
            reply_markup=keyboard([
                "Только текст, без действий",
                "Доступ к интернету (поиск)",
                "Доступ к файлам/коду",
                "Несколько агентов, проверяющих друг друга",
            ]),
        )
    elif project_type == "SaaS-сервис":
        await message.answer(
            "Нужна ли система пользователей с входом (auth)?",
            reply_markup=keyboard(YES_NO),
        )
    elif project_type == "iOS-приложение":
        await message.answer(
            "Есть ли у вас Mac для разработки? Это важно: Xcode "
            "работает только на macOS.",
            reply_markup=keyboard(YES_NO),
        )
    else:
        await message.answer(
            "Что важнее всего получить в первой версии?",
            reply_markup=keyboard([
                "Рабочий прототип",
                "Красивый интерфейс",
                "AI-логику",
                "Подготовку к монетизации",
            ]),
        )


@dp.message(Survey.extra_question)
async def set_extra_answer(message: types.Message, state: FSMContext):
    await state.update_data(extra_answer=message.text)
    await state.set_state(Survey.readme_detail)
    await message.answer(
        "Нужен ли README с максимально подробной пошаговой инструкцией "
        "под ваш уровень опыта?",
        reply_markup=keyboard(README_DETAIL),
    )


@dp.message(Survey.readme_detail, F.text.in_(README_DETAIL))
async def set_readme_detail(message: types.Message, state: FSMContext):
    await state.update_data(readme_detail=message.text)
    await state.set_state(Survey.project_name)
    await message.answer(
        "Как назвать проект? Напишите название одним сообщением "
        "(можно по-русски — я сам приведу его к корректному имени папки).",
        reply_markup=types.ReplyKeyboardRemove(),
    )


async def generate_project_archive(data: dict, user_id: int) -> tuple[Path, str, list[str]]:
    project_name = data["project_name"]
    safe_name = make_safe_filename(project_name)

    user_dir = GENERATED_DIR / str(user_id)
    project_dir = user_dir / safe_name
    zip_path = user_dir / f"{safe_name}.zip"
    data["_project_dir"] = project_dir
    data["_zip_path"] = zip_path

    if project_dir.exists():
        shutil.rmtree(project_dir)
    project_dir.mkdir(parents=True, exist_ok=True)

    generation_mode = "template"

    try:
        custom_idea = data.get("custom_idea") or ""
        if custom_idea:
            if "idea_analysis" not in data:
                data["idea_analysis"] = analyze_project_idea(custom_idea)
            if "interview_questions" not in data:
                data["interview_questions"] = build_interview_questions(
                    data["idea_analysis"]
                )
            if "interview_answers" not in data:
                data["interview_answers"] = []
            if "domain_pack" not in data:
                domain_name = detect_domain_pack(custom_idea, data["idea_analysis"])
                data["domain_pack"] = get_domain_pack(domain_name)
            if "assistant_architecture" not in data:
                data["assistant_architecture"] = build_assistant_architecture(
                    data["domain_pack"],
                    data["idea_analysis"],
                    data["interview_answers"],
                )
            if "agent_blueprint" not in data:
                data["agent_blueprint"] = build_agent_blueprint(
                    custom_idea,
                    data["domain_pack"],
                    data["idea_analysis"],
                    data["interview_answers"],
                    data["assistant_architecture"],
                )

        ai_files = await asyncio.wait_for(
            ai_generator.generate_project_files(data),
            timeout=AI_GENERATION_TIMEOUT_SECONDS,
        )
    except asyncio.TimeoutError:
        logger.warning(
            "AI generation timed out after %s seconds; using template fallback",
            AI_GENERATION_TIMEOUT_SECONDS,
        )
        ai_files = None
    except Exception:
        logger.exception("AI generation failed")
        ai_files = None

    if ai_files:
        files = ai_files
        generation_mode = "AI"
    else:
        files = build_static_files(data)

    data["_generation_mode"] = generation_mode
    write_files(project_dir, files)

    if zip_path.exists():
        zip_path.unlink()

    create_project_zip(project_dir, zip_path, project_dir.parent)

    return zip_path, project_name, sorted(files.keys())


def cleanup_project_paths(zip_path: Path | None, project_dir: Path | None) -> None:
    if zip_path and zip_path.exists():
        zip_path.unlink()
    if project_dir:
        shutil.rmtree(project_dir, ignore_errors=True)


@dp.message(Survey.project_name)
async def finish_survey(message: types.Message, state: FSMContext):
    if not is_valid_project_name_input(message.text):
        await message.answer("Введите название проекта текстом.")
        return

    project_name = message.text.strip()
    if len(project_name) > MAX_PROJECT_NAME_LENGTH:
        await message.answer(
            f"Название проекта слишком длинное. Максимум {MAX_PROJECT_NAME_LENGTH} символов. "
            "Пожалуйста, отправьте более короткое название."
        )
        return

    user_id = message.from_user.id

    remaining = generation_cooldown.seconds_remaining(user_id)
    if remaining > 0:
        await message.answer("⏳ Подождите немного перед новой генерацией.")
        return

    if not generation_lock.acquire(user_id):
        await message.answer("⏳ Ваш проект уже генерируется. Дождитесь завершения.")
        return

    data = {}
    zip_path = None
    project_dir = None

    try:
        await state.update_data(project_name=project_name)
        data = await state.get_data()

        await message.answer("Собираю проект... ⏳")

        zip_path, generated_project_name, files_list = await asyncio.wait_for(
            generate_project_archive(data, user_id),
            timeout=GENERATION_PIPELINE_TIMEOUT_SECONDS,
        )
        project_dir = zip_path.parent / zip_path.stem

        await message.answer_document(
            FSInputFile(zip_path),
            caption=f"📦 Готов проект «{generated_project_name}»",
        )

        if zip_path.exists():
            zip_path.unlink()

        custom_idea = data.get("custom_idea") or "—"
        files_text = "\n".join(f"• {name}" for name in files_list)
        generation_mode = data.get("_generation_mode", "template")

        summary = (
            "📦 Проект создан\n\n"
            f"Название: {generated_project_name}\n"
            f"Тип: {data['project_type']}\n"
            f"Идея: {custom_idea}\n"
            f"Задача: {data['goal']}\n"
            f"Уровень: {data['experience']}\n"
            f"Модель: {data['model']}\n"
            f"Язык: {data['language']}\n"
            f"Хостинг: {data['hosting']}\n"
            f"Режим: {generation_mode}\n\n"
            "Что внутри:\n"
            f"{files_text}\n\n"
            "Если режим template — значит AI-ключ не настроен или генерация упала, "
            "и бот использовал безопасный шаблон.\n\n"
            "Напишите /start, чтобы собрать ещё один проект."
        )

        await message.answer(summary)
        await state.clear()
    except asyncio.TimeoutError:
        logger.warning(
            "Pipeline timed out after %s seconds for user %s",
            GENERATION_PIPELINE_TIMEOUT_SECONDS,
            user_id,
        )
        await message.answer(
            "Генерация заняла слишком много времени и была остановлена. "
            "Попробуйте ещё раз через /start."
        )
    except Exception:
        logger.exception("Project generation failed")
        await message.answer(
            "Не удалось собрать проект. Попробуйте ещё раз через /start. "
            "Если ошибка повторится, проверьте настройки токенов и AI-провайдера."
        )
    finally:
        cleanup_zip_path = zip_path or data.get("_zip_path")
        cleanup_project_dir = project_dir or data.get("_project_dir")
        cleanup_project_paths(cleanup_zip_path, cleanup_project_dir)
        generation_lock.release(user_id)
        generation_cooldown.record_finished(user_id)


@dp.message()
async def fallback(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("Напишите /start, чтобы начать.")
    else:
        await message.answer("Пожалуйста, выберите один из вариантов на кнопках ниже 🙂")


async def main():
    logger.info("Bot started. Press Ctrl+C to stop.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
