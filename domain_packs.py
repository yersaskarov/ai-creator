# -*- coding: utf-8 -*-
from typing import Any


GENERIC_INTERVIEW_QUESTIONS = [
    "РљС‚Рѕ Р±СѓРґРµС‚ РѕСЃРЅРѕРІРЅС‹Рј РїРѕР»СЊР·РѕРІР°С‚РµР»РµРј СЌС‚РѕРіРѕ Р±РѕС‚Р°?",
    "РљР°РєРёРµ РґР°РЅРЅС‹Рµ Р±РѕС‚ РґРѕР»Р¶РµРЅ РїРѕР»СѓС‡Р°С‚СЊ РЅР° РІС…РѕРґ?",
    "РљР°РєРѕР№ СЂРµР·СѓР»СЊС‚Р°С‚ Р±РѕС‚ РґРѕР»Р¶РµРЅ РѕС‚РґР°РІР°С‚СЊ?",
    "РќСѓР¶РЅС‹ Р»Рё РёРЅС‚РµРіСЂР°С†РёРё СЃ РІРЅРµС€РЅРёРјРё СЃРµСЂРІРёСЃР°РјРё?",
    "РќСѓР¶РЅРѕ Р»Рё С…СЂР°РЅРёС‚СЊ РёСЃС‚РѕСЂРёСЋ РґРµР№СЃС‚РІРёР№?",
]


DOMAIN_PACKS: dict[str, dict[str, Any]] = {
    "logistics": {
        "name": "logistics",
        "description": "Assistants for logistics, supplier documents, shipment paperwork, and operational document checks.",
        "keywords": [
            "logistics",
            "shipment",
            "supplier",
            "warehouse",
            "invoice",
            "delivery",
            "cargo",
            "audit trail",
            "supplier documents",
            "template processing",
            "Р»РѕРіРёСЃС‚РёРєР°",
            "РїРѕСЃС‚Р°РІС‰РёРє",
            "РЅР°РєР»Р°РґРЅР°СЏ",
        ],
        "assistant_type": "logistics_document_assistant",
        "interview_questions": [
            "РљР°РєРёРµ РґРѕРєСѓРјРµРЅС‚С‹ РЅСѓР¶РЅРѕ РѕР±СЂР°Р±Р°С‚С‹РІР°С‚СЊ: РЅР°РєР»Р°РґРЅС‹Рµ, СЃС‡РµС‚Р°, Р°РєС‚С‹ РёР»Рё Р·Р°СЏРІРєРё?",
            "РќСѓР¶РµРЅ Р»Рё audit trail РґР»СЏ РёР·РјРµРЅРµРЅРёР№ Рё СЃРѕР·РґР°РЅРЅС‹С… РґРѕРєСѓРјРµРЅС‚РѕРІ?",
            "РЎ РєР°РєРёРјРё С€Р°Р±Р»РѕРЅР°РјРё Рё С„РѕСЂРјР°С‚Р°РјРё РґРѕР»Р¶РµРЅ СЂР°Р±РѕС‚Р°С‚СЊ Р°СЃСЃРёСЃС‚РµРЅС‚?",
        ],
        "recommended_stack": [
            "Python",
            "aiogram",
            "python-docx",
            "PDF workflow",
            "template processing",
            "SQLite",
        ],
        "integrations": [
            "supplier documents",
            "document templates",
            "PDF conversion",
            "audit trail",
        ],
        "production_considerations": [
            "Validate uploaded supplier documents before processing.",
            "Keep an audit trail for generated and corrected documents.",
            "Store secrets and document templates outside source code.",
        ],
    },
    "document_automation": {
        "name": "document_automation",
        "description": "Assistants that generate, validate, and deliver DOCX/PDF business documents from templates.",
        "keywords": [
            "document",
            "docx",
            "pdf",
            "template",
            "signature",
            "stamp",
            "word",
            "РґРѕРєСѓРјРµРЅС‚",
            "Р·Р°СЏРІРєР°",
            "Р°РєС‚",
            "СЃС‡РµС‚",
            "СЃС‡С‘С‚",
            "РїРµС‡Р°С‚СЊ",
            "РїРѕРґРїРёСЃСЊ",
        ],
        "assistant_type": "document_automation_assistant",
        "interview_questions": [
            "РљР°РєРёРµ С„РѕСЂРјР°С‚С‹ С„Р°Р№Р»РѕРІ РЅСѓР¶РЅРѕ РїРѕРґРґРµСЂР¶РёРІР°С‚СЊ: DOCX, PDF РёР»Рё РѕР±Р°?",
            "РќСѓР¶РЅРѕ Р»Рё РЅР°РєР»Р°РґС‹РІР°С‚СЊ РїРµС‡Р°С‚СЊ Рё РїРѕРґРїРёСЃСЊ Р°РІС‚РѕРјР°С‚РёС‡РµСЃРєРё?",
            "РќСѓР¶РЅРѕ Р»Рё С…СЂР°РЅРёС‚СЊ РёСЃС‚РѕСЂРёСЋ СЃРѕР·РґР°РЅРЅС‹С… РґРѕРєСѓРјРµРЅС‚РѕРІ?",
        ],
        "recommended_stack": [
            "Python",
            "aiogram",
            "python-docx",
            "LibreOffice headless",
            "PyMuPDF",
            "SQLite",
        ],
        "integrations": [
            "DOCX templates",
            "PDF workflow",
            "file storage",
            "Telegram document delivery",
        ],
        "production_considerations": [
            "Do not hardcode signatures, stamps, or sensitive company data.",
            "Validate templates before rendering user documents.",
            "Add access control for document generation and history.",
        ],
    },
    "jira": {
        "name": "jira",
        "description": "Assistants for Jira ticket lifecycle, comments, status notifications, and team updates.",
        "keywords": [
            "jira",
            "ticket",
            "issue",
            "status",
            "comment",
            "assignee",
            "webhook",
            "Р·Р°РґР°С‡Р°",
            "С‚РёРєРµС‚",
            "СЃС‚Р°С‚СѓСЃ",
            "РЅР°Р·РЅР°С‡РёР»Рё",
        ],
        "assistant_type": "jira_workflow_assistant",
        "interview_questions": [
            "РљР°РєР°СЏ СЃРёСЃС‚РµРјР° Р·Р°РґР°С‡ РёСЃРїРѕР»СЊР·СѓРµС‚СЃСЏ: Jira РёР»Рё РґСЂСѓРіР°СЏ?",
            "РљР°РєРёРµ СЃС‚Р°С‚СѓСЃС‹ РґРѕР»Р¶РЅС‹ РѕС‚РїСЂР°РІР»СЏС‚СЊ СѓРІРµРґРѕРјР»РµРЅРёСЏ?",
            "РљР°Рє СЃРѕРїРѕСЃС‚Р°РІР»СЏС‚СЊ РїРѕР»СЊР·РѕРІР°С‚РµР»РµР№ Jira Рё Telegram?",
            "Р’ РєР°РєРѕР№ Telegram С‡Р°С‚ РѕС‚РїСЂР°РІР»СЏС‚СЊ СѓРІРµРґРѕРјР»РµРЅРёСЏ?",
        ],
        "recommended_stack": [
            "Python",
            "aiogram",
            "Jira API",
            "webhooks",
            "APScheduler",
            "SQLite",
        ],
        "integrations": [
            "Jira API",
            "Jira webhooks",
            "ticket lifecycle",
            "comments",
            "status notifications",
        ],
        "production_considerations": [
            "Store Jira tokens only in environment variables.",
            "Verify user permissions before exposing ticket data.",
            "Debounce bulk ticket updates to avoid notification floods.",
        ],
    },
    "zabbix": {
        "name": "zabbix",
        "description": "Assistants for Zabbix monitoring alerts, severity routing, and incident acknowledgement.",
        "keywords": [
            "zabbix",
            "monitoring",
            "alert",
            "incident",
            "severity",
            "acknowledgement",
            "РєР°РјРµСЂР°",
            "СѓРїР°Р»Р°",
            "РјРѕРЅРёС‚РѕСЂРёРЅРі",
            "СЃРµСЂРІРёСЃ РЅРµРґРѕСЃС‚СѓРїРµРЅ",
            "Р°Р»РµСЂС‚",
        ],
        "assistant_type": "monitoring_alert_assistant",
        "interview_questions": [
            "РџРѕР»СѓС‡Р°С‚СЊ СЃРѕР±С‹С‚РёСЏ С‡РµСЂРµР· Zabbix API РёР»Рё webhook?",
            "Р’ РєР°РєРѕР№ Telegram С‡Р°С‚ РѕС‚РїСЂР°РІР»СЏС‚СЊ СѓРІРµРґРѕРјР»РµРЅРёСЏ?",
            "РќСѓР¶РЅРѕ Р»Рё РіСЂСѓРїРїРёСЂРѕРІР°С‚СЊ РїРѕРІС‚РѕСЂСЏСЋС‰РёРµСЃСЏ Р°Р»РµСЂС‚С‹?",
        ],
        "recommended_stack": [
            "Python",
            "aiogram",
            "Zabbix API",
            "APScheduler",
            "SQLite",
        ],
        "integrations": [
            "Zabbix API",
            "Telegram alerts",
            "severity levels",
            "incident acknowledgement",
        ],
        "production_considerations": [
            "Protect Zabbix credentials and endpoint URLs.",
            "Rate-limit repeated alerts from noisy triggers.",
            "Log acknowledgement actions with user and timestamp.",
        ],
    },
    "knowledge_assistant": {
        "name": "knowledge_assistant",
        "description": "Internal assistants that answer employee questions from policies, FAQ, and knowledge bases.",
        "keywords": [
            "knowledge",
            "faq",
            "policy",
            "assistant",
            "instructions",
            "regulations",
            "Р±Р°Р·Р° Р·РЅР°РЅРёР№",
            "Р°СЃСЃРёСЃС‚РµРЅС‚",
            "РїРѕРјРѕС‰РЅРёРє",
            "СЂРµРіР»Р°РјРµРЅС‚",
            "РёРЅСЃС‚СЂСѓРєС†РёСЏ",
            "РѕС‚РІРµС‡Р°Р» РЅР° РІРѕРїСЂРѕСЃС‹",
        ],
        "assistant_type": "internal_knowledge_assistant",
        "interview_questions": [
            "Р“РґРµ С…СЂР°РЅСЏС‚СЃСЏ FAQ, СЂРµРіР»Р°РјРµРЅС‚С‹ Рё РёРЅСЃС‚СЂСѓРєС†РёРё?",
            "РќСѓР¶РЅРѕ Р»Рё РїРѕРєР°Р·С‹РІР°С‚СЊ РёСЃС‚РѕС‡РЅРёРє РѕС‚РІРµС‚Р°?",
            "РљС‚Рѕ СЃРјРѕР¶РµС‚ РѕР±РЅРѕРІР»СЏС‚СЊ Р±Р°Р·Сѓ Р·РЅР°РЅРёР№?",
        ],
        "recommended_stack": [
            "Python",
            "aiogram",
            "OpenAI or Anthropic API",
            "vector search",
            "SQLite",
        ],
        "integrations": [
            "internal knowledge base",
            "FAQ documents",
            "source references",
            "admin content updates",
        ],
        "production_considerations": [
            "Restrict access to internal content by Telegram ID.",
            "Show source references when possible.",
            "Avoid logging sensitive employee questions verbatim.",
        ],
    },
    "trading": {
        "name": "trading",
        "description": "Assistants for trading journals, prop firm risk tracking, TradingView alerts, smart money workflows, and economic calendar reminders.",
        "keywords": [
            "trading",
            "trader",
            "forex",
            "funding pips",
            "ftmo",
            "the5ers",
            "eurusd",
            "gold",
            "xauusd",
            "smart money",
            "ict",
            "liquidity",
            "fvg",
            "order block",
            "journal",
            "rr",
            "risk reward",
            "winrate",
            "tradingview",
            "prop firm",
        ],
        "assistant_type": "Trading Assistant",
        "interview_questions": [
            "What exactly should the trading assistant do?",
            "Which markets are used?",
            "Which instruments are traded?",
            "Is TradingView used?",
            "Are webhook signals used?",
            "Is a trade journal needed?",
            "Should the assistant calculate statistics?",
            "Are economic news notifications needed?",
            "Are risk and drawdown notifications needed?",
        ],
        "recommended_stack": [
            "Python",
            "aiogram",
            "Telegram Bot",
            "TradingView Webhook Receiver",
            "Trade Journal",
            "SQLite/Postgres",
            "Statistics Engine",
            "News Calendar Integration",
        ],
        "integrations": [
            "TradingView alerts",
            "webhook signals",
            "economic calendar data",
            "Telegram notifications",
        ],
        "production_considerations": [
            "Never store broker credentials in code or generated project files.",
            "Never auto-trade without explicit user approval and separate risk controls.",
            "Protect webhook secrets and validate incoming TradingView payloads.",
        ],
    },
    "generic": {
        "name": "generic",
        "description": "Generic assistant project with no strong professional domain detected.",
        "keywords": [],
        "assistant_type": "general_work_assistant",
        "interview_questions": list(GENERIC_INTERVIEW_QUESTIONS),
        "recommended_stack": [
            "Python",
            "aiogram",
            "SQLite",
            "python-dotenv",
        ],
        "integrations": [
            "Telegram Bot API",
        ],
        "production_considerations": [
            "Keep secrets in environment variables.",
            "Add logging, rate limits, and clear error handling.",
            "Document setup steps for a non-technical user.",
        ],
    },
}


PROJECT_TYPE_TO_DOMAIN = {
    "document_automation_bot": "document_automation",
    "monitoring_alert_bot": "zabbix",
    "ticket_notification_bot": "jira",
    "internal_ai_assistant": "knowledge_assistant",
    "trading_assistant_bot": "trading",
    "generic_telegram_bot": "generic",
}

DOMAIN_TO_PROJECT_TYPE = {
    "document_automation": "document_automation_bot",
    "zabbix": "monitoring_alert_bot",
    "jira": "ticket_notification_bot",
    "knowledge_assistant": "internal_ai_assistant",
    "logistics": "document_automation_bot",
    "trading": "trading_assistant_bot",
    "generic": "generic_telegram_bot",
}

DOMAIN_ANALYSIS_PROFILES = {
    "document_automation": {
        "target_user": "teams that create repeated business documents",
        "main_goal": "automate document generation and delivery through Telegram",
        "required_features": [
            "document template selection",
            "user data collection",
            "DOCX/PDF generation",
            "document delivery in Telegram",
            "document history",
        ],
    },
    "zabbix": {
        "target_user": "operators and admins who need fast incident alerts",
        "main_goal": "send monitoring alerts to Telegram and reduce missed incidents",
        "required_features": [
            "monitoring event intake",
            "Telegram alert delivery",
            "alert grouping",
            "acknowledgement flow",
            "connection error logging",
        ],
    },
    "jira": {
        "target_user": "teams that track tasks and tickets",
        "main_goal": "notify users about ticket assignments and status changes",
        "required_features": [
            "ticket system integration",
            "assignment notifications",
            "status change notifications",
            "user mapping",
            "notification preferences",
        ],
    },
    "knowledge_assistant": {
        "target_user": "employees who need answers from internal knowledge",
        "main_goal": "answer routine questions using internal instructions and FAQ",
        "required_features": [
            "knowledge base ingestion",
            "question answering",
            "source references",
            "admin-only content updates",
            "fallback answer for unknown topics",
        ],
    },
    "logistics": {
        "target_user": "logistics teams that process supplier and shipment documents",
        "main_goal": "automate logistics document handling and reduce manual checks",
        "required_features": [
            "supplier document intake",
            "template-based document generation",
            "PDF/DOCX workflow",
            "audit trail",
            "document delivery in Telegram",
        ],
    },
    "trading": {
        "target_user": "traders, prop firm challengers, and trading teams",
        "main_goal": "track trades, alerts, risk, statistics, and trading reviews through Telegram",
        "required_features": [
            "TradingView alert intake",
            "manual trade journal entries",
            "RR and winrate calculations",
            "daily drawdown tracking",
            "weekly review reports",
        ],
    },
    "generic": {
        "target_user": "Telegram users",
        "main_goal": "build a practical Telegram bot from the described idea",
        "required_features": [
            "start command",
            "guided user interaction",
            "basic persistence",
            "admin configuration",
        ],
    },
}

DOMAIN_MATCH_THRESHOLD = 1


def get_domain_pack(domain_name: str) -> dict[str, Any]:
    pack_name = domain_name if domain_name in DOMAIN_PACKS else "generic"
    pack = DOMAIN_PACKS[pack_name]
    return {
        "name": pack["name"],
        "description": pack["description"],
        "keywords": list(pack["keywords"]),
        "assistant_type": pack["assistant_type"],
        "interview_questions": list(pack["interview_questions"]),
        "recommended_stack": list(pack["recommended_stack"]),
        "integrations": list(pack["integrations"]),
        "production_considerations": list(pack["production_considerations"]),
    }


def get_domain_for_project_type(project_type: str | None) -> str:
    return PROJECT_TYPE_TO_DOMAIN.get(str(project_type or ""), "generic")


def get_project_type_for_domain(domain_name: str) -> str:
    return DOMAIN_TO_PROJECT_TYPE.get(domain_name, "generic_telegram_bot")


def get_analysis_profile(domain_name: str) -> dict[str, Any]:
    profile_name = domain_name if domain_name in DOMAIN_ANALYSIS_PROFILES else "generic"
    profile = DOMAIN_ANALYSIS_PROFILES[profile_name]
    return {
        "target_user": profile["target_user"],
        "main_goal": profile["main_goal"],
        "required_features": list(profile["required_features"]),
    }


def detect_domain_pack(custom_idea: str, idea_analysis: dict[str, Any] | None) -> str:
    if isinstance(idea_analysis, dict):
        domain_name = idea_analysis.get("domain")
        if domain_name in DOMAIN_PACKS:
            return str(domain_name)

        project_type = idea_analysis.get("project_type")
        mapped_domain = get_domain_for_project_type(str(project_type or ""))
        if mapped_domain != "generic":
            return mapped_domain

    text = (custom_idea or "").casefold()
    if isinstance(idea_analysis, dict):
        analysis_parts = [
            str(idea_analysis.get("project_type", "")),
            str(idea_analysis.get("target_user", "")),
            str(idea_analysis.get("main_goal", "")),
            " ".join(str(item) for item in idea_analysis.get("required_features", []) if item),
        ]
        text = f"{text} {' '.join(analysis_parts).casefold()}"

    scores: dict[str, int] = {}
    for domain_name, pack in DOMAIN_PACKS.items():
        if domain_name == "generic":
            continue
        score = sum(1 for keyword in pack["keywords"] if keyword.casefold() in text)
        if score:
            scores[domain_name] = score

    if not scores:
        return "generic"

    best_domain, best_score = max(scores.items(), key=lambda item: item[1])
    return best_domain if best_score >= DOMAIN_MATCH_THRESHOLD else "generic"
