"""Tests for AI and MCP tools."""

from tools.ai_tools import get_ai_capabilities, get_mcp_information


def test_get_ai_capabilities():
    """Scenario 5: Retrieve AI capabilities."""
    res = get_ai_capabilities()
    assert "Computer Vision Systems" in res["ai_development_capabilities"][1]
    assert len(res["ai_strategy_capabilities"]) >= 8
    assert res["ai_development_url"].startswith("https://")

    # Verify all 6 AI agent pillars
    expected_pillars = [
        "Observe & Monitor",
        "Analyze & Reason",
        "Recommend & Support Decisions",
        "Automate & Execute",
        "Learn & Improve Over Time",
        "Communicate & Collaborate",
    ]
    pillar_names = [p["name"] for p in res["ai_agents_capabilities"]]
    assert pillar_names == expected_pillars

    # Integration environments
    assert "ERP and CRM systems" in res["ai_agents_integration_environments"]
    assert "Business dashboards" in res["ai_agents_integration_environments"]

    # AI Agents FAQ
    assert len(res["ai_agents_faq"]) >= 5
    assert "Are these AI agents pre-built products?" in res["ai_agents_faq"][0]["q"]

    # AI visibility
    assert "Reveal how LLMs talk about your brand" in res["ai_visibility"]["tagline"]
    assert "guardrails_notice" in res


def test_get_mcp_information():
    """Scenario 6: Retrieve MCP information preserving exact published expansion."""
    res = get_mcp_information()
    assert res["title"] == "MCP by Intellizo"
    # Mandatory requirement: preserve exact published expansion
    assert res["expansion_as_published"] == "Model Context & Orchestration Layer"
    assert "intelligence layer that connects AI to your business context" in res["summary"]
    assert res["source_url"] == "https://intellizosoftwares.com/mcp.html"

    # Use cases
    assert len(res["use_cases"]) == 3
    assert any("Unlock insights anywhere" in uc for uc in res["use_cases"])

    # Environments
    assert "Claude" in res["integration_environments_named"]
    assert "Cursor" in res["integration_environments_named"]
    assert "GitHub" in res["integration_environments_named"]
    assert "OpenAI" in res["integration_environments_named"]
    assert "Model Context Protocol" in res["integration_environments_named"]

    # Notice
    assert "Website wording, not a verified compatibility matrix" in res["environments_note"]

    # FAQ
    assert len(res["faq"]) == 4
    faq_questions = [f["q"] for f in res["faq"]]
    assert "What models power Agents?" in faq_questions
    assert "How are Agents priced?" in faq_questions
