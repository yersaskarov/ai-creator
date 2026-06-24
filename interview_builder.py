# -*- coding: utf-8 -*-
from typing import Any

from domain_packs import (
    GENERIC_INTERVIEW_QUESTIONS,
    detect_domain_pack,
    get_domain_pack,
)


FALLBACK_QUESTIONS = list(GENERIC_INTERVIEW_QUESTIONS)


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

    domain_name = detect_domain_pack("", idea_analysis)
    if domain_name == "generic":
        questions = FALLBACK_QUESTIONS
    else:
        questions = get_domain_pack(domain_name)["interview_questions"]

    return _dedupe_questions(questions)[:max_questions]
