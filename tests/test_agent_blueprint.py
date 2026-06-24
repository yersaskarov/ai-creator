import agent_blueprint
import domain_packs
from assistant_architect import build_assistant_architecture
from idea_analyzer import analyze_project_idea


def _blueprint_for(idea):
    idea_analysis = analyze_project_idea(idea)
    domain_pack = domain_packs.get_domain_pack(idea_analysis["domain"])
    architecture = build_assistant_architecture(domain_pack, idea_analysis, [])
    return agent_blueprint.build_agent_blueprint(
        idea,
        domain_pack,
        idea_analysis,
        [],
        architecture,
    )


def test_blueprint_contains_all_required_keys():
    blueprint = _blueprint_for("Telegram bot for Jira ticket status notifications.")

    assert set(blueprint) == set(agent_blueprint.BLUEPRINT_KEYS)


def test_zabbix_idea_produces_long_down_acceptance_criteria():
    blueprint = _blueprint_for("Send Zabbix alerts to Telegram when camera is down.")

    assert "Zabbix API" in blueprint["inputs"]
    assert "long-down device list" in blueprint["outputs"]
    assert any("5 days" in item for item in blueprint["acceptance_criteria"])


def test_logistics_document_idea_produces_docx_pdf_stamp_signature_blueprint():
    blueprint = _blueprint_for(
        "Need logistics assistant for supplier documents with stamp signature PDF workflow."
    )

    assert "DOCX template" in blueprint["inputs"]
    assert "generated PDF" in blueprint["outputs"]
    assert "apply stamp/signature" in blueprint["agent_actions"]
    assert any("stamp/signature" in item for item in blueprint["security_notes"])


def test_jira_idea_produces_issue_notifications_blueprint():
    blueprint = _blueprint_for("Jira issue webhook for comments and status notifications.")

    assert "Jira webhook/API" in blueprint["inputs"]
    assert "Telegram notifications" in blueprint["outputs"]
    assert "notify on comments" in blueprint["agent_actions"]
    assert any("assigned issues" in item for item in blueprint["acceptance_criteria"])


def test_knowledge_assistant_idea_produces_source_reference_security_blueprint():
    blueprint = _blueprint_for("Internal knowledge assistant for FAQ and policy documents.")

    assert "documents" in blueprint["inputs"]
    assert "answers with source references" in blueprint["outputs"]
    assert any("internal data" in item for item in blueprint["security_notes"])
    assert any("source references" in item for item in blueprint["acceptance_criteria"])


def test_generic_fallback_works():
    blueprint = _blueprint_for("Small helper bot for a team.")

    assert "user messages" in blueprint["inputs"]
    assert "happy path works from /start to final response" in blueprint["acceptance_criteria"]


def test_empty_inputs_do_not_crash():
    blueprint = agent_blueprint.build_agent_blueprint("", {}, {}, [], {})

    assert set(blueprint) == set(agent_blueprint.BLUEPRINT_KEYS)
    assert blueprint["problem_statement"]
    assert blueprint["target_users"]
