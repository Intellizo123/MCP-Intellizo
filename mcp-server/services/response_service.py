"""Guardrails, response policies, and conflict management."""

from typing import Any, Dict, List
from utils.data_loader import get_knowledge_base


class ResponseService:
    """Service to enforce RAG response policies and guardrails."""

    @staticmethod
    def get_policies() -> List[str]:
        """Return published RAG response policies from data.json."""
        data = get_knowledge_base()
        return data.get("rag_response_policy", [])

    @staticmethod
    def get_known_conflicts() -> List[Dict[str, Any]]:
        """Return known conflicts from data.json."""
        data = get_knowledge_base()
        return data.get("known_conflicts", [])

    @staticmethod
    def get_metrics_conflict_note() -> str:
        """Formatted note about company metrics discrepancy."""
        return (
            "Metric Discrepancy Note: Homepage claims 108+ clients and 8+ countries. "
            "However, rendered Resources page shows 0 for countries, clients, and team members; "
            "an indexed version showed 8+ countries, 106 clients, and 25 AI products. "
            "These numbers are published company claims and are not independently verified."
        )

    @staticmethod
    def get_contact_discrepancy_note() -> List[str]:
        """Formatted details about email address discrepancies."""
        return [
            "Contact Page: info@intellizo.in, support@intellizo.in",
            "General Footer: hello@intellizosoftwares.com (variant: hello@intellizo.com)",
            "Privacy Policy: info@intellizosofwtares.com (contains an evident typo as published on the site)",
        ]

    @staticmethod
    def get_action_guardrail() -> str:
        """Action guardrail for inquiries, consultation, and bookings."""
        return (
            "Guardrail: Autonomous form submission, booking, or enquiry dispatch is not permitted. "
            "Please direct the user to the official contact flow at https://intellizosoftwares.com/contact.html "
            "or use the verified email info@intellizo.in."
        )

    @staticmethod
    def get_mcp_guardrail() -> str:
        """MCP terminology guardrail."""
        return (
            "Guardrail: Intellizo Softwares expands MCP as 'Model Context & Orchestration Layer' "
            "(rather than purely Model Context Protocol). Listed environments (Claude, Cursor, GitHub, OpenAI) "
            "reflect published website wording, not an independently verified compatibility matrix."
        )

    @staticmethod
    def get_careers_guardrail() -> str:
        """Careers guardrail."""
        return (
            "Guardrail: Job listings captured in the knowledge base are time-sensitive and may become outdated. "
            "Direct applicants to the official careers page at https://www.intellizosoftwares.com/career.html."
        )


response_service = ResponseService()
