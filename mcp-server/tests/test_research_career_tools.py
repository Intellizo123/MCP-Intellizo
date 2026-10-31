"""Tests for careers and research tools."""

from tools.career_tools import get_careers
from tools.research_tools import get_research_articles


def test_get_careers():
    """Scenario 8: Retrieve career information."""
    res = get_careers()
    assert "career.html" in res["careers_page_url"]
    assert "Tech" in res["filters_supported"]["departments"]
    assert "Design" in res["filters_supported"]["departments"]
    assert len(res["openings"]) >= 2

    titles = [op["title"] for op in res["openings"]]
    assert "Custom Software Engineer" in titles
    assert "UI / UX Designer" in titles

    se = next(op for op in res["openings"] if op["title"] == "Custom Software Engineer")
    assert se["location"] == "Bhubaneswar"
    assert se["experience"] == "5–10 Years"
    assert len(se["responsibilities"]) >= 4
    assert any("JavaScript" in sk for sk in se["required_skills"])

    # Time sensitivity warning
    assert "time-sensitive" in res["time_sensitivity_warning"].lower()


def test_get_research_articles():
    """Scenario 9: Retrieve research articles."""
    res = get_research_articles()
    assert len(res["articles"]) >= 6

    titles = [a["title"] for a in res["articles"]]
    assert any("Sovereign AI" in t for t in titles)
    assert any("Efficiency Dividend" in t for t in titles)
    assert any("10x Developer" in t for t in titles)
    assert any("From Debt to Value" in t for t in titles)
    assert any("Digital Ecosystems" in t for t in titles)
    assert any("APIs, ERP" in t for t in titles)

    for a in res["articles"]:
        assert a["url"].startswith("https://")
        assert len(a["date"]) == 10
        assert "min" in a["read_time"]
        assert len(a["summary"]) > 20

    # Cards
    assert len(res["homepage_research_cards"]) >= 6
    assert len(res["service_page_research_cards"]) >= 3

    # Guardrails
    assert "Never invent" in res["guardrails_notice"]
    assert "article claims" in res["note"]
