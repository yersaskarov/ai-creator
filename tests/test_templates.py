import templates


def test_should_include_prompts_for_python_telegram_bot():
    data = {
        "project_type": "Telegram-бот",
        "language": "Python",
    }

    assert templates.should_include_prompts(data) is True


def test_should_include_prompts_for_javascript_todo_stub_combo():
    data = {
        "project_type": "SaaS-сервис",
        "language": "JavaScript / TypeScript",
    }

    assert templates.should_include_prompts(data) is False


def test_should_include_prompts_for_javascript_telegram_bot():
    data = {
        "project_type": "Telegram-бот",
        "language": "JavaScript / TypeScript",
    }

    assert templates.should_include_prompts(data) is True
