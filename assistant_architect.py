# -*- coding: utf-8 -*-
from typing import Any

from domain_packs import get_domain_pack


ASSISTANT_TYPES = {
    "logistics": "logistics_document_assistant",
    "document_automation": "document_automation_assistant",
    "jira": "jira_workflow_assistant",
    "zabbix": "monitoring_alert_assistant",
    "knowledge_assistant": "internal_knowledge_assistant",
    "generic": "general_work_assistant",
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


def _answer_notes(interview_answers: Any) -> list[str]:
    if not isinstance(interview_answers, list):
        return []

    notes = []
    for item in interview_answers:
        if not isinstance(item, dict):
            continue
        question = str(item.get("question", "")).strip()
        answer = str(item.get("answer", "")).strip()
        if question and answer:
            notes.append(f"User clarified: {question} -> {answer}")
    return notes


def build_assistant_architecture(
    domain_pack: str | dict[str, Any],
    idea_analysis: dict[str, Any] | None,
    interview_answers: list[dict[str, str]] | None,
) -> dict[str, Any]:
    if isinstance(domain_pack, dict):
        pack_name = str(domain_pack.get("name", "generic"))
        pack = get_domain_pack(pack_name)
    else:
        pack = get_domain_pack(domain_pack)
        pack_name = pack["name"]

    if not isinstance(idea_analysis, dict):
        idea_analysis = {}

    recommended_stack = _dedupe(
        [
            *pack["recommended_stack"],
            *idea_analysis.get("recommended_stack", []),
        ]
    )
    integrations = _dedupe(pack["integrations"])

    architecture_notes = _dedupe(
        [
            f"Build a {ASSISTANT_TYPES.get(pack_name, ASSISTANT_TYPES['generic'])}.",
            idea_analysis.get("main_goal", ""),
            *idea_analysis.get("required_features", []),
            *_answer_notes(interview_answers),
        ]
    )
    production_considerations = _dedupe(
        [
            *pack["production_considerations"],
            *idea_analysis.get("risk_notes", []),
        ]
    )

    return {
        "assistant_type": ASSISTANT_TYPES.get(pack_name, ASSISTANT_TYPES["generic"]),
        "recommended_stack": recommended_stack,
        "integrations": integrations,
        "architecture_notes": architecture_notes,
        "production_considerations": production_considerations,
    }
