import domain_packs


def test_detect_domain_pack_logistics():
    result = domain_packs.detect_domain_pack(
        "Need a logistics assistant for supplier documents and audit trail",
        {},
    )

    assert result == "logistics"


def test_detect_domain_pack_jira():
    result = domain_packs.detect_domain_pack(
        "Telegram bot for Jira ticket lifecycle comments and status notifications",
        {},
    )

    assert result == "jira"


def test_detect_domain_pack_zabbix():
    result = domain_packs.detect_domain_pack(
        "Send Zabbix alerts to Telegram with severity levels and acknowledgement",
        {},
    )

    assert result == "zabbix"


def test_detect_domain_pack_fallback_generic_for_low_confidence():
    result = domain_packs.detect_domain_pack("small helper bot", {})

    assert result == "generic"


def test_get_domain_pack_returns_generic_for_unknown_domain():
    result = domain_packs.get_domain_pack("unknown")

    assert result["name"] == "generic"
    assert result["recommended_stack"]
