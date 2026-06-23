# -*- coding: utf-8 -*-
from typing import Any


REQUIRED_KEYS = (
    "project_type",
    "target_user",
    "main_goal",
    "required_features",
    "recommended_stack",
    "questions",
    "risk_notes",
)


PROJECT_PRESETS: dict[str, dict[str, Any]] = {
    "document_automation_bot": {
        "target_user": "teams that create repeated business documents",
        "main_goal": "automate document generation and delivery through Telegram",
        "required_features": [
            "document template selection",
            "user data collection",
            "DOCX/PDF generation",
            "document delivery in Telegram",
            "document history",
        ],
        "recommended_stack": [
            "Python",
            "aiogram",
            "python-docx",
            "LibreOffice headless",
            "PyMuPDF",
            "SQLite",
        ],
        "questions": [
            "Какие форматы файлов нужно поддерживать: DOCX, PDF или оба?",
            "Нужно ли накладывать печать и подпись автоматически?",
            "Нужно ли хранить историю созданных документов?",
        ],
        "risk_notes": [
            "Ограничить доступ по Telegram ID",
            "Не хранить подписи и печати без защиты",
            "Проверять шаблоны документов перед обработкой",
        ],
    },
    "monitoring_alert_bot": {
        "target_user": "operators and admins who need fast incident alerts",
        "main_goal": "send monitoring alerts to Telegram and reduce missed incidents",
        "required_features": [
            "monitoring event intake",
            "Telegram alert delivery",
            "alert grouping",
            "acknowledgement flow",
            "connection error logging",
        ],
        "recommended_stack": [
            "Python",
            "aiogram",
            "Zabbix API",
            "APScheduler",
            "SQLite",
        ],
        "questions": [
            "Получать события через Zabbix API или webhook?",
            "В какой Telegram чат отправлять уведомления?",
            "Нужно ли группировать повторяющиеся алерты?",
        ],
        "risk_notes": [
            "Не хранить Zabbix credentials в коде",
            "Добавить rate limiting для алертов",
            "Логировать ошибки подключения к Zabbix",
        ],
    },
    "ticket_notification_bot": {
        "target_user": "teams that track tasks and tickets",
        "main_goal": "notify users about ticket assignments and status changes",
        "required_features": [
            "ticket system integration",
            "assignment notifications",
            "status change notifications",
            "user mapping",
            "notification preferences",
        ],
        "recommended_stack": [
            "Python",
            "aiogram",
            "Jira API",
            "APScheduler",
            "SQLite",
        ],
        "questions": [
            "Какая система задач используется: Jira или другая?",
            "Какие статусы должны отправлять уведомления?",
            "Как сопоставлять пользователей Jira и Telegram?",
        ],
        "risk_notes": [
            "Не хранить Jira tokens в коде",
            "Проверять права доступа к проектам и задачам",
            "Ограничить частоту уведомлений при массовых обновлениях",
        ],
    },
    "internal_ai_assistant": {
        "target_user": "employees who need answers from internal knowledge",
        "main_goal": "answer routine questions using internal instructions and FAQ",
        "required_features": [
            "knowledge base ingestion",
            "question answering",
            "source references",
            "admin-only content updates",
            "fallback answer for unknown topics",
        ],
        "recommended_stack": [
            "Python",
            "aiogram",
            "OpenAI or Anthropic API",
            "SQLite",
            "vector search",
        ],
        "questions": [
            "Где хранятся FAQ, регламенты и инструкции?",
            "Нужно ли показывать источник ответа?",
            "Кто сможет обновлять базу знаний?",
        ],
        "risk_notes": [
            "Не отправлять чувствительные данные без проверки доступа",
            "Добавить список разрешенных Telegram ID",
            "Логировать вопросы без секретов и персональных данных",
        ],
    },
    "generic_telegram_bot": {
        "target_user": "Telegram users",
        "main_goal": "build a practical Telegram bot from the described idea",
        "required_features": [
            "start command",
            "guided user interaction",
            "basic persistence",
            "admin configuration",
        ],
        "recommended_stack": [
            "Python",
            "aiogram",
            "SQLite",
            "python-dotenv",
        ],
        "questions": [
            "Кто будет основным пользователем бота?",
            "Какие команды нужны в первой версии?",
            "Нужно ли хранить данные пользователей?",
        ],
        "risk_notes": [
            "Ограничить доступ к административным функциям",
            "Не хранить токены и секреты в коде",
            "Добавить обработку ошибок и логирование",
        ],
    },
}


KEYWORDS = {
    "document_automation_bot": (
        "word",
        "docx",
        "pdf",
        "документ",
        "заявка",
        "акт",
        "счет",
        "счёт",
        "печать",
        "подпись",
    ),
    "monitoring_alert_bot": (
        "zabbix",
        "камера",
        "упала",
        "мониторинг",
        "alert",
        "сервис недоступен",
    ),
    "ticket_notification_bot": (
        "jira",
        "задача",
        "тикет",
        "issue",
        "назначили",
        "статус",
    ),
    "internal_ai_assistant": (
        "ассистент",
        "помощник",
        "faq",
        "регламент",
        "инструкция",
        "отвечал на вопросы",
    ),
}


def _detect_project_type(idea_text: str) -> str:
    normalized_text = idea_text.lower()
    for project_type, keywords in KEYWORDS.items():
        if any(keyword in normalized_text for keyword in keywords):
            return project_type
    return "generic_telegram_bot"


def analyze_project_idea(idea_text: str) -> dict:
    project_type = _detect_project_type(idea_text or "")
    preset = PROJECT_PRESETS[project_type]

    return {
        "project_type": project_type,
        "target_user": preset["target_user"],
        "main_goal": preset["main_goal"],
        "required_features": list(preset["required_features"]),
        "recommended_stack": list(preset["recommended_stack"]),
        "questions": list(preset["questions"]),
        "risk_notes": list(preset["risk_notes"]),
    }
