"""Intellizo Softwares MCP Tools module.

Registers all 10 MCP tools:
1. search_company_knowledge
2. get_company_profile
3. get_services
4. get_service_details
5. get_ai_capabilities
6. get_mcp_information
7. get_company_contact
8. get_careers
9. get_research_articles
10. get_company_navigation
"""

from typing import Any
from tools.ai_tools import get_ai_capabilities, get_mcp_information
from tools.career_tools import get_careers
from tools.company_tools import get_company_navigation, get_company_profile
from tools.contact_tools import get_company_contact
from tools.research_tools import get_research_articles
from tools.search_tools import search_company_knowledge
from tools.service_tools import get_service_details, get_services
from utils.logger import logger

ALL_TOOLS = [
    (
        search_company_knowledge,
        "search_company_knowledge",
        "Search across all Intellizo Softwares company information using deterministic keyword matching.",
    ),
    (
        get_company_profile,
        "get_company_profile",
        "Retrieve the official company profile, mission, vision, operating priorities, culture, and presence for Intellizo Softwares.",
    ),
    (
        get_services,
        "get_services",
        "Retrieve all six official Intellizo Softwares service categories and published technology stack.",
    ),
    (
        get_service_details,
        "get_service_details",
        "Retrieve detailed capabilities, process, platforms, and source URL for a specific Intellizo service.",
    ),
    (
        get_ai_capabilities,
        "get_ai_capabilities",
        "Retrieve Intellizo Softwares AI development capabilities, AI agent operational pillars, integration environments, and FAQs.",
    ),
    (
        get_mcp_information,
        "get_mcp_information",
        "Retrieve Intellizo Softwares MCP (Model Context & Orchestration Layer) specifications, use cases, and FAQs.",
    ),
    (
        get_company_contact,
        "get_company_contact",
        "Retrieve official contact channels, meeting form fields, inquiry options, and communication guardrails for Intellizo Softwares.",
    ),
    (
        get_careers,
        "get_careers",
        "Retrieve published career openings, required skills, and department filters for Intellizo Softwares.",
    ),
    (
        get_research_articles,
        "get_research_articles",
        "Retrieve published research articles, whitepaper insights, and card summaries from Intellizo Softwares.",
    ),
    (
        get_company_navigation,
        "get_company_navigation",
        "Retrieve official website links and navigation hierarchy for Intellizo Softwares.",
    ),
]


def register_tools(server: Any) -> None:
    """Register all 10 tools on the FastMCP / MCPServer instance."""
    for func, name, description in ALL_TOOLS:
        logger.info("Registering MCP tool: %s", name)
        server.add_tool(func, name=name, description=description)
    logger.info("Successfully registered %d MCP tools.", len(ALL_TOOLS))


__all__ = [
    "search_company_knowledge",
    "get_company_profile",
    "get_services",
    "get_service_details",
    "get_ai_capabilities",
    "get_mcp_information",
    "get_company_contact",
    "get_careers",
    "get_research_articles",
    "get_company_navigation",
    "register_tools",
    "ALL_TOOLS",
]
