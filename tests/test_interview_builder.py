import interview_builder


def test_build_interview_questions_returns_list_of_strings():
    result = interview_builder.build_interview_questions(
        {"questions": ["First?", "Second?"]}
    )

    assert isinstance(result, list)
    assert all(isinstance(question, str) for question in result)


def test_build_interview_questions_respects_max_questions():
    result = interview_builder.build_interview_questions(
        {
            "questions": [
                "One?",
                "Two?",
                "Three?",
            ]
        },
        max_questions=2,
    )

    assert result == ["One?", "Two?"]


def test_build_interview_questions_removes_empty_questions():
    result = interview_builder.build_interview_questions(
        {"questions": ["", "  ", "Real question?"]}
    )

    assert result == ["Real question?"]


def test_build_interview_questions_removes_duplicates():
    result = interview_builder.build_interview_questions(
        {"questions": ["Same?", "same?", "Other?"]}
    )

    assert result == ["Same?", "Other?"]


def test_build_interview_questions_returns_fallback_for_empty_analysis():
    result = interview_builder.build_interview_questions({})

    assert result == interview_builder.FALLBACK_QUESTIONS


def test_document_automation_bot_adds_document_questions():
    result = interview_builder.build_interview_questions(
        {
            "project_type": "document_automation_bot",
            "questions": [],
        },
        max_questions=10,
    )

    assert "Какие форматы документов нужно поддерживать: DOCX, PDF или оба?" in result
    assert "Нужно ли автоматически добавлять печать и подпись?" in result


def test_monitoring_alert_bot_adds_api_webhook_polling_question():
    result = interview_builder.build_interview_questions(
        {
            "project_type": "monitoring_alert_bot",
            "questions": [],
        },
        max_questions=10,
    )

    assert "Откуда получать события: API, webhook или polling?" in result


def test_ticket_notification_bot_adds_events_and_chat_questions():
    result = interview_builder.build_interview_questions(
        {
            "project_type": "ticket_notification_bot",
            "questions": [],
        },
        max_questions=10,
    )

    assert (
        "По каким событиям отправлять уведомления: новая задача, изменение статуса или комментарий?"
        in result
    )
    assert "В какой Telegram чат отправлять уведомления?" in result


def test_internal_ai_assistant_adds_knowledge_source_question():
    result = interview_builder.build_interview_questions(
        {
            "project_type": "internal_ai_assistant",
            "questions": [],
        },
        max_questions=10,
    )

    assert "Откуда ассистент должен брать знания: документы, база знаний или API?" in result


def test_generic_type_does_not_break_function():
    result = interview_builder.build_interview_questions(
        {
            "project_type": "generic_telegram_bot",
            "questions": ["What should it do?"],
        }
    )

    assert result == ["What should it do?"]
