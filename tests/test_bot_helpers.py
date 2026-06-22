import importlib


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
