"""Tests for contact and communication tools."""

from tools.contact_tools import get_company_contact


def test_get_company_contact():
    """Scenario 7: Retrieve company contact."""
    res = get_company_contact()
    assert res["business_contact"] == "info@intellizo.in"
    assert res["support_contact"] == "support@intellizo.in"
    assert "https://www.intellizosoftwares.com/" in res["official_website"]
    assert "contact.html" in res["official_contact_page"]

    # Check channels list
    channels = res["channels"]
    purposes = [c["purpose"] for c in channels]
    assert "Business" in purposes
    assert "Queries / support" in purposes
    assert "Advertising Division" in purposes
    assert "General footer / newsletter" in purposes
    assert any("Privacy Policy" in p for p in purposes)

    # Check meeting form and project enquiry forms
    assert "Full Name" in res["meeting_form"]["fields"]
    assert "Project Consultation" in res["meeting_form"]["meeting_types"]
    assert "Preferred Call Time" in res["project_enquiry_form"]["fields"]
    assert "AI & Machine Learning" in res["project_enquiry_form"]["service_options"]


def test_contact_discrepancy_and_action_guardrail():
    """Verify email discrepancies and form submission guardrails."""
    res = get_company_contact()
    # Email discrepancies reported
    discrepancies = res["email_discrepancies"]
    assert any("info@intellizo.in" in d for d in discrepancies)
    assert any("info@intellizosofwtares.com" in d for d in discrepancies)  # published typo noted

    # Action guardrail prohibits pretending to submit
    guardrail = res["action_guardrail"]
    assert "not permitted" in guardrail
    assert "contact.html" in guardrail
