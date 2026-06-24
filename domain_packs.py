# -*- coding: utf-8 -*-
from typing import Any


DOMAIN_PACKS: dict[str, dict[str, Any]] = {
    "logistics": {
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
            "Р»РѕРіРёСЃС‚РёРєР°",
            "РїРѕСЃС‚Р°РІС‰РёРє",
            "РЅР°РєР»Р°РґРЅР°СЏ",
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
        "description": "Assistants that generate, validate, and deliver DOCX/PDF business documents from templates.",
        "keywords": [
            "document",
            "docx",
            "pdf",
            "template",
            "signature",
            "stamp",
            "РґРѕРєСѓРјРµРЅС‚",
            "РїРµС‡Р°С‚СЊ",
            "РїРѕРґРїРёСЃСЊ",
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
        ],
        "recommended_stack": [
            "Python",
            "aiogram",
            "Jira API",
            "webhooks",
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
        "description": "Assistants for Zabbix monitoring alerts, severity routing, and incident acknowledgement.",
        "keywords": [
            "zabbix",
            "monitoring",
            "alert",
            "incident",
            "severity",
            "acknowledgement",
            "РјРѕРЅРёС‚РѕСЂРёРЅРі",
            "Р°Р»РµСЂС‚",
            "РёРЅС†РёРґРµРЅС‚",
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
            "СЂРµРіР»Р°РјРµРЅС‚",
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
    "generic": {
        "description": "Generic assistant project with no strong professional domain detected.",
        "keywords": [],
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
}


def get_domain_pack(domain_name: str) -> dict[str, Any]:
    pack_name = domain_name if domain_name in DOMAIN_PACKS else "generic"
    pack = DOMAIN_PACKS[pack_name]
    return {
        "name": pack_name,
        "description": pack["description"],
        "keywords": list(pack["keywords"]),
        "recommended_stack": list(pack["recommended_stack"]),
        "integrations": list(pack["integrations"]),
        "production_considerations": list(pack["production_considerations"]),
    }


def detect_domain_pack(custom_idea: str, idea_analysis: dict[str, Any] | None) -> str:
    if isinstance(idea_analysis, dict):
        project_type = idea_analysis.get("project_type")
        if project_type in PROJECT_TYPE_TO_DOMAIN:
            return PROJECT_TYPE_TO_DOMAIN[project_type]

    text = (custom_idea or "").casefold()
    if isinstance(idea_analysis, dict):
        analysis_parts = [
            str(idea_analysis.get("project_type", "")),
            str(idea_analysis.get("target_user", "")),
            str(idea_analysis.get("main_goal", "")),
            " ".join(str(item) for item in idea_analysis.get("required_features", []) if item),
            " ".join(str(item) for item in idea_analysis.get("recommended_stack", []) if item),
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
    return best_domain if best_score >= 2 else "generic"
