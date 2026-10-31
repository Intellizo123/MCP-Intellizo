"""Request models with Pydantic validation."""

from typing import Optional
from pydantic import BaseModel, Field

VALID_SEARCH_CATEGORIES = [
    "company",
    "services",
    "AI",
    "MCP",
    "research",
    "contact",
    "careers",
    "privacy",
    "navigation",
]

class SearchRequest(BaseModel):
    """Input parameters for searching company knowledge."""
    query: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="The search query or keywords to look up across Intellizo Softwares knowledge base.",
    )
    category: Optional[str] = Field(
        default=None,
        description=(
            "Optional category filter. Allowed values: "
            "company, services, AI, MCP, research, contact, careers, privacy, navigation."
        ),
    )
    max_results: Optional[int] = Field(
        default=5,
        ge=1,
        le=50,
        description="Maximum number of search results to return (default 5).",
    )


class ServiceDetailsRequest(BaseModel):
    """Input parameters for looking up specific service details."""
    service_name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description=(
            "Name or partial name of the Intellizo service "
            "(e.g., 'Web Application Development', 'AI Development', 'Indoor Navigation', 'Blockchain', 'System Design', 'Mobile & Smart TV')."
        ),
    )
