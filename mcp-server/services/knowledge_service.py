"""Knowledge indexing and access service for Intellizo Softwares data."""

from typing import Any, Dict, List, Optional
from models.response_models import SearchItem
from utils.data_loader import get_knowledge_base
from utils.logger import logger


class KnowledgeIndexItem:
    """Internal indexed knowledge chunk."""

    def __init__(
        self,
        item_id: str,
        category: str,
        title: str,
        content: str,
        source_url: Optional[str] = None,
        source_context: str = "",
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.item_id = item_id
        self.category = category
        self.title = title
        self.content = content
        self.source_url = source_url
        self.source_context = source_context
        self.metadata = metadata or {}

    def to_search_item(self, relevance_score: float) -> SearchItem:
        return SearchItem(
            id=self.item_id,
            title=self.title,
            category=self.category,
            content=self.content,
            source_url=self.source_url,
            source_context=self.source_context,
            relevance_score=round(relevance_score, 3),
        )


class KnowledgeService:
    """Service to load, index, and provide access to company data chunks."""

    def __init__(self):
        self._index: List[KnowledgeIndexItem] = []
        self._is_indexed = False

    def build_index(self) -> None:
        """Parse data.json and build searchable index items."""
        data = get_knowledge_base()
        items: List[KnowledgeIndexItem] = []

        domain = data.get("meta", {}).get("domain", "https://www.intellizosoftwares.com/")

        # 1. Company category
        comp = data.get("company", {})
        items.append(
            KnowledgeIndexItem(
                item_id="comp_profile",
                category="company",
                title=f"{comp.get('name', 'Intellizo Softwares')} - Profile & Tagline",
                content=f"Company: {comp.get('name')}. Tagline: {comp.get('tagline')}. Description: {comp.get('description')}",
                source_url=domain,
                source_context="company.overview",
                metadata={"name": comp.get("name"), "tagline": comp.get("tagline")},
            )
        )

        items.append(
            KnowledgeIndexItem(
                item_id="comp_mission_vision",
                category="company",
                title="Intellizo Mission & Vision",
                content=f"Mission: {comp.get('mission')}. Vision: {comp.get('vision')}",
                source_url=domain,
                source_context="company.mission_vision",
            )
        )

        operating_priorities = " | ".join(comp.get("operating_priorities", []))
        items.append(
            KnowledgeIndexItem(
                item_id="comp_operating_priorities",
                category="company",
                title="Intellizo Operating Priorities",
                content=f"Operating Priorities: {operating_priorities}",
                source_url=domain,
                source_context="company.operating_priorities",
            )
        )

        principles_text = " | ".join(
            f"{k.replace('_', ' ').title()}: {v}"
            for k, v in comp.get("principles", {}).items()
        )
        items.append(
            KnowledgeIndexItem(
                item_id="comp_principles",
                category="company",
                title="Intellizo Core Principles",
                content=f"Core Principles: {principles_text}",
                source_url=domain,
                source_context="company.principles",
            )
        )

        culture = comp.get("culture", {})
        published_principles_str = " | ".join(
            f"{p.get('name')}: {p.get('text')}"
            for p in culture.get("published_principles", [])
        )
        items.append(
            KnowledgeIndexItem(
                item_id="comp_culture",
                category="company",
                title="Intellizo Culture & Values",
                content=(
                    f"Culture Highlights: {', '.join(culture.get('highlights', []))}. "
                    f"Insight: {culture.get('insight', '')}. "
                    f"Principles: {published_principles_str}"
                ),
                source_url=culture.get("source_url"),
                source_context="company.culture",
            )
        )

        presence = comp.get("global_presence", {})
        items.append(
            KnowledgeIndexItem(
                item_id="comp_presence",
                category="company",
                title="Global Presence",
                content=(
                    f"Presence regions: {', '.join(presence.get('regions_selectors', []))}. "
                    f"Note: {presence.get('note', '')}"
                ),
                source_url=presence.get("source_url"),
                source_context="company.global_presence",
            )
        )

        teams = comp.get("teams", {})
        for team in teams.get("list", []):
            team_name = team.get("team", "")
            items.append(
                KnowledgeIndexItem(
                    item_id=f"comp_team_{team_name.lower().replace(' ', '_')}",
                    category="company",
                    title=f"Intellizo Team - {team_name}",
                    content=(
                        f"Team: {team_name}. Focus: {team.get('focus')}. "
                        f"Roles: {', '.join(team.get('roles', []))}. "
                        f"Tools: {', '.join(team.get('tools', []))}. "
                        f"Note: {teams.get('member_counts_note')}"
                    ),
                    source_url=teams.get("source_url"),
                    source_context=f"company.teams.{team_name}",
                )
            )

        # 2. Services category
        srv = data.get("services", {})
        items.append(
            KnowledgeIndexItem(
                item_id="srv_overview",
                category="services",
                title="Intellizo Software Services Overview & Tech Stack",
                content=(
                    f"Services count: {srv.get('count', 6)}. "
                    f"Tech Stack: {', '.join(srv.get('technology_stack_labels', []))}. "
                    f"Note: {srv.get('technology_stack_note', '')}"
                ),
                source_url=srv.get("overview_source_url"),
                source_context="services.overview",
            )
        )

        for s in srv.get("list", []):
            s_name = s.get("name", "")
            s_caps = " | ".join(s.get("capabilities", []))
            s_proc = " -> ".join(s.get("process", [])) if s.get("process") else ""
            s_extra = ""
            if s.get("additional_offers"):
                s_extra += f" Additional Offers: {' | '.join(s['additional_offers'])}."
            if s.get("smart_tv_platforms"):
                s_extra += f" Smart TV Platforms: {', '.join(s['smart_tv_platforms'])}. Use Cases: {', '.join(s.get('smart_tv_use_cases', []))}."
            if s.get("benefits_visible"):
                s_extra += f" Visible Benefits: {' | '.join(s['benefits_visible'])}."

            content = (
                f"Service: {s_name}. Summary: {s.get('summary')}. "
                f"Capabilities: {s_caps}.{s_extra} Process: {s_proc}"
            )
            items.append(
                KnowledgeIndexItem(
                    item_id=f"srv_{s_name.lower().replace(' ', '_').replace('&', 'and')}",
                    category="services",
                    title=f"Service: {s_name}",
                    content=content,
                    source_url=s.get("source_url"),
                    source_context=f"services.{s_name}",
                    metadata={"service_name": s_name, "raw": s},
                )
            )

        # 3. AI category
        ai = data.get("ai_offerings", {})
        agents = ai.get("ai_agents", {})
        agent_caps = " | ".join(
            f"{c.get('name')}: {c.get('text')}"
            for c in agents.get("capabilities", [])
        )
        agent_envs = ", ".join(agents.get("integration_environments", []))
        items.append(
            KnowledgeIndexItem(
                item_id="ai_agents_overview",
                category="AI",
                title="Intellizo AI Agents & Automation",
                content=(
                    f"Summary: {agents.get('summary')}. "
                    f"Pillars & Capabilities: {agent_caps}. "
                    f"Integration Environments: {agent_envs}"
                ),
                source_url=agents.get("source_url"),
                source_context="ai_offerings.ai_agents",
            )
        )

        for i, faq in enumerate(agents.get("faq", [])):
            items.append(
                KnowledgeIndexItem(
                    item_id=f"ai_agents_faq_{i+1}",
                    category="AI",
                    title=f"AI Agent FAQ: {faq.get('q')}",
                    content=f"Question: {faq.get('q')} Answer: {faq.get('a')}",
                    source_url=agents.get("source_url"),
                    source_context="ai_offerings.ai_agents.faq",
                )
            )

        visibility = ai.get("ai_visibility", {})
        items.append(
            KnowledgeIndexItem(
                item_id="ai_visibility",
                category="AI",
                title="AI Visibility & AI Search Optimization",
                content=f"Tagline: {visibility.get('tagline')}. Note: {visibility.get('note')}",
                source_url=visibility.get("source_url"),
                source_context="ai_offerings.ai_visibility",
            )
        )

        # 4. MCP category
        mcp = ai.get("mcp", {})
        use_cases = " | ".join(mcp.get("use_cases", []))
        envs = ", ".join(mcp.get("environments_named", []))
        items.append(
            KnowledgeIndexItem(
                item_id="mcp_overview",
                category="MCP",
                title=f"{mcp.get('title', 'MCP by Intellizo')} - {mcp.get('expansion_as_published', '')}",
                content=(
                    f"Expansion: {mcp.get('expansion_as_published')}. "
                    f"Summary: {mcp.get('summary')}. "
                    f"Use Cases: {use_cases}. "
                    f"Listed Environments: {envs}. "
                    f"Note: {mcp.get('environments_note')}"
                ),
                source_url=mcp.get("source_url"),
                source_context="ai_offerings.mcp",
                metadata={"expansion": mcp.get("expansion_as_published")},
            )
        )

        for i, mcp_faq in enumerate(mcp.get("faq", [])):
            items.append(
                KnowledgeIndexItem(
                    item_id=f"mcp_faq_{i+1}",
                    category="MCP",
                    title=f"MCP FAQ: {mcp_faq.get('q')}",
                    content=f"Question: {mcp_faq.get('q')} Answer: {mcp_faq.get('a')}",
                    source_url=mcp.get("source_url"),
                    source_context="ai_offerings.mcp.faq",
                )
            )

        # 5. Research category
        res = data.get("research", {})
        for art in res.get("articles", []):
            title = art.get("title", "")
            key_pts = " | ".join(art.get("key_points", []))
            items.append(
                KnowledgeIndexItem(
                    item_id=f"res_art_{title.lower()[:20].replace(' ', '_')}",
                    category="research",
                    title=f"Research: {title}",
                    content=(
                        f"Date: {art.get('date')}. Read time: {art.get('read_time')}. "
                        f"Summary: {art.get('summary')}. Key points: {key_pts}. "
                        f"Note: {res.get('note', '')}"
                    ),
                    source_url=art.get("url"),
                    source_context="research.articles",
                )
            )

        for card in res.get("homepage_cards", []):
            items.append(
                KnowledgeIndexItem(
                    item_id=f"res_card_home_{card.get('title', '')[:20].lower().replace(' ', '_')}",
                    category="research",
                    title=f"Research Insight: {card.get('title')}",
                    content=f"Card Title: {card.get('title')}. Description: {card.get('description')}",
                    source_url=domain,
                    source_context="research.homepage_cards",
                )
            )

        # 6. Contact category
        contact = data.get("contact", {})
        channels_str = " | ".join(
            f"{c.get('purpose')}: {c.get('value')} ({c.get('note', '')})"
            for c in contact.get("channels", [])
        )
        meeting = contact.get("meeting_form", {})
        project_enquiry = contact.get("project_enquiry_form", {})
        items.append(
            KnowledgeIndexItem(
                item_id="contact_channels",
                category="contact",
                title="Intellizo Softwares Contact Information & Inquiries",
                content=(
                    f"Official Channels: {channels_str}. "
                    f"Meeting Form Fields: {', '.join(meeting.get('fields', []))}. "
                    f"Meeting Types: {', '.join(meeting.get('meeting_types', []))}. "
                    f"Project Enquiry Service Options: {', '.join(project_enquiry.get('service_options', []))}"
                ),
                source_url=contact.get("source_url"),
                source_context="contact.channels",
            )
        )

        # 7. Careers category
        careers = data.get("careers", {})
        for op in careers.get("openings", []):
            op_title = op.get("title", "")
            resp = " | ".join(op.get("responsibilities", [])) if op.get("responsibilities") else ""
            skills = " | ".join(op.get("required_skills", [])) if op.get("required_skills") else ""
            items.append(
                KnowledgeIndexItem(
                    item_id=f"career_{op_title.lower().replace(' ', '_')}",
                    category="careers",
                    title=f"Career Opening: {op_title} ({op.get('location')})",
                    content=(
                        f"Title: {op_title}. Location: {op.get('location')}. "
                        f"Type: {op.get('type')}. Experience: {op.get('experience')}. "
                        f"Summary: {op.get('summary')}. Responsibilities: {resp}. "
                        f"Required Skills: {skills}. Note: {careers.get('note')}"
                    ),
                    source_url=careers.get("source_url"),
                    source_context="careers.openings",
                )
            )

        # 8. Privacy category
        privacy = data.get("privacy_policy", {})
        sections = privacy.get("sections", {})
        for sec_name, sec_val in sections.items():
            sec_val_str = ", ".join(sec_val) if isinstance(sec_val, list) else str(sec_val)
            items.append(
                KnowledgeIndexItem(
                    item_id=f"privacy_{sec_name}",
                    category="privacy",
                    title=f"Privacy Policy: {sec_name.replace('_', ' ').title()}",
                    content=f"Section: {sec_name}. Content: {sec_val_str}",
                    source_url=privacy.get("source_url"),
                    source_context=f"privacy_policy.{sec_name}",
                )
            )

        # 9. Navigation category
        nav = data.get("navigation", [])
        for link in nav:
            area = link.get("area", "")
            items.append(
                KnowledgeIndexItem(
                    item_id=f"nav_{area.lower().replace(' ', '_').replace('&', 'and')}",
                    category="navigation",
                    title=f"Navigation: {area}",
                    content=f"Website Navigation Link for {area}: {link.get('url')}",
                    source_url=link.get("url"),
                    source_context="navigation",
                )
            )

        self._index = items
        self._is_indexed = True
        logger.info("Knowledge index constructed with %d items.", len(self._index))

    def get_index(self) -> List[KnowledgeIndexItem]:
        if not self._is_indexed:
            self.build_index()
        return self._index


knowledge_service = KnowledgeService()
