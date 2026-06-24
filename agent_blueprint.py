# -*- coding: utf-8 -*-
from typing import Any


BLUEPRINT_KEYS = (
    "problem_statement",
    "target_users",
    "inputs",
    "outputs",
    "agent_actions",
    "integrations",
    "data_storage",
    "security_notes",
    "deployment_notes",
    "acceptance_criteria",
)


DOMAIN_DEFAULTS: dict[str, dict[str, list[str]]] = {
    "zabbix": {
        "inputs": ["Zabbix API", "host/item status", "trigger events"],
        "outputs": ["Telegram alerts", "daily summary", "long-down device list"],
        "agent_actions": [
            "check current status",
            "track first_seen_down",
            "group repeated alerts",
        ],
        "data_storage": ["alert history", "first_seen_down timestamps", "acknowledgements"],
        "security_notes": [
            "do not store credentials in code",
            "restrict Telegram chat",
        ],
        "deployment_notes": ["run scheduled checks in a worker or polling loop"],
        "acceptance_criteria": [
            "unavailable cameras must stay visible even after 5 days",
            "repeated alerts are grouped instead of flooding the chat",
        ],
    },
    "logistics": {
        "inputs": [
            "DOCX template",
            "supplier data",
            "date",
            "bank details",
            "stamp/signature image",
        ],
        "outputs": ["generated PDF", "filled DOCX"],
        "agent_actions": [
            "replace placeholders",
            "convert DOCX to PDF",
            "apply stamp/signature",
        ],
        "data_storage": ["document templates", "generated document history", "audit trail"],
        "security_notes": [
            "restrict access",
            "protect stamp/signature files",
        ],
        "deployment_notes": ["install document conversion dependencies on the server"],
        "acceptance_criteria": [
            "generated PDF contains correct supplier/date/bank fields",
            "stamp/signature files are never exposed in generated source code",
        ],
    },
    "document_automation": {
        "inputs": [
            "DOCX template",
            "supplier data",
            "date",
            "bank details",
            "stamp/signature image",
        ],
        "outputs": ["generated PDF", "filled DOCX"],
        "agent_actions": [
            "replace placeholders",
            "convert DOCX to PDF",
            "apply stamp/signature",
        ],
        "data_storage": ["document templates", "generated document history"],
        "security_notes": [
            "restrict access",
            "protect stamp/signature files",
        ],
        "deployment_notes": ["document conversion must work in the deployment environment"],
        "acceptance_criteria": [
            "generated PDF contains correct supplier/date/bank fields",
            "filled DOCX keeps the selected template structure",
        ],
    },
    "jira": {
        "inputs": ["Jira webhook/API", "issue events"],
        "outputs": ["Telegram notifications", "issue summary"],
        "agent_actions": [
            "notify on new task",
            "notify on status change",
            "notify on comments",
        ],
        "data_storage": ["issue-to-message mapping", "user notification preferences"],
        "security_notes": ["do not expose Jira token"],
        "deployment_notes": ["configure webhook endpoint or scheduled Jira polling"],
        "acceptance_criteria": [
            "assigned issues are delivered to Telegram",
            "status changes include issue key and new status",
        ],
    },
    "knowledge_assistant": {
        "inputs": ["documents", "FAQ", "internal knowledge base"],
        "outputs": ["answers with source references"],
        "agent_actions": [
            "search knowledge",
            "summarize answer",
            "ask clarifying question",
        ],
        "data_storage": ["indexed knowledge chunks", "source metadata"],
        "security_notes": ["restrict answers to internal data"],
        "deployment_notes": ["prepare a repeatable knowledge update process"],
        "acceptance_criteria": [
            "assistant refuses unknown answers instead of hallucinating",
            "answers include source references when available",
        ],
    },
    "trading": {
        "inputs": [
            "TradingView alerts",
            "Manual trade entries",
            "Economic calendar data",
        ],
        "outputs": [
            "Telegram notifications",
            "Trade journal",
            "Statistics reports",
            "Weekly review",
        ],
        "agent_actions": [
            "Track trades",
            "Calculate RR",
            "Calculate winrate",
            "Track daily loss",
            "Generate reports",
        ],
        "data_storage": [
            "trade journal entries",
            "TradingView alert history",
            "risk and drawdown metrics",
            "weekly review snapshots",
        ],
        "security_notes": [
            "Never store broker credentials",
            "Never auto-trade without explicit approval",
            "Protect webhook secrets",
        ],
        "deployment_notes": [
            "run webhook receiver behind HTTPS",
            "store risk settings in environment or admin configuration",
        ],
        "acceptance_criteria": [
            "Trade journal stores trades",
            "Statistics are reproducible",
            "RR calculations are correct",
            "Daily drawdown is tracked",
        ],
    },
    "generic": {
        "inputs": ["user messages", "configuration values"],
        "outputs": ["Telegram responses", "generated result"],
        "agent_actions": [
            "collect user input",
            "validate required fields",
            "return a useful result",
        ],
        "data_storage": ["basic user state", "operation history"],
        "security_notes": ["store secrets in environment variables", "validate user input"],
        "deployment_notes": ["document local and server startup steps"],
        "acceptance_criteria": [
            "happy path works from /start to final response",
            "invalid input receives a helpful message",
        ],
    },
}


def _dedupe(items: list[Any]) -> list[str]:
    result = []
    seen = set()
    for item in items:
        text = str(item).strip()
        if not text:
            continue
        key = text.casefold()
        if key in seen:
            continue
        seen.add(key)
        result.append(text)
    return result


def _domain_name(domain_pack: Any) -> str:
    if isinstance(domain_pack, dict):
        name = str(domain_pack.get("name", "generic")).strip()
        return name if name in DOMAIN_DEFAULTS else "generic"
    return "generic"


def _answer_lines(interview_answers: Any) -> list[str]:
    if not isinstance(interview_answers, list):
        return []

    lines = []
    for item in interview_answers:
        if isinstance(item, dict):
            question = str(item.get("question", "")).strip()
            answer = str(item.get("answer", "")).strip()
            if question and answer:
                lines.append(f"{question}: {answer}")
        elif str(item).strip():
            lines.append(str(item).strip())
    return lines


def build_agent_blueprint(
    custom_idea: str,
    domain_pack: dict,
    idea_analysis: dict,
    interview_answers: list[str],
    assistant_architecture: dict,
) -> dict[str, Any]:
    if not isinstance(domain_pack, dict):
        domain_pack = {}
    if not isinstance(idea_analysis, dict):
        idea_analysis = {}
    if not isinstance(assistant_architecture, dict):
        assistant_architecture = {}

    domain_name = _domain_name(domain_pack)
    defaults = DOMAIN_DEFAULTS[domain_name]

    problem = str(custom_idea or "").strip()
    if not problem:
        problem = str(idea_analysis.get("main_goal", "")).strip()
    if not problem:
        problem = str(domain_pack.get("description", "")).strip()
    if not problem:
        problem = "Build a practical assistant for the described workflow."

    target_users = _dedupe(
        [
            idea_analysis.get("target_user", ""),
            domain_pack.get("description", ""),
        ]
    )
    architecture_notes = assistant_architecture.get("architecture_notes", [])
    if not isinstance(architecture_notes, list):
        architecture_notes = []

    integrations = _dedupe(
        [
            *domain_pack.get("integrations", []),
            *assistant_architecture.get("integrations", []),
        ]
    )
    security_notes = _dedupe(
        [
            *defaults["security_notes"],
            *domain_pack.get("production_considerations", []),
            *assistant_architecture.get("production_considerations", []),
        ]
    )

    answer_notes = _answer_lines(interview_answers)
    acceptance_criteria = _dedupe(
        [
            *defaults["acceptance_criteria"],
            *[f"User clarification is reflected: {answer}" for answer in answer_notes],
        ]
    )

    return {
        "problem_statement": problem,
        "target_users": target_users or ["project user"],
        "inputs": _dedupe(defaults["inputs"]),
        "outputs": _dedupe(defaults["outputs"]),
        "agent_actions": _dedupe([*defaults["agent_actions"], *architecture_notes]),
        "integrations": integrations or _dedupe(defaults.get("integrations", [])),
        "data_storage": _dedupe(defaults["data_storage"]),
        "security_notes": security_notes,
        "deployment_notes": _dedupe(defaults["deployment_notes"]),
        "acceptance_criteria": acceptance_criteria,
    }
