"""Contact and inquiry MCP tools for Intellizo Softwares."""

from typing import Any, Dict
from services.company_service import company_service
from utils.logger import logger


def get_company_contact() -> Dict[str, Any]:
    """Retrieve official contact channels, meeting form fields, and inquiry options for Intellizo Softwares.

    Important Guardrail: Does not submit forms or pretend to send enquiries.
    Directs users to the official contact and consultation flow.

    Returns:
        Structured dictionary covering:
        - Primary business contact: info@intellizo.in
        - Support contact: support@intellizo.in
        - Official website: https://www.intellizosoftwares.com/
        - Official contact page: https://intellizosoftwares.com/contact.html
        - All published channels (business, support, advertising division, general footer)
        - Meeting enquiry form fields and consultation meeting types
        - Project enquiry form fields and service options
        - Published email address discrepancies (including privacy policy typo)
        - Mandatory action guardrail prohibiting simulated submissions
    """
    logger.info("Tool call get_company_contact")
    res = company_service.get_company_contact()
    return res.model_dump()
