# -*- coding: utf-8 -*-
from typing import Any


FALLBACK_QUESTIONS = [
    "Кто будет основным пользователем этого бота?",
    "Какие данные бот должен получать на вход?",
    "Какой результат бот должен отдавать?",
    "Нужны ли интеграции с внешними сервисами?",
    "Нужно ли хранить историю действий?",
]

SMART_QUESTIONS_BY_TYPE = {
    "document_automation_bot": [
        "Какие форматы документов нужно поддерживать: DOCX, PDF или оба?",
        "Нужно ли автоматически добавлять печать и подпись?",
    ],
    "monitoring_alert_bot": [
        "Откуда получать события: API, webhook или polling?",
        "Нужно ли группировать повторяющиеся алерты?",
    ],
    "ticket_notification_bot": [
        "По каким событиям отправлять уведомления: новая задача, изменение статуса или комментарий?",
        "В какой Telegram чат отправлять уведомления?",
    ],
    "internal_ai_assistant": [
        "Откуда ассистент должен брать знания: документы, база знаний или API?",
        "Нужно ли ограничивать ответы только внутренними данными?",
    ],
}


def _dedupe_questions(questions: list[str]) -> list[str]:
    seen = set()
    result = []
    for question in questions:
        normalized_question = str(question).strip()
        if not normalized_question:
            continue
        dedupe_key = normalized_question.casefold()
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        result.append(normalized_question)
    return result


def build_interview_questions(
    idea_analysis: dict[str, Any],
    max_questions: int = 5,
) -> list[str]:
    if max_questions <= 0:
        return []

    if not isinstance(idea_analysis, dict):
        idea_analysis = {}

    raw_questions = idea_analysis.get("questions") or FALLBACK_QUESTIONS
    if not isinstance(raw_questions, list):
        raw_questions = FALLBACK_QUESTIONS

    project_type = idea_analysis.get("project_type")
    smart_questions = SMART_QUESTIONS_BY_TYPE.get(project_type, [])

    questions = _dedupe_questions([*raw_questions, *smart_questions])
    if not questions:
        questions = _dedupe_questions(FALLBACK_QUESTIONS)

    return questions[:max_questions]
