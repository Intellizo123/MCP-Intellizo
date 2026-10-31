"""Tests for retrieval engine, keyword search, categories, and guardrails."""

import pytest
from services.retrieval_service import retrieval_service


def test_search_company_knowledge_basic():
    """Verify basic search returns relevant items with confidence score and source."""
    res = retrieval_service.search("Intellizo Softwares consultancy", max_results=3)
    assert res.total_results > 0
    assert len(res.results) <= 3
    first = res.results[0]
    assert first.relevance_score > 0.0
    assert first.category in ["company", "services"]
    assert "Intellizo" in first.title or "Intellizo" in first.content


def test_search_category_filter():
    """Verify category filtering strictly confines results to requested category."""
    res = retrieval_service.search("automation", category="AI", max_results=5)
    assert res.total_results > 0
    for item in res.results:
        assert item.category == "AI"


def test_search_services_category():
    """Verify searching services returns service details and URLs."""
    res = retrieval_service.search("indoor navigation", category="services")
    assert res.total_results > 0
    assert any("indoor" in item.title.lower() for item in res.results)
    assert any(item.source_url and "indoornavigation" in item.source_url for item in res.results)


def test_search_synonyms():
    """Verify synonym expansion matches related keywords."""
    res = retrieval_service.search("hiring in Bhubaneswar")
    assert res.total_results > 0
    assert any(item.category == "careers" for item in res.results)


def test_search_empty_query():
    """Verify empty query returns 0 results cleanly without failing."""
    res = retrieval_service.search("")
    assert res.total_results == 0
    assert res.results == []


def test_search_whitespace_query():
    """Verify whitespace query returns 0 results."""
    res = retrieval_service.search("   ")
    assert res.total_results == 0


def test_search_unknown_query():
    """Verify completely irrelevant nonsense query yields 0 results."""
    res = retrieval_service.search("quantum teleportation interstellar xyz999")
    assert res.total_results == 0


def test_search_unknown_category():
    """Verify unknown category raises ValueError with list of allowed categories."""
    with pytest.raises(ValueError, match="Unknown category 'astronomy'"):
        retrieval_service.search("AI", category="astronomy")


def test_search_max_results_limit():
    """Verify max_results limits number of items returned."""
    res = retrieval_service.search("software", max_results=2)
    assert len(res.results) <= 2
