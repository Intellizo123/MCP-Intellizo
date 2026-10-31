"""Structured response models for Intellizo Softwares MCP tools."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class SearchItem(BaseModel):
    """An individual search result item."""
    id: str = Field(description="Unique identifier of the knowledge item")
    title: str = Field(description="Title or heading of the item")
    category: str = Field(description="Knowledge category (e.g. services, AI, company, contact)")
    content: str = Field(description="Primary descriptive text")
    source_url: Optional[str] = Field(default=None, description="Official source URL when available")
    source_context: str = Field(description="Contextual section or origin of this information")
    relevance_score: float = Field(description="Relevance or confidence score between 0.0 and 1.0")


class SearchResponse(BaseModel):
    """Response returned by search_company_knowledge tool."""
    query: str
    category_filter: Optional[str] = None
    total_results: int
    results: List[SearchItem]
    guardrails_notice: str = Field(
        default="Official Intellizo Softwares knowledge archive. Marketing figures and claims are published company statements, not independently verified. Refer to official URLs for latest updates."
    )


class CompanyProfileResponse(BaseModel):
    """Response returned by get_company_profile tool."""
    company_name: str
    tagline: str
    description: str
    website: str
    mission: str
    vision: str
    operating_priorities: List[str]
    principles: Dict[str, str]
    culture: Dict[str, Any]
    global_presence: Dict[str, Any]
    teams_overview: Dict[str, Any]
    known_conflicts: List[Dict[str, Any]]
    disclaimer: str


class ServiceSummary(BaseModel):
    """Brief summary of a single service."""
    name: str
    summary: str
    capabilities: List[str]
    source_url: Optional[str] = None


class ServicesListResponse(BaseModel):
    """Response returned by get_services tool."""
    total_services: int
    overview_url: str
    technology_stack_labels: List[str]
    technology_stack_note: str
    services: List[ServiceSummary]
    disclaimer: str


class ServiceDetailResponse(BaseModel):
    """Response returned by get_service_details tool."""
    found: bool
    service_name: str
    matched_official_name: Optional[str] = None
    summary: Optional[str] = None
    capabilities: Optional[List[str]] = None
    additional_offers: Optional[List[str]] = None
    process: Optional[List[str]] = None
    smart_tv_platforms: Optional[List[str]] = None
    smart_tv_use_cases: Optional[List[str]] = None
    benefits: Optional[List[str]] = None
    source_url: Optional[str] = None
    notes: Optional[str] = None
    available_services: Optional[List[str]] = None


class AICapabilityPillar(BaseModel):
    """An AI capability pillar."""
    name: str
    text: str


class AICapabilitiesResponse(BaseModel):
    """Response returned by get_ai_capabilities tool."""
    ai_development_summary: str
    ai_development_capabilities: List[str]
    ai_strategy_capabilities: List[str]
    ai_development_process: List[str]
    ai_development_url: str
    ai_agents_summary: str
    ai_agents_capabilities: List[AICapabilityPillar]
    ai_agents_integration_environments: List[str]
    ai_agents_faq: List[Dict[str, str]]
    ai_agents_url: str
    ai_visibility: Dict[str, Any]
    guardrails_notice: str


class MCPInformationResponse(BaseModel):
    """Response returned by get_mcp_information tool."""
    title: str
    expansion_as_published: str
    summary: str
    source_url: str
    use_cases: List[str]
    integration_environments_named: List[str]
    environments_note: str
    faq: List[Dict[str, str]]
    guardrails_notice: str


class ContactChannel(BaseModel):
    """Contact communication channel."""
    purpose: str
    value: str
    note: Optional[str] = None


class CompanyContactResponse(BaseModel):
    """Response returned by get_company_contact tool."""
    business_contact: str
    support_contact: str
    official_website: str
    official_contact_page: str
    channels: List[ContactChannel]
    meeting_form: Dict[str, Any]
    project_enquiry_form: Dict[str, Any]
    email_discrepancies: List[str]
    action_guardrail: str


class CareerOpening(BaseModel):
    """Job vacancy item."""
    title: str
    location: str
    type: str
    experience: str
    summary: str
    responsibilities: Optional[List[str]] = None
    required_skills: Optional[List[str]] = None


class CareersResponse(BaseModel):
    """Response returned by get_careers tool."""
    careers_page_url: str
    filters_supported: Dict[str, Any]
    openings: List[CareerOpening]
    time_sensitivity_warning: str


class ResearchArticle(BaseModel):
    """A published research article."""
    title: str
    url: str
    date: str
    read_time: str
    summary: str
    key_points: List[str]


class ResearchArticlesResponse(BaseModel):
    """Response returned by get_research_articles tool."""
    note: str
    articles: List[ResearchArticle]
    homepage_research_cards: List[Dict[str, str]]
    service_page_research_cards: List[Dict[str, str]]
    guardrails_notice: str


class NavigationLink(BaseModel):
    """A site navigation entry."""
    area: str
    url: str


class NavigationResponse(BaseModel):
    """Response returned by get_company_navigation tool."""
    official_website: str
    navigation_links: List[NavigationLink]
    organized_by_category: Dict[str, List[NavigationLink]]
