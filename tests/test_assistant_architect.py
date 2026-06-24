import assistant_architect
import domain_packs


def test_build_assistant_architecture_generates_domain_architecture():
    architecture = assistant_architect.build_assistant_architecture(
        domain_packs.get_domain_pack("jira"),
        {
            "main_goal": "notify teams about ticket changes",
            "required_features": ["assignment notifications"],
            "recommended_stack": ["APScheduler"],
        },
        [
            {
                "question": "Which statuses matter?",
                "answer": "In progress and blocked",
            }
        ],
    )

    assert architecture["assistant_type"] == "jira_workflow_assistant"
    assert "Jira API" in architecture["recommended_stack"]
    assert "APScheduler" in architecture["recommended_stack"]
    assert "Jira webhooks" in architecture["integrations"]
    assert any("In progress and blocked" in note for note in architecture["architecture_notes"])
    assert "Store Jira tokens only in environment variables." in architecture["production_considerations"]


def test_build_assistant_architecture_uses_assistant_type_from_domain_pack():
    architecture = assistant_architect.build_assistant_architecture(
        domain_packs.get_domain_pack("logistics"),
        {"main_goal": "process supplier documents"},
        [],
    )

    assert architecture["assistant_type"] == domain_packs.get_domain_pack("logistics")["assistant_type"]


def test_build_assistant_architecture_handles_empty_answers():
    architecture = assistant_architect.build_assistant_architecture(
        "zabbix",
        {"main_goal": "send alerts", "required_features": []},
        [],
    )

    assert architecture["assistant_type"] == "monitoring_alert_assistant"
    assert architecture["architecture_notes"]
    assert all("User clarified" not in note for note in architecture["architecture_notes"])


def test_build_assistant_architecture_handles_unknown_domain():
    architecture = assistant_architect.build_assistant_architecture(
        "unknown",
        {},
        None,
    )

    assert architecture["assistant_type"] == "general_work_assistant"
    assert "Python" in architecture["recommended_stack"]
    assert architecture["production_considerations"]
