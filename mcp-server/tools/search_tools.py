"""Tool for searching company knowledge across all categories."""

from typing import Any, Dict, Optional
from services.retrieval_service import retrieval_service
from utils.logger import logger


def search_company_knowledge(
    query: str,
    category: Optional[str] = None,
    max_results: Optional[int] = 5,
) -> Dict[str, Any]:
    """Search across all Intellizo Softwares company information using deterministic keyword matching.

    Use this tool to find relevant details across categories such as company profile,
    services, AI capabilities, MCP orchestration, research papers, contact channels,
    careers, privacy policy, and website navigation.

    Args:
        query: The search keywords or question (e.g., 'smart tv development', 'MCP', 'indoor navigation', 'Bhubaneswar office').
        category: Optional category filter. Allowed values: company, services, AI, MCP, research, contact, careers, privacy, navigation.
        max_results: Maximum number of ranked results to return (default is 5, max is 50).

    Returns:
        Structured dictionary containing query, category filter, total results found,
        list of matching items (with title, category, content, source URL, source context,
        relevance score), and guardrail notices.
    """
    logger.info("Tool call search_company_knowledge: query=%r, category=%r, max_results=%r", query, category, max_results)
    limit = max(1, min(max_results or 5, 50))
    res = retrieval_service.search(query=query, category=category, max_results=limit)
    return res.model_dump()
