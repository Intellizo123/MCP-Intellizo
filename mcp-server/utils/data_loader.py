"""Data loader and validator for Intellizo Softwares knowledge base."""

import json
from pathlib import Path
from typing import Any, Dict, Optional

from utils.config import resolve_data_json_path, settings
from utils.logger import logger

REQUIRED_TOP_LEVEL_KEYS = [
    "meta",
    "company",
    "services",
    "ai_offerings",
    "research",
    "contact",
    "privacy_policy",
    "careers",
    "navigation",
    "known_conflicts",
    "rag_response_policy",
]

_cached_data: Optional[Dict[str, Any]] = None


def validate_knowledge_base(data: Dict[str, Any]) -> None:
    """Validate structure of loaded knowledge base data."""
    if not isinstance(data, dict):
        raise ValueError("Knowledge base root must be a JSON dictionary.")

    missing_keys = [k for k in REQUIRED_TOP_LEVEL_KEYS if k not in data]
    if missing_keys:
        raise ValueError(f"Knowledge base is missing required top-level keys: {missing_keys}")

    # Validate company section
    company = data.get("company", {})
    if not isinstance(company, dict) or not company.get("name"):
        raise ValueError("Invalid 'company' section: 'name' is required.")

    # Validate services section
    services = data.get("services", {})
    if not isinstance(services, dict) or "list" not in services or not isinstance(services["list"], list):
        raise ValueError("Invalid 'services' section: 'list' array is required.")

    if len(services["list"]) != 6:
        logger.warning(
            "Expected 6 company services in data.json, found %d", len(services["list"])
        )

    # Validate AI offerings
    ai = data.get("ai_offerings", {})
    if not isinstance(ai, dict) or "ai_agents" not in ai or "mcp" not in ai:
        raise ValueError("Invalid 'ai_offerings' section: 'ai_agents' and 'mcp' are required.")

    # Validate contact
    contact = data.get("contact", {})
    if not isinstance(contact, dict) or "channels" not in contact:
        raise ValueError("Invalid 'contact' section: 'channels' is required.")

    # Validate careers
    careers = data.get("careers", {})
    if not isinstance(careers, dict) or "openings" not in careers:
        raise ValueError("Invalid 'careers' section: 'openings' is required.")


def load_knowledge_base(file_path: Optional[Path | str] = None, force_reload: bool = False) -> Dict[str, Any]:
    """Load and validate the data.json knowledge base file."""
    global _cached_data

    if _cached_data is not None and not force_reload:
        return _cached_data

    if file_path:
        path = Path(file_path)
    else:
        path = settings.data_json_path
        if not path.exists():
            path = resolve_data_json_path()

    if not path.exists():
        raise FileNotFoundError(f"Knowledge base file not found at: {path}")

    logger.info("Loading knowledge base from: %s", path)

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Failed to parse JSON from {path}: {exc}") from exc

    validate_knowledge_base(data)
    _cached_data = data
    logger.info("Successfully loaded and validated knowledge base from %s", path)
    return _cached_data


def get_knowledge_base() -> Dict[str, Any]:
    """Get the cached knowledge base or load it if not yet loaded."""
    global _cached_data
    if _cached_data is None:
        return load_knowledge_base()
    return _cached_data
