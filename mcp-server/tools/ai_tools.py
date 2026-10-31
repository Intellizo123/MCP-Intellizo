"""AI and MCP tools for Intellizo Softwares."""

from typing import Any, Dict
from services.company_service import company_service
from utils.logger import logger


def get_ai_capabilities() -> Dict[str, Any]:
    """Retrieve Intellizo Softwares AI capabilities, AI agent pillars, integration environments, and FAQs.

    Returns:
        Structured dictionary covering:
        - AI Development capabilities (custom models, computer vision, NLP, predictive analytics, chatbots)
        - Core AI strategy capabilities (readiness, governance, roadmap, pipeline)
        - AI Agents summary and 6 operational pillars:
          1. Observe & Monitor
          2. Analyze & Reason
          3. Recommend & Support Decisions
          4. Automate & Execute
          5. Learn & Improve Over Time
          6. Communicate & Collaborate
        - Integration environments (ERP, CRM, data warehouses, cloud, on-premises)
        - AI Agents FAQs and AI Visibility offering details
        - Guardrails disclaimers regarding unverified claims and pricing
    """
    logger.info("Tool call get_ai_capabilities")
    res = company_service.get_ai_capabilities()
    return res.model_dump()


def get_mcp_information() -> Dict[str, Any]:
    """Retrieve Intellizo Softwares MCP (Model Context & Orchestration Layer) specifications and FAQs.

    Preserves the published expansion and claims without fabricating unsupported compatibility.

    Returns:
        Structured dictionary covering:
        - Title: MCP by Intellizo
        - Expansion as published: 'Model Context & Orchestration Layer'
        - Summary of context, orchestration, and control
        - Key use cases (unlocking insights, context for every team, enhancing AI workflows)
        - Listed integration environments (Claude, Cursor, GitHub, OpenAI, Model Context Protocol)
        - Environments note explaining website wording status
        - MCP FAQs (models powering agents, technical expertise requirements, usage-based pricing)
        - Source URL: https://intellizosoftwares.com/mcp.html
    """
    logger.info("Tool call get_mcp_information")
    res = company_service.get_mcp_information()
    return res
