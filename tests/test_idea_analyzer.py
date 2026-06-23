import idea_analyzer


REQUIRED_KEYS = {
    "project_type",
    "target_user",
    "main_goal",
    "required_features",
    "recommended_stack",
    "questions",
    "risk_notes",
}

LIST_KEYS = {
    "required_features",
    "recommended_stack",
    "questions",
    "risk_notes",
}


def test_document_idea_is_detected_as_document_automation_bot():
    result = idea_analyzer.analyze_project_idea(
        "Нужен бот, который заполняет docx договор, делает PDF и ставит печать."
    )

    assert result["project_type"] == "document_automation_bot"


def test_zabbix_camera_idea_is_detected_as_monitoring_alert_bot():
    result = idea_analyzer.analyze_project_idea(
        "Бот должен проверять Zabbix и писать, если камера упала."
    )

    assert result["project_type"] == "monitoring_alert_bot"


def test_jira_idea_is_detected_as_ticket_notification_bot():
    result = idea_analyzer.analyze_project_idea(
        "Хочу уведомления, когда в Jira назначили задачу или поменяли статус."
    )

    assert result["project_type"] == "ticket_notification_bot"


def test_assistant_faq_idea_is_detected_as_internal_ai_assistant():
    result = idea_analyzer.analyze_project_idea(
        "Нужен внутренний ассистент, который отвечал на вопросы по FAQ и регламентам."
    )

    assert result["project_type"] == "internal_ai_assistant"


def test_unknown_idea_falls_back_to_generic_telegram_bot():
    result = idea_analyzer.analyze_project_idea("Хочу небольшой бот для команды.")

    assert result["project_type"] == "generic_telegram_bot"


def test_empty_idea_does_not_break_analysis():
    result = idea_analyzer.analyze_project_idea("")

    assert result["project_type"] == "generic_telegram_bot"


def test_result_always_contains_required_keys():
    result = idea_analyzer.analyze_project_idea("jira status bot")

    assert set(result.keys()) == REQUIRED_KEYS


def test_collection_fields_are_always_lists():
    result = idea_analyzer.analyze_project_idea("unknown idea")

    for key in LIST_KEYS:
        assert isinstance(result[key], list)
