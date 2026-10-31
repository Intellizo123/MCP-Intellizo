"""Service-related MCP tools for Intellizo Softwares."""

from typing import Any, Dict
from services.company_service import company_service
from utils.logger import logger


def get_services() -> Dict[str, Any]:
    """Retrieve all six official Intellizo Softwares service categories and technology stack.

    The six services are:
    1. System Design & Consultancy
    2. Web Application Development
    3. Mobile & Smart TV App Development
    4. AI Development & Integration
    5. Indoor Navigation Solutions
    6. Blockchain & NFT Development

    Returns:
        Structured dictionary containing total services count, official overview URL,
        full technology stack labels, and each service with its summary, capabilities,
        and source URL.
    """
    logger.info("Tool call get_services")
    res = company_service.get_services()
    return res.model_dump()


def get_service_details(service_name: str) -> Dict[str, Any]:
    """Retrieve detailed capabilities, process, platforms, and source URL for a specific Intellizo service.

    Supports partial and approximate names (e.g., 'smart tv', 'tv', 'web dev', 'blockchain',
    'indoor navigation', 'beacons', 'system design', 'ai', 'machine learning').

    Args:
        service_name: The name or partial keyword of the service to look up.

    Returns:
        Structured dictionary containing:
        - found: bool
        - service_name: query provided
        - matched_official_name: standardized official name
        - summary: detailed description
        - capabilities: full list of technical capabilities
        - additional_offers: enterprise architecture / integration offers if applicable
        - process: engineering and delivery workflow steps
        - smart_tv_platforms / smart_tv_use_cases: platform specifics if applicable
        - benefits: tamper-proof / process automation benefits if applicable
        - source_url: official page URL
        - available_services: list of all 6 valid services if queried name was not matched
    """
    logger.info("Tool call get_service_details: service_name=%r", service_name)
    res = company_service.get_service_details(service_name=service_name)
    return res.model_dump()
