import importlib
import asyncio


class FakeUser:
    def __init__(self, user_id=123):
        self.id = user_id


class FakeMessage:
    def __init__(self, text="", user_id=123):
        self.text = text
        self.from_user = FakeUser(user_id)
        self.answers = []
        self.documents = []

    async def answer(self, text, **kwargs):
        self.answers.append(text)

    async def answer_document(self, document, **kwargs):
        self.documents.append((document, kwargs))


class FakeState:
    def __init__(self, data=None):
        self.data = dict(data or {})
        self.clear_called = False
        self.state = None

    async def clear(self):
        self.clear_called = True
        self.data.clear()
        self.state = None

    async def set_state(self, state):
        self.state = state

    async def update_data(self, **kwargs):
        self.data.update(kwargs)

    async def get_data(self):
        return self.data


def test_make_safe_filename_sanitizes_punctuation(monkeypatch):
    monkeypatch.setenv("PYTHON_DOTENV_DISABLED", "1")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:dummy_token_for_tests")

    bot = importlib.import_module("bot")

    assert bot.make_safe_filename(" My Project!!! 2026 ") == "My_Project_2026"


def test_make_safe_filename_falls_back_for_empty_result(monkeypatch):
    monkeypatch.setenv("PYTHON_DOTENV_DISABLED", "1")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:dummy_token_for_tests")

    bot = importlib.import_module("bot")

    assert bot.make_safe_filename("!!!") == "my_project"


def test_should_block_start_for_generation(monkeypatch):
    monkeypatch.setenv("PYTHON_DOTENV_DISABLED", "1")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:dummy_token_for_tests")

    bot = importlib.import_module("bot")
    lock = bot.GenerationLock()
    lock.acquire(123)

    assert bot.should_block_start_for_generation(123, lock) is True
    assert bot.should_block_start_for_generation(456, lock) is False


def test_is_valid_project_name_input(monkeypatch):
    monkeypatch.setenv("PYTHON_DOTENV_DISABLED", "1")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:dummy_token_for_tests")

    bot = importlib.import_module("bot")

    assert bot.is_valid_project_name_input(None) is False
    assert bot.is_valid_project_name_input("") is False
    assert bot.is_valid_project_name_input("   ") is False
    assert bot.is_valid_project_name_input("My Project") is True


def test_prepare_interview_data_builds_questions(monkeypatch):
    monkeypatch.setenv("PYTHON_DOTENV_DISABLED", "1")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:dummy_token_for_tests")

    bot = importlib.import_module("bot")

    data = bot.prepare_interview_data(
        "Р‘РѕС‚ РґРµР»Р°РµС‚ PDF РґРѕРєСѓРјРµРЅС‚ Рё СЃС‚Р°РІРёС‚ РїРµС‡Р°С‚СЊ."
    )

    assert data["idea_analysis"]["project_type"] == "document_automation_bot"
    assert data["interview_questions"]
    assert data["interview_answers"] == []
    assert data["interview_question_index"] == 0


def test_custom_idea_starts_interview_flow(monkeypatch):
    monkeypatch.setenv("PYTHON_DOTENV_DISABLED", "1")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:dummy_token_for_tests")

    bot = importlib.import_module("bot")

    monkeypatch.setattr(
        bot,
        "prepare_interview_data",
        lambda custom_idea: {
            "idea_analysis": {"project_type": "custom"},
            "interview_questions": ["Question one?", "Question two?"],
            "interview_answers": [],
            "interview_question_index": 0,
        },
    )

    message = FakeMessage("My custom idea", user_id=123)
    state = FakeState()

    asyncio.run(bot.set_custom_idea(message, state))

    assert state.data["custom_idea"] == "My custom idea"
    assert state.data["idea_analysis"] == {"project_type": "custom"}
    assert state.data["interview_questions"] == ["Question one?", "Question two?"]
    assert state.data["interview_answers"] == []
    assert state.state == bot.Survey.interview_question
    assert "Question one?" in message.answers[-1]


def test_interview_answer_collects_answers_and_asks_next(monkeypatch):
    monkeypatch.setenv("PYTHON_DOTENV_DISABLED", "1")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:dummy_token_for_tests")

    bot = importlib.import_module("bot")
    message = FakeMessage("First answer", user_id=123)
    state = FakeState(
        {
            "interview_questions": ["Question one?", "Question two?"],
            "interview_answers": [],
            "interview_question_index": 0,
        }
    )

    asyncio.run(bot.set_interview_answer(message, state))

    assert state.data["interview_answers"] == [
        {"question": "Question one?", "answer": "First answer"}
    ]
    assert state.data["interview_question_index"] == 1
    assert state.state is None
    assert "Question two?" in message.answers[-1]


def test_interview_answer_strips_text_before_saving(monkeypatch):
    monkeypatch.setenv("PYTHON_DOTENV_DISABLED", "1")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:dummy_token_for_tests")

    bot = importlib.import_module("bot")
    message = FakeMessage("  First answer  ", user_id=123)
    state = FakeState(
        {
            "interview_questions": ["Question one?", "Question two?"],
            "interview_answers": [],
            "interview_question_index": 0,
        }
    )

    asyncio.run(bot.set_interview_answer(message, state))

    assert state.data["interview_answers"] == [
        {"question": "Question one?", "answer": "First answer"}
    ]
    assert state.data["interview_question_index"] == 1


def test_non_text_interview_answer_does_not_advance(monkeypatch):
    monkeypatch.setenv("PYTHON_DOTENV_DISABLED", "1")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:dummy_token_for_tests")

    bot = importlib.import_module("bot")
    message = FakeMessage(None, user_id=123)
    state = FakeState(
        {
            "interview_questions": ["Question one?", "Question two?"],
            "interview_answers": [],
            "interview_question_index": 0,
        }
    )

    asyncio.run(bot.set_interview_answer(message, state))

    assert state.data["interview_answers"] == []
    assert state.data["interview_question_index"] == 0
    assert state.state is None
    assert message.answers == [
        "Ответьте текстом, чтобы я мог учесть это при генерации проекта."
    ]


def test_whitespace_interview_answer_does_not_advance(monkeypatch):
    monkeypatch.setenv("PYTHON_DOTENV_DISABLED", "1")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:dummy_token_for_tests")

    bot = importlib.import_module("bot")
    message = FakeMessage("   ", user_id=123)
    state = FakeState(
        {
            "interview_questions": ["Question one?", "Question two?"],
            "interview_answers": [],
            "interview_question_index": 0,
        }
    )

    asyncio.run(bot.set_interview_answer(message, state))

    assert state.data["interview_answers"] == []
    assert state.data["interview_question_index"] == 0
    assert message.answers == [
        "Ответьте текстом, чтобы я мог учесть это при генерации проекта."
    ]


def test_too_long_interview_answer_does_not_advance(monkeypatch):
    monkeypatch.setenv("PYTHON_DOTENV_DISABLED", "1")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:dummy_token_for_tests")

    bot = importlib.import_module("bot")
    message = FakeMessage("x" * (bot.MAX_INTERVIEW_ANSWER_LENGTH + 1), user_id=123)
    state = FakeState(
        {
            "interview_questions": ["Question one?", "Question two?"],
            "interview_answers": [],
            "interview_question_index": 0,
        }
    )

    asyncio.run(bot.set_interview_answer(message, state))

    assert state.data["interview_answers"] == []
    assert state.data["interview_question_index"] == 0
    assert message.answers == [
        "Ответ слишком длинный. Сократите его до 1500 символов."
    ]


def test_interview_answer_finishes_flow_after_last_question(monkeypatch):
    monkeypatch.setenv("PYTHON_DOTENV_DISABLED", "1")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:dummy_token_for_tests")

    bot = importlib.import_module("bot")
    message = FakeMessage("Second answer", user_id=123)
    state = FakeState(
        {
            "interview_questions": ["Question one?", "Question two?"],
            "interview_answers": [
                {"question": "Question one?", "answer": "First answer"}
            ],
            "interview_question_index": 1,
        }
    )

    asyncio.run(bot.set_interview_answer(message, state))

    assert state.data["interview_answers"] == [
        {"question": "Question one?", "answer": "First answer"},
        {"question": "Question two?", "answer": "Second answer"},
    ]
    assert state.data["interview_question_index"] == 2
    assert state.state == bot.Survey.goal
    assert message.answers


def test_start_during_active_generation_does_not_clear_state(monkeypatch):
    monkeypatch.setenv("PYTHON_DOTENV_DISABLED", "1")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:dummy_token_for_tests")

    bot = importlib.import_module("bot")
    bot.generation_lock.release(123)
    bot.generation_lock.acquire(123)
    message = FakeMessage("/start", user_id=123)
    state = FakeState()

    try:
        asyncio.run(bot.start(message, state))
    finally:
        bot.generation_lock.release(123)

    assert state.clear_called is False
    assert message.answers == ["⏳ Ваш проект уже генерируется. Дождитесь завершения."]


def test_start_during_interview_clears_old_interview_data(monkeypatch):
    monkeypatch.setenv("PYTHON_DOTENV_DISABLED", "1")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:dummy_token_for_tests")

    bot = importlib.import_module("bot")
    bot.generation_lock.release(123)
    message = FakeMessage("/start", user_id=123)
    state = FakeState(
        {
            "custom_idea": "old idea",
            "idea_analysis": {"project_type": "old"},
            "interview_questions": ["Old question?"],
            "interview_answers": [
                {"question": "Old question?", "answer": "Old answer"}
            ],
            "interview_question_index": 0,
        }
    )
    state.state = bot.Survey.interview_question

    asyncio.run(bot.start(message, state))

    assert state.clear_called is True
    assert "interview_questions" not in state.data
    assert "interview_answers" not in state.data
    assert state.state == bot.Survey.project_type


def test_project_name_empty_string_does_not_start_generation(monkeypatch):
    monkeypatch.setenv("PYTHON_DOTENV_DISABLED", "1")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:dummy_token_for_tests")

    bot = importlib.import_module("bot")

    async def fail_generate_project_archive(data, user_id):
        raise AssertionError("generation should not start")

    monkeypatch.setattr(bot, "generate_project_archive", fail_generate_project_archive)
    message = FakeMessage("   ", user_id=123)
    state = FakeState()

    asyncio.run(bot.finish_survey(message, state))

    assert message.answers == ["Введите название проекта текстом."]
    assert bot.generation_lock.is_active(123) is False


def test_project_name_non_text_does_not_start_generation(monkeypatch):
    monkeypatch.setenv("PYTHON_DOTENV_DISABLED", "1")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:dummy_token_for_tests")

    bot = importlib.import_module("bot")

    async def fail_generate_project_archive(data, user_id):
        raise AssertionError("generation should not start")

    monkeypatch.setattr(bot, "generate_project_archive", fail_generate_project_archive)
    message = FakeMessage(None, user_id=123)
    state = FakeState()

    asyncio.run(bot.finish_survey(message, state))

    assert message.answers == ["Введите название проекта текстом."]
    assert bot.generation_lock.is_active(123) is False


def test_project_name_valid_text_starts_generation(monkeypatch, tmp_path):
    monkeypatch.setenv("PYTHON_DOTENV_DISABLED", "1")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:dummy_token_for_tests")

    bot = importlib.import_module("bot")
    zip_path = tmp_path / "Valid_App.zip"
    zip_path.write_bytes(b"zip")
    data = {
        "project_type": "Telegram-bot",
        "custom_idea": "",
        "goal": "Test goal",
        "experience": "Beginner",
        "target_user": "Personal",
        "model": "GPT",
        "language": "Python",
        "hosting": "Local",
        "extra_answer": "",
        "readme_detail": "",
    }
    calls = []

    async def generate_project_archive(project_data, user_id):
        calls.append((project_data["project_name"], user_id))
        project_data["_generation_mode"] = "template"
        return zip_path, project_data["project_name"], ["README.md"]

    monkeypatch.setattr(bot, "generate_project_archive", generate_project_archive)
    message = FakeMessage(" Valid App ", user_id=123)
    state = FakeState(data)

    asyncio.run(bot.finish_survey(message, state))

    assert calls == [("Valid App", 123)]
    assert message.documents
    assert state.clear_called is True
    assert bot.generation_lock.is_active(123) is False


def test_generate_project_archive_uses_template_fallback_on_ai_timeout(monkeypatch, tmp_path):
    monkeypatch.setenv("PYTHON_DOTENV_DISABLED", "1")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:dummy_token_for_tests")

    bot = importlib.import_module("bot")

    async def slow_generate_project_files(data):
        await asyncio.sleep(1)
        return {"AI.md": "too late"}

    data = {
        "project_name": "Timeout Demo",
        "project_type": "Telegram-Р±РѕС‚",
        "custom_idea": "",
        "goal": "Test goal",
        "experience": "РќР°С‡РёРЅР°СЋС‰РёР№",
        "target_user": "Personal",
        "model": "GPT",
        "language": "Python",
        "hosting": "Local",
        "extra_answer": "",
        "readme_detail": "",
        "interview_answers": [
            {
                "question": "РљР°РєРёРµ С„РѕСЂРјР°С‚С‹?",
                "answer": "PDF",
            }
        ],
    }

    monkeypatch.setattr(bot, "GENERATED_DIR", tmp_path)
    monkeypatch.setattr(bot, "AI_GENERATION_TIMEOUT_SECONDS", 0.01)
    monkeypatch.setattr(bot.ai_generator, "generate_project_files", slow_generate_project_files)

    zip_path, project_name, files_list = asyncio.run(
        bot.generate_project_archive(data, user_id=123)
    )

    try:
        assert project_name == "Timeout Demo"
        assert "requirements.txt" in files_list
        assert "AI.md" not in files_list
        assert data["_generation_mode"] == "template"
        assert zip_path.exists()
    finally:
        bot.cleanup_project_paths(data.get("_zip_path"), data.get("_project_dir"))


def test_cleanup_project_paths_ignores_missing_paths(monkeypatch, tmp_path):
    monkeypatch.setenv("PYTHON_DOTENV_DISABLED", "1")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:dummy_token_for_tests")

    bot = importlib.import_module("bot")

    bot.cleanup_project_paths(tmp_path / "missing.zip", tmp_path / "missing_project")


def test_generate_project_archive_adds_idea_analysis_for_custom_idea(monkeypatch, tmp_path):
    monkeypatch.setenv("PYTHON_DOTENV_DISABLED", "1")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:dummy_token_for_tests")

    bot = importlib.import_module("bot")

    async def generate_project_files(data):
        return {
            "README.md": "\n".join(data["interview_questions"]),
            "main.py": "print('ok')",
        }

    data = {
        "project_name": "Docs Bot",
        "project_type": "Свободная идея",
        "custom_idea": "Бот делает PDF документ и ставит печать.",
        "goal": "Test goal",
        "experience": "Начинающий",
        "target_user": "Personal",
        "model": "GPT",
        "language": "Python",
        "hosting": "Local",
        "extra_answer": "",
        "readme_detail": "",
        "interview_answers": [
            {
                "question": "РљР°РєРёРµ С„РѕСЂРјР°С‚С‹?",
                "answer": "PDF",
            }
        ],
    }

    monkeypatch.setattr(bot, "GENERATED_DIR", tmp_path)
    monkeypatch.setattr(bot.ai_generator, "generate_project_files", generate_project_files)

    zip_path, _, files_list = asyncio.run(bot.generate_project_archive(data, user_id=456))

    try:
        assert data["idea_analysis"]["project_type"] == "document_automation_bot"
        assert data["interview_questions"]
        assert data["interview_answers"][0]["answer"] == "PDF"
        assert any("DOCX" in question for question in data["interview_questions"])
        assert "README.md" in files_list
    finally:
        bot.cleanup_project_paths(data.get("_zip_path"), data.get("_project_dir"))
