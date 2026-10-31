"""Company profile and website navigation MCP tools."""

from typing import Any, Dict
from services.company_service import company_service
from utils.logger import logger


def get_company_profile() -> Dict[str, Any]:
    """Retrieve the official company profile, mission, vision, culture, and presence for Intellizo Softwares.

    Returns:
        Structured company profile including:
        - Company name: Intellizo Softwares
        - Tagline: IDEAS ReEngineered
        - Description: End-to-end software and AI consultancy
        - Mission & Vision (retaining exact published wording)
        - Operating priorities and core principles
        - Company culture (trust, curiosity, clarity, human-centered systems)
        - Global presence information and regional selectors
        - Teams breakdown (AI Lab, Backend, Content, QA/DevOps, Frontend, UX/UI, Digital)
        - Known conflicting information notes (e.g. homepage claims vs resources page metrics)
    """
    logger.info("Tool call get_company_profile")
    profile = company_service.get_company_profile()
    return profile.model_dump()


def get_company_navigation() -> Dict[str, Any]:
    """Retrieve official website links and navigation hierarchy for Intellizo Softwares.

    Returns:
        Official website URLs for:
        - Homepage
        - About
        - Services overview
        - System Design & Integration
        - Web Development
        - Mobile & Smart TV App Development
        - AI Development & Machine Learning
        - Indoor Navigation Solutions
        - Blockchain Development
        - AI Agents
        - MCP (Model Context & Orchestration Layer)
        - Research / Resources
        - Careers
        - Contact
        - Privacy Policy
        - Culture
        - Global Presence
    """
    logger.info("Tool call get_company_navigation")
    nav = company_service.get_company_navigation()
    return nav.model_dump()
