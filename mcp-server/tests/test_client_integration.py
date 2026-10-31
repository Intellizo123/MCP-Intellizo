"""Integration tests for MCP tool discovery and execution via FastMCP / MCPServer."""

import pytest
from starlette.testclient import TestClient
from server import get_asgi_app, mcp_server


@pytest.mark.asyncio
async def test_mcp_tool_discovery():
    """Verify an MCP client discovers all 10 registered tools."""
    tools = await mcp_server.list_tools()
    tool_names = [t.name for t in tools]

    expected_tools = [
        "search_company_knowledge",
        "get_company_profile",
        "get_services",
        "get_service_details",
        "get_ai_capabilities",
        "get_mcp_information",
        "get_company_contact",
        "get_careers",
        "get_research_articles",
        "get_company_navigation",
    ]

    for expected in expected_tools:
        assert expected in tool_names, f"Expected tool '{expected}' not registered"

    assert len(tool_names) == 10


@pytest.mark.asyncio
async def test_mcp_call_search_tool():
    """Verify tool execution via MCP protocol call_tool."""
    result = await mcp_server.call_tool(
        name="search_company_knowledge",
        arguments={"query": "indoor navigation", "category": "services"},
    )
    assert result is not None
    # Result content check
    assert len(result.content) > 0
    first_block = result.content[0]
    assert hasattr(first_block, "text")
    assert "Indoor Navigation" in first_block.text


@pytest.mark.asyncio
async def test_mcp_call_profile_tool():
    """Verify get_company_profile execution via MCP protocol."""
    result = await mcp_server.call_tool(
        name="get_company_profile",
        arguments={},
    )
    assert result is not None
    text = result.content[0].text
    assert "Intellizo Softwares" in text
    assert "IDEAS ReEngineered" in text


@pytest.mark.asyncio
async def test_mcp_call_services_tool():
    """Verify get_services execution via MCP protocol."""
    result = await mcp_server.call_tool(
        name="get_services",
        arguments={},
    )
    assert result is not None
    text = result.content[0].text
    assert "System Design & Consultancy" in text
    assert "Web Application Development" in text


@pytest.mark.asyncio
async def test_mcp_call_service_details_tool():
    """Verify get_service_details execution via MCP protocol."""
    result = await mcp_server.call_tool(
        name="get_service_details",
        arguments={"service_name": "smart tv"},
    )
    assert result is not None
    text = result.content[0].text
    assert "Mobile & Smart TV App Development" in text


@pytest.mark.asyncio
async def test_mcp_call_mcp_information_tool():
    """Verify get_mcp_information execution via MCP protocol."""
    result = await mcp_server.call_tool(
        name="get_mcp_information",
        arguments={},
    )
    assert result is not None
    text = result.content[0].text
    assert "Model Context & Orchestration Layer" in text


def test_http_health_check_endpoint():
    """Verify HTTP health check endpoint returns 200 and healthy status."""
    app = get_asgi_app()
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["tools_count"] == 10
        assert data["company"] == "Intellizo Softwares"
