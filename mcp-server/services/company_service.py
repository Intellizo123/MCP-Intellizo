"""Business logic handlers for Intellizo Softwares MCP tools."""

import re
from typing import Any, Dict, List, Optional
from models.response_models import (
    AICapabilitiesResponse,
    AICapabilityPillar,
    CareerOpening,
    CareersResponse,
    CompanyContactResponse,
    CompanyProfileResponse,
    ContactChannel,
    NavigationLink,
    NavigationResponse,
    ResearchArticle,
    ResearchArticlesResponse,
    ServiceDetailResponse,
    ServicesListResponse,
    ServiceSummary,
)
from services.response_service import response_service
from utils.data_loader import get_knowledge_base
from utils.logger import logger


class CompanyService:
    """Core domain logic service."""

    def __init__(self):
        pass

    def get_company_profile(self) -> CompanyProfileResponse:
        """Retrieve full company profile with guardrails and conflict transparency."""
        data = get_knowledge_base()
        comp = data.get("company", {})
        meta = data.get("meta", {})

        return CompanyProfileResponse(
            company_name=comp.get("name", "Intellizo Softwares"),
            tagline=comp.get("tagline", "IDEAS ReEngineered"),
            description=comp.get("description", ""),
            website=meta.get("domain", "https://www.intellizosoftwares.com/"),
            mission=comp.get("mission", ""),
            vision=comp.get("vision", ""),
            operating_priorities=comp.get("operating_priorities", []),
            principles=comp.get("principles", {}),
            culture=comp.get("culture", {}),
            global_presence=comp.get("global_presence", {}),
            teams_overview=comp.get("teams", {}),
            known_conflicts=response_service.get_known_conflicts(),
            disclaimer=(
                "Statements regarding client counts and global operations are published company claims. "
                f"{response_service.get_metrics_conflict_note()}"
            ),
        )

    def get_services(self) -> ServicesListResponse:
        """Retrieve overview of all six company service categories."""
        data = get_knowledge_base()
        srv = data.get("services", {})
        services_list = srv.get("list", [])

        summaries = [
            ServiceSummary(
                name=s.get("name", ""),
                summary=s.get("summary", ""),
                capabilities=s.get("capabilities") or s.get("benefits_visible") or [],
                source_url=s.get("source_url"),
            )
            for s in services_list
        ]

        return ServicesListResponse(
            total_services=len(summaries),
            overview_url=srv.get("overview_source_url", "https://www.intellizosoftwares.com/service.html"),
            technology_stack_labels=srv.get("technology_stack_labels", []),
            technology_stack_note=srv.get(
                "technology_stack_note",
                "Technology labels read from published site visuals.",
            ),
            services=summaries,
            disclaimer="All capabilities are based on Intellizo published service portfolios. Specific SLAs or pricing are not published and require direct inquiry.",
        )

    def get_service_details(self, service_name: str) -> ServiceDetailResponse:
        """Find details for a service supporting exact and partial/approximate matching."""
        data = get_knowledge_base()
        services_list = data.get("services", {}).get("list", [])
        all_names = [s.get("name", "") for s in services_list]

        if not service_name or not service_name.strip():
            return ServiceDetailResponse(
                found=False,
                service_name=service_name or "",
                notes="Service name cannot be empty. Please choose from available services.",
                available_services=all_names,
            )

        query = service_name.strip().lower()

        # Fuzzy / keyword mapping dictionary
        aliases = {
            "System Design & Consultancy": [
                "system", "design", "consultancy", "consulting", "architecture",
                "integration", "enterprise", "system design"
            ],
            "Web Application Development": [
                "web", "website", "web app", "web application", "portal",
                "crm", "erp", "web dev"
            ],
            "Mobile & Smart TV App Development": [
                "mobile", "smart tv", "tv", "android", "ios", "app",
                "tizen", "webos", "roku", "apple tv", "pwa", "mobile app"
            ],
            "AI Development & Integration": [
                "ai", "ml", "machine learning", "computer vision", "nlp",
                "artificial intelligence", "predictive", "chatbot", "chatbots"
            ],
            "Indoor Navigation Solutions": [
                "indoor", "indoor navigation", "navigation", "beacons",
                "wifi", "uwb", "geofencing", "asset tracking"
            ],
            "Blockchain & NFT Development": [
                "blockchain", "nft", "smart contracts", "dapps", "token",
                "tokenization", "crypto", "ledger"
            ],
        }

        matched_service: Optional[Dict[str, Any]] = None

        # 1. Exact match (case-insensitive)
        for s in services_list:
            if s.get("name", "").lower() == query:
                matched_service = s
                break

        # 2. Substring match
        if not matched_service:
            for s in services_list:
                s_name_lower = s.get("name", "").lower()
                if query in s_name_lower or s_name_lower in query:
                    matched_service = s
                    break

        # 3. Alias / keyword match
        if not matched_service:
            query_words = set(re.findall(r"\w+", query))
            best_match_name = None
            max_overlap = 0

            for official_name, kw_list in aliases.items():
                overlap = sum(1 for kw in kw_list if kw in query or any(w in kw for w in query_words))
                if overlap > max_overlap:
                    max_overlap = overlap
                    best_match_name = official_name

            if best_match_name and max_overlap > 0:
                for s in services_list:
                    if s.get("name") == best_match_name:
                        matched_service = s
                        break

        if not matched_service:
            return ServiceDetailResponse(
                found=False,
                service_name=service_name,
                notes=(
                    f"No Intellizo service matches '{service_name}'. "
                    f"Intellizo offers 6 official services. Never invent non-existent services."
                ),
                available_services=all_names,
            )

        return ServiceDetailResponse(
            found=True,
            service_name=service_name,
            matched_official_name=matched_service.get("name"),
            summary=matched_service.get("summary"),
            capabilities=matched_service.get("capabilities"),
            additional_offers=matched_service.get("additional_offers"),
            process=matched_service.get("process"),
            smart_tv_platforms=matched_service.get("smart_tv_platforms"),
            smart_tv_use_cases=matched_service.get("smart_tv_use_cases"),
            benefits=matched_service.get("benefits_visible"),
            source_url=matched_service.get("source_url"),
            notes=matched_service.get("note"),
            available_services=all_names,
        )

    def get_ai_capabilities(self) -> AICapabilitiesResponse:
        """Retrieve AI capabilities, agent pillars, environments, and FAQs."""
        data = get_knowledge_base()
        ai = data.get("ai_offerings", {})
        services_list = data.get("services", {}).get("list", [])
        
        # Get AI development details from services
        ai_service = next(
            (s for s in services_list if "AI Development" in s.get("name", "")),
            {},
        )

        agents = ai.get("ai_agents", {})
        pillars = [
            AICapabilityPillar(name=c.get("name", ""), text=c.get("text", ""))
            for c in agents.get("capabilities", [])
        ]

        return AICapabilitiesResponse(
            ai_development_summary=ai_service.get(
                "summary",
                "Custom AI model development, computer vision, NLP, predictive analytics and enterprise integration.",
            ),
            ai_development_capabilities=ai_service.get("capabilities", []),
            ai_strategy_capabilities=ai_service.get("core_strategy_capabilities", []),
            ai_development_process=ai_service.get("process", []),
            ai_development_url=ai_service.get("source_url", "https://www.intellizosoftwares.com/ai%26machinelearning.html"),
            ai_agents_summary=agents.get("summary", ""),
            ai_agents_capabilities=pillars,
            ai_agents_integration_environments=agents.get("integration_environments", []),
            ai_agents_faq=agents.get("faq", []),
            ai_agents_url=agents.get("source_url", "https://www.intellizosoftwares.com/aiagents.html"),
            ai_visibility=ai.get("ai_visibility", {}),
            guardrails_notice=(
                "Intellizo does not guarantee unlisted integrations. "
                "Pricing and delivery timelines vary and require direct technical scoping. "
                "Marketing slogans are claims, not technical warranties."
            ),
        )

    def get_mcp_information(self) -> Dict[str, Any]:
        """Retrieve MCP information preserving exact published expansion."""
        data = get_knowledge_base()
        mcp = data.get("ai_offerings", {}).get("mcp", {})

        return {
            "title": mcp.get("title", "MCP by Intellizo"),
            "expansion_as_published": mcp.get("expansion_as_published", "Model Context & Orchestration Layer"),
            "summary": mcp.get("summary", ""),
            "source_url": mcp.get("source_url", "https://intellizosoftwares.com/mcp.html"),
            "use_cases": mcp.get("use_cases", []),
            "integration_environments_named": mcp.get("environments_named", []),
            "environments_note": mcp.get("environments_note", "Website wording, not a verified compatibility matrix."),
            "faq": mcp.get("faq", []),
            "guardrails_notice": (
                "Intellizo defines MCP as 'Model Context & Orchestration Layer'. "
                "Do not claim unsupported integration compatibility beyond published wording. "
                "Pricing is stated to vary by usage and plan configuration."
            ),
        }

    def get_company_contact(self) -> CompanyContactResponse:
        """Retrieve company contact channels, form fields, and explicit guardrails."""
        data = get_knowledge_base()
        contact = data.get("contact", {})
        meta = data.get("meta", {})

        channels_data = contact.get("channels", [])
        channels = [
            ContactChannel(
                purpose=c.get("purpose", ""),
                value=c.get("value", ""),
                note=c.get("note"),
            )
            for c in channels_data
        ]

        # Extract business and support values
        business = next((c.get("value", "") for c in channels_data if c.get("purpose") == "Business"), "info@intellizo.in")
        support = next((c.get("value", "") for c in channels_data if "support" in c.get("purpose", "").lower()), "support@intellizo.in")

        return CompanyContactResponse(
            business_contact=business,
            support_contact=support,
            official_website=meta.get("domain", "https://www.intellizosoftwares.com/"),
            official_contact_page=contact.get("source_url", "https://intellizosoftwares.com/contact.html"),
            channels=channels,
            meeting_form=contact.get("meeting_form", {}),
            project_enquiry_form=contact.get("project_enquiry_form", {}),
            email_discrepancies=response_service.get_contact_discrepancy_note(),
            action_guardrail=response_service.get_action_guardrail(),
        )

    def get_careers(self) -> CareersResponse:
        """Retrieve job openings with time-sensitivity disclaimer."""
        data = get_knowledge_base()
        careers = data.get("careers", {})
        openings_data = careers.get("openings", [])

        openings = [
            CareerOpening(
                title=op.get("title", ""),
                location=op.get("location", "Bhubaneswar"),
                type=op.get("type", "Full Time"),
                experience=op.get("experience", ""),
                summary=op.get("summary", ""),
                responsibilities=op.get("responsibilities"),
                required_skills=op.get("required_skills"),
            )
            for op in openings_data
        ]

        return CareersResponse(
            careers_page_url=careers.get("source_url", "https://www.intellizosoftwares.com/career.html"),
            filters_supported=careers.get("filters", {}),
            openings=openings,
            time_sensitivity_warning=(
                "Important: Job openings from data.json are time-sensitive and may become outdated. "
                "Always refer candidates to the official careers page at https://www.intellizosoftwares.com/career.html "
                "for the most up-to-date vacancies and application instructions."
            ),
        )

    def get_research_articles(self) -> ResearchArticlesResponse:
        """Retrieve research catalogue preserving note on claims."""
        data = get_knowledge_base()
        res = data.get("research", {})

        articles = [
            ResearchArticle(
                title=a.get("title", ""),
                url=a.get("url", ""),
                date=a.get("date", ""),
                read_time=a.get("read_time", ""),
                summary=a.get("summary", ""),
                key_points=a.get("key_points", []),
            )
            for a in res.get("articles", [])
        ]

        return ResearchArticlesResponse(
            note=res.get(
                "note",
                "Only card text and partial/paraphrased summaries captured; not full papers. Figures like 41% are article claims, not verified statistics.",
            ),
            articles=articles,
            homepage_research_cards=res.get("homepage_cards", []),
            service_page_research_cards=res.get("service_page_cards", []),
            guardrails_notice="Never invent missing research content. Paraphrased insights are based on published summaries.",
        )

    def get_company_navigation(self) -> NavigationResponse:
        """Retrieve all official website links organized by area."""
        data = get_knowledge_base()
        nav_list = data.get("navigation", [])
        domain = data.get("meta", {}).get("domain", "https://www.intellizosoftwares.com/")

        links = [
            NavigationLink(area=item.get("area", ""), url=item.get("url", ""))
            for item in nav_list
        ]

        # Categorize links for easy consumption
        categorized: Dict[str, List[NavigationLink]] = {
            "Core": [],
            "Services": [],
            "AI & Tech": [],
            "Company & Governance": [],
        }

        for link in links:
            area_lower = link.area.lower()
            if any(k in area_lower for k in ["service", "system", "web", "mobile", "indoor", "blockchain"]):
                categorized["Services"].append(link)
            elif any(k in area_lower for k in ["ai", "mcp"]):
                categorized["AI & Tech"].append(link)
            elif any(k in area_lower for k in ["about", "culture", "resources", "global", "careers", "privacy"]):
                categorized["Company & Governance"].append(link)
            else:
                categorized["Core"].append(link)

        return NavigationResponse(
            official_website=domain,
            navigation_links=links,
            organized_by_category=categorized,
        )


company_service = CompanyService()
