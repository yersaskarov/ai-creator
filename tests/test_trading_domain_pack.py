import agent_blueprint
import ai_generator
import domain_packs
import interview_builder
from assistant_architect import build_assistant_architecture
from idea_analyzer import analyze_project_idea


def _trading_flow(idea):
    idea_analysis = analyze_project_idea(idea)
    domain_pack = domain_packs.get_domain_pack(idea_analysis["domain"])
    questions = interview_builder.build_interview_questions(idea_analysis, max_questions=10)
    answers = [
        {
            "question": questions[0],
            "answer": "Track TradingView alerts and manual trades for a prop firm account.",
        }
    ]
    architecture = build_assistant_architecture(domain_pack, idea_analysis, answers)
    blueprint = agent_blueprint.build_agent_blueprint(
        idea,
        domain_pack,
        idea_analysis,
        answers,
        architecture,
    )
    return idea_analysis, domain_pack, questions, architecture, blueprint


def test_detects_trading_domain_pack():
    result = domain_packs.detect_domain_pack(
        "Build a TradingView alert bot for XAUUSD forex prop firm risk tracking.",
        {},
    )

    assert result == "trading"


def test_trading_interview_generation_uses_domain_pack():
    idea_analysis = {
        "domain": "trading",
        "project_type": "trading_assistant_bot",
    }

    questions = interview_builder.build_interview_questions(idea_analysis, max_questions=10)

    assert questions == domain_packs.get_domain_pack("trading")["interview_questions"]
    assert "Is TradingView used?" in questions
    assert "Should the assistant calculate statistics?" in questions


def test_trading_architecture_generation_uses_pack_components():
    _, domain_pack, _, architecture, _ = _trading_flow(
        "Need a trading journal assistant for FTMO with RR, winrate, and drawdown."
    )

    assert domain_pack["assistant_type"] == "Trading Assistant"
    assert architecture["assistant_type"] == "Trading Assistant"
    assert "TradingView Webhook Receiver" in architecture["recommended_stack"]
    assert "Statistics Engine" in architecture["recommended_stack"]
    assert "News Calendar Integration" in architecture["recommended_stack"]


def test_trading_blueprint_generation_contains_trading_defaults():
    _, _, _, _, blueprint = _trading_flow(
        "TradingView alert bot for EURUSD and XAUUSD with trade journal and daily loss alerts."
    )

    assert "TradingView alerts" in blueprint["inputs"]
    assert "Manual trade entries" in blueprint["inputs"]
    assert "Trade journal" in blueprint["outputs"]
    assert "Calculate RR" in blueprint["agent_actions"]
    assert "Calculate winrate" in blueprint["agent_actions"]
    assert "Track daily loss" in blueprint["agent_actions"]
    assert "Never store broker credentials" in blueprint["security_notes"]
    assert "Protect webhook secrets" in blueprint["security_notes"]
    assert "RR calculations are correct" in blueprint["acceptance_criteria"]
    assert "Daily drawdown is tracked" in blueprint["acceptance_criteria"]


def test_trading_prompt_enrichment_contains_domain_architecture_and_blueprint():
    _, domain_pack, questions, architecture, blueprint = _trading_flow(
        "Build a TradingView alert bot and prop firm trade journal for XAUUSD."
    )

    prompt = ai_generator._build_generation_prompt(
        {
            "project_name": "Trading Assistant",
            "custom_idea": "Build a TradingView alert bot and prop firm trade journal for XAUUSD.",
            "domain_pack": domain_pack,
            "interview_questions": questions,
            "assistant_architecture": architecture,
            "agent_blueprint": blueprint,
        }
    )

    assert "## Domain Context" in prompt
    assert "trading" in prompt
    assert "## Recommended Architecture" in prompt
    assert "TradingView Webhook Receiver" in prompt
    assert "## Agent Blueprint" in prompt
    assert "Trade journal stores trades" in prompt
    assert "Never store broker credentials" in prompt
