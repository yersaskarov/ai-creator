# -*- coding: utf-8 -*-
from domain_packs import (
    detect_domain_pack,
    get_analysis_profile,
    get_project_type_for_domain,
)


REQUIRED_KEYS = (
    "domain",
    "project_type",
    "target_user",
    "main_goal",
    "required_features",
    "recommended_stack",
    "questions",
    "risk_notes",
)


def analyze_project_idea(idea_text: str) -> dict:
    domain_name = detect_domain_pack(idea_text or "", None)
    profile = get_analysis_profile(domain_name)

    return {
        "domain": domain_name,
        "project_type": get_project_type_for_domain(domain_name),
        "target_user": profile["target_user"],
        "main_goal": profile["main_goal"],
        "required_features": list(profile["required_features"]),
        "recommended_stack": [],
        "questions": [],
        "risk_notes": [],
    }
