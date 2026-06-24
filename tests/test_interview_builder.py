import interview_builder
from domain_packs import get_domain_pack


def test_build_interview_questions_returns_list_of_strings():
    result = interview_builder.build_interview_questions(
        {"project_type": "ticket_notification_bot"}
    )

    assert isinstance(result, list)
    assert all(isinstance(question, str) for question in result)


def test_build_interview_questions_respects_max_questions():
    result = interview_builder.build_interview_questions(
        {"project_type": "ticket_notification_bot"},
        max_questions=2,
    )

    assert result == get_domain_pack("jira")["interview_questions"][:2]


def test_build_interview_questions_returns_empty_for_zero_limit():
    result = interview_builder.build_interview_questions(
        {"project_type": "ticket_notification_bot"},
        max_questions=0,
    )

    assert result == []


def test_build_interview_questions_returns_fallback_for_empty_analysis():
    result = interview_builder.build_interview_questions({})

    assert result == interview_builder.FALLBACK_QUESTIONS


def test_domain_pack_is_used_for_document_automation_questions():
    result = interview_builder.build_interview_questions(
        {
            "domain": "document_automation",
            "project_type": "document_automation_bot",
        },
        max_questions=10,
    )

    assert result == get_domain_pack("document_automation")["interview_questions"]
    assert any("DOCX" in question for question in result)


def test_domain_pack_is_used_for_zabbix_questions():
    result = interview_builder.build_interview_questions(
        {
            "domain": "zabbix",
            "project_type": "monitoring_alert_bot",
        },
        max_questions=10,
    )

    assert result == get_domain_pack("zabbix")["interview_questions"]
    assert any("Zabbix" in question for question in result)


def test_domain_pack_is_used_for_jira_questions():
    result = interview_builder.build_interview_questions(
        {
            "domain": "jira",
            "project_type": "ticket_notification_bot",
        },
        max_questions=10,
    )

    assert result == get_domain_pack("jira")["interview_questions"]
    assert any("Jira" in question for question in result)


def test_domain_pack_is_used_for_knowledge_assistant_questions():
    result = interview_builder.build_interview_questions(
        {
            "domain": "knowledge_assistant",
            "project_type": "internal_ai_assistant",
        },
        max_questions=10,
    )

    assert result == get_domain_pack("knowledge_assistant")["interview_questions"]


def test_generic_type_uses_fallback_questions():
    result = interview_builder.build_interview_questions(
        {
            "domain": "generic",
            "project_type": "generic_telegram_bot",
        }
    )

    assert result == interview_builder.FALLBACK_QUESTIONS
