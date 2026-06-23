import importlib
import asyncio


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
