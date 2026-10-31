"""Tests for knowledge base data loader and validation."""

import pytest
from utils.data_loader import get_knowledge_base, load_knowledge_base, validate_knowledge_base


def test_load_knowledge_base_success():
    """Verify data.json loads cleanly and passes all validation checks."""
    data = load_knowledge_base(force_reload=True)
    assert isinstance(data, dict)
    assert data["company"]["name"] == "Intellizo Softwares"
    assert data["company"]["tagline"] == "IDEAS ReEngineered"
    assert len(data["services"]["list"]) == 6
    assert "rag_response_policy" in data
    assert "known_conflicts" in data


def test_cached_knowledge_base():
    """Verify get_knowledge_base returns cached dictionary."""
    kb1 = get_knowledge_base()
    kb2 = get_knowledge_base()
    assert kb1 is kb2


def test_validate_knowledge_base_missing_keys():
    """Verify validation raises ValueError on missing required keys."""
    invalid_data = {"meta": {}}
    with pytest.raises(ValueError, match="missing required top-level keys"):
        validate_knowledge_base(invalid_data)


def test_validate_knowledge_base_invalid_company():
    """Verify validation raises ValueError when company name is missing."""
    invalid_data = {
        "meta": {},
        "company": {},
        "services": {"list": []},
        "ai_offerings": {"ai_agents": {}, "mcp": {}},
        "research": {},
        "contact": {"channels": []},
        "privacy_policy": {},
        "careers": {"openings": []},
        "navigation": [],
        "known_conflicts": [],
        "rag_response_policy": [],
    }
    with pytest.raises(ValueError, match="'name' is required"):
        validate_knowledge_base(invalid_data)


def test_load_nonexistent_file():
    """Verify FileNotFoundError is raised for non-existent path."""
    with pytest.raises(FileNotFoundError):
        load_knowledge_base(file_path="nonexistent_data.json", force_reload=True)
