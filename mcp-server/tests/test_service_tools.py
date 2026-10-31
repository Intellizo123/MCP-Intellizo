"""Tests for services MCP tools."""

from tools.service_tools import get_service_details, get_services


def test_get_services_all_six():
    """Scenario 2: Retrieve all six services."""
    res = get_services()
    assert res["total_services"] == 6
    assert len(res["services"]) == 6

    expected_services = [
        "System Design & Consultancy",
        "Web Application Development",
        "Mobile & Smart TV App Development",
        "AI Development & Integration",
        "Indoor Navigation Solutions",
        "Blockchain & NFT Development",
    ]

    returned_names = [s["name"] for s in res["services"]]
    assert returned_names == expected_services

    # Verify each service has summary, capabilities, and source URL
    for s in res["services"]:
        assert len(s["summary"]) > 10
        assert len(s["capabilities"]) > 0
        assert s["source_url"].startswith("https://")


def test_get_service_details_exact():
    """Scenario 3: Retrieve individual service information with exact name."""
    res = get_service_details("Indoor Navigation Solutions")
    assert res["found"] is True
    assert res["matched_official_name"] == "Indoor Navigation Solutions"
    assert "Indoor Mapping & Digital Layouts" in res["capabilities"]
    assert "indoornavigation.html" in res["source_url"]


def test_get_service_details_smart_tv():
    """Scenario 3: Retrieve Smart TV app development with partial query."""
    res = get_service_details("smart tv")
    assert res["found"] is True
    assert res["matched_official_name"] == "Mobile & Smart TV App Development"
    assert "Tizen" in res["smart_tv_platforms"]
    assert "OTT streaming" in res["smart_tv_use_cases"]


def test_get_service_details_approximate_matches():
    """Scenario 3: Test various approximate/partial queries."""
    queries = [
        ("web dev", "Web Application Development"),
        ("blockchain", "Blockchain & NFT Development"),
        ("ai", "AI Development & Integration"),
        ("system design", "System Design & Consultancy"),
    ]
    for q, expected_name in queries:
        res = get_service_details(q)
        assert res["found"] is True, f"Failed for query '{q}'"
        assert res["matched_official_name"] == expected_name


def test_get_service_details_unknown():
    """Scenario 10 & 12: Handle unknown service query without fabricating services."""
    res = get_service_details("Quantum Teleportation Service")
    assert res["found"] is False
    assert res["matched_official_name"] is None
    assert "available_services" in res
    assert len(res["available_services"]) == 6


def test_get_service_details_empty():
    """Scenario 10 & 11: Handle empty service name input."""
    res = get_service_details("")
    assert res["found"] is False
    assert "cannot be empty" in res["notes"]
