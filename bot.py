# -*- coding: utf-8 -*-
import os
import asyncio
import logging
import shutil
from pathlib import Path

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, FSInputFile

import ai_generator
from project_builder import (
    build_static_files,
    format_files_list,
    make_safe_filename,
    write_files,
)
from zip_utils import create_project_zip

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAX_CUSTOM_IDEA_LENGTH = 1500
MAX_PROJECT_NAME_LENGTH = 80
DEFAULT_AI_GENERATION_TIMEOUT_SECONDS = 120

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError(
        "Не найден TELEGRAM_BOT_TOKEN. Создайте файл .env рядом с этим "
        "файлом и добавьте строку TELEGRAM_BOT_TOKEN=ваш_токен"
    )

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

BASE_DIR = Path(__file__).parent
GENERATED_DIR = BASE_DIR / "generated_projects"


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


def keyboard(buttons: list[str]) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=b)] for b in buttons],
        resize_keyboard=True,
    )


class Survey(StatesGroup):
    project_type = State()
    custom_idea = State()
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

    await state.update_data(custom_idea=custom_idea)
    await state.set_state(Survey.goal)
    await message.answer(
        "Какую главную задачу решает эта идея?",
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


@dp.message(Survey.project_name)
async def finish_survey(message: types.Message, state: FSMContext):
    project_name = message.text or ""
    if len(project_name) > MAX_PROJECT_NAME_LENGTH:
        await message.answer(
            f"Название проекта слишком длинное. Максимум {MAX_PROJECT_NAME_LENGTH} символов. "
            "Пожалуйста, отправьте более короткое название."
        )
        return

    await state.update_data(project_name=project_name)
    data = await state.get_data()

    safe_name = make_safe_filename(data["project_name"])
    user_id = message.from_user.id

    user_dir = GENERATED_DIR / str(user_id)
    project_dir = user_dir / safe_name
    zip_path = user_dir / f"{safe_name}.zip"

    if project_dir.exists():
        shutil.rmtree(project_dir)
    project_dir.mkdir(parents=True, exist_ok=True)

    await message.answer("Собираю проект... ⏳")

    generation_mode = "template"

    try:
        try:
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

        write_files(project_dir, files)

        if zip_path.exists():
            zip_path.unlink()

        create_project_zip(project_dir, zip_path, project_dir.parent)

        await message.answer_document(
            FSInputFile(zip_path),
            caption=f"📦 Готов проект «{data['project_name']}»",
        )

        if zip_path.exists():
            zip_path.unlink()

        custom_idea = data.get("custom_idea") or "—"
        files_list = format_files_list(files)

        summary = (
            "📦 Проект создан\n\n"
            f"Название: {data['project_name']}\n"
            f"Тип: {data['project_type']}\n"
            f"Идея: {custom_idea}\n"
            f"Задача: {data['goal']}\n"
            f"Уровень: {data['experience']}\n"
            f"Модель: {data['model']}\n"
            f"Язык: {data['language']}\n"
            f"Хостинг: {data['hosting']}\n"
            f"Режим: {generation_mode}\n\n"
            "Что внутри:\n"
            f"{files_list}\n\n"
            "Если режим template — значит AI-ключ не настроен или генерация упала, "
            "и бот использовал безопасный шаблон.\n\n"
            "Напишите /start, чтобы собрать ещё один проект."
        )

        await message.answer(summary)
        await state.clear()
    except Exception:
        logger.exception("Project generation failed")
        await message.answer(
            "Не удалось собрать проект. Попробуйте ещё раз через /start. "
            "Если ошибка повторится, проверьте настройки токенов и AI-провайдера."
        )
    finally:
        shutil.rmtree(project_dir, ignore_errors=True)


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
