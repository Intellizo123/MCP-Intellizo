"""Tests for company profile and navigation tools."""

from tools.company_tools import get_company_navigation, get_company_profile


def test_get_company_profile():
    """Scenario 1: Retrieve company profile."""
    res = get_company_profile()
    assert res["company_name"] == "Intellizo Softwares"
    assert res["tagline"] == "IDEAS ReEngineered"
    assert "software and AI consultancy" in res["description"]
    assert "gloabl" in res["mission"]  # spelling as published
    assert "trusted partner" in res["vision"]
    assert len(res["operating_priorities"]) == 4
    assert "custom_solutions" in res["principles"]
    assert "trust" in res["culture"]["highlights"]
    assert "Asia Pacific" in res["global_presence"]["regions_selectors"]
    assert len(res["teams_overview"]["list"]) >= 7


def test_company_conflicts_reported():
    """Scenario 14: Check conflicting company information."""
    res = get_company_profile()
    conflicts = res["known_conflicts"]
    assert len(conflicts) >= 2
    metric_conflict = next(c for c in conflicts if c["topic"] == "Company metrics")
    assert any("108+ clients" in d for d in metric_conflict["details"])
    assert any("0 for countries" in d for d in metric_conflict["details"])
    assert "disclaimer" in res
    assert "Metric Discrepancy Note" in res["disclaimer"]


def test_get_company_navigation():
    """Scenario 10: Retrieve official website navigation."""
    nav = get_company_navigation()
    assert "https://www.intellizosoftwares.com/" in nav["official_website"]
    assert len(nav["navigation_links"]) >= 15

    areas = [link["area"] for link in nav["navigation_links"]]
    assert "Homepage" in areas
    assert "About" in areas
    assert "Services overview" in areas
    assert "AI Development" in areas
    assert "AI Agents" in areas
    assert "MCP" in areas
    assert "Careers" in areas
    assert "Contact" in areas
    assert "Privacy Policy" in areas


def test_validate_navigation_source_urls():
    """Scenario 13: Validate that all navigation source URLs are properly formatted."""
    nav = get_company_navigation()
    for link in nav["navigation_links"]:
        url = link["url"]
        assert url.startswith("http://") or url.startswith("https://")
        assert "intellizo" in url.lower()
