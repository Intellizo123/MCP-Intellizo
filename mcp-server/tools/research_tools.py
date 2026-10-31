"""Research and technical papers MCP tools for Intellizo Softwares."""

from typing import Any, Dict
from services.company_service import company_service
from utils.logger import logger


def get_research_articles() -> Dict[str, Any]:
    """Retrieve published research articles, whitepaper insights, and card summaries from Intellizo Softwares.

    Preserves published summaries without inventing missing research content or statistical facts.

    Returns:
        Structured dictionary covering:
        - Research articles catalogue:
          * Beyond the Bot: Architecting for a World of "Sovereign AI"
          * The Efficiency Dividend: Using Agentic AI to Turn Operational Debt into Market Share
          * The 10x Developer & The AI-First Team: Redefining "Human + Software" Excellence
          * From Debt to Value: Reclaiming the 41% of IT Budget Lost to Manual Legacy
          * Building Stable and Scalable Digital Ecosystems
          * Integrating APIs, ERP, and UX Excellence
        - Article publication dates, read times, summaries, key points, and URLs
        - Homepage and service page insight cards
        - Guardrails notice regarding card paraphrasing and statistical claim status
    """
    logger.info("Tool call get_research_articles")
    res = company_service.get_research_articles()
    return res.model_dump()
