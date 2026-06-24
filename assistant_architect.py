# -*- coding: utf-8 -*-
from typing import Any

from domain_packs import get_domain_pack


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
        pack = get_domain_pack(str(domain_pack.get("name", "generic")))
    else:
        pack = get_domain_pack(domain_pack)

    if not isinstance(idea_analysis, dict):
        idea_analysis = {}

    architecture_notes = _dedupe(
        [
            f"Build a {pack['assistant_type']}.",
            idea_analysis.get("main_goal", ""),
            *idea_analysis.get("required_features", []),
            *_answer_notes(interview_answers),
        ]
    )

    return {
        "assistant_type": pack["assistant_type"],
        "recommended_stack": list(pack["recommended_stack"]),
        "integrations": list(pack["integrations"]),
        "architecture_notes": architecture_notes,
        "production_considerations": list(pack["production_considerations"]),
    }
