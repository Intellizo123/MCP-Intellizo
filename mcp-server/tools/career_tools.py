"""Careers and recruitment MCP tools for Intellizo Softwares."""

from typing import Any, Dict
from services.company_service import company_service
from utils.logger import logger


def get_careers() -> Dict[str, Any]:
    """Retrieve published career openings, required skills, and department filters for Intellizo Softwares.

    Important: Listings in the knowledge base are time-sensitive.
    Directs applicants to the official careers page for current openings.

    Returns:
        Structured dictionary covering:
        - Official careers URL: https://www.intellizosoftwares.com/career.html
        - Department filters: Tech, Design, Marketing, HR
        - Openings currently catalogued in data.json:
          * Custom Software Engineer (Bhubaneswar, Full Time, 5-10 Years)
          * UI / UX Designer (Bhubaneswar, Full Time, 3-6 Years)
        - Responsibilities and required technical skills
        - Explicit time-sensitivity advisory
    """
    logger.info("Tool call get_careers")
    res = company_service.get_careers()
    return res.model_dump()
