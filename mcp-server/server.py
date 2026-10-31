"""Intellizo Softwares Production MCP Server Application.

Exposes company knowledge, services, AI capabilities, MCP information,
contact details, careers, research articles, and site navigation through
the Model Context Protocol (MCP) using FastMCP / Streamable HTTP.
"""

import argparse
import sys
from typing import Any

from starlette.requests import Request
from starlette.responses import JSONResponse, Response

try:
    from mcp.server.mcpserver import MCPServer as FastMCP
except ImportError:
    from mcp.server.fastmcp import FastMCP

from tools import ALL_TOOLS, register_tools
from utils.config import settings
from utils.data_loader import load_knowledge_base
from utils.logger import logger


def create_mcp_server() -> FastMCP:
    """Initialize and configure FastMCP server with tools and custom routes."""
    # Pre-validate and load knowledge base
    try:
        load_knowledge_base()
        logger.info("Knowledge base pre-loaded successfully.")
    except Exception as exc:
        logger.error("Failed to load knowledge base on startup: %s", exc)
        raise

    server = FastMCP(
        name="IntellizoCompanyServer",
        instructions=(
            "You are the official Intellizo Softwares MCP Knowledge Assistant. "
            "Use the registered tools to provide accurate, verified information about "
            "Intellizo Softwares' profile, services, AI offerings, MCP integration, "
            "contact channels, research papers, and career openings. "
            "Never invent non-existent services, pricing, or SLAs. Follow the RAG response policies."
        ),
    )

    # Register all 10 MCP tools
    register_tools(server)

    # Health check route
    @server.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> Response:
        return JSONResponse(
            {
                "status": "healthy",
                "server": settings.app_name,
                "version": settings.app_version,
                "company": settings.company_name,
                "transport": settings.transport,
                "endpoint": settings.streamable_http_path,
                "tools_count": len(ALL_TOOLS),
            }
        )

    return server


# Global server instance
mcp_server = create_mcp_server()


def get_asgi_app():
    """Return the Starlette ASGI application for Streamable HTTP."""
    return mcp_server.streamable_http_app(
        streamable_http_path=settings.streamable_http_path,
        host=settings.host,
    )


def main():
    """Entry point for running the MCP server."""
    parser = argparse.ArgumentParser(description="Intellizo Softwares MCP Server")
    parser.add_argument(
        "--transport",
        choices=["streamable-http", "stdio", "sse"],
        default=settings.transport,
        help="Transport protocol (default: streamable-http)",
    )
    parser.add_argument(
        "--host",
        default=settings.host,
        help=f"Host address for HTTP server (default: {settings.host})",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=settings.port,
        help=f"Port for HTTP server (default: {settings.port})",
    )
    parser.add_argument(
        "--path",
        default=settings.streamable_http_path,
        help=f"Path for Streamable HTTP endpoint (default: {settings.streamable_http_path})",
    )

    args = parser.parse_args()

    logger.info("Starting %s v%s", settings.app_name, settings.app_version)
    logger.info("Transport: %s", args.transport)

    if args.transport == "streamable-http":
        logger.info(
            "Streamable HTTP MCP endpoint: http://%s:%d%s",
            args.host,
            args.port,
            args.path,
        )
        logger.info("Health check endpoint: http://%s:%d/health", args.host, args.port)
        mcp_server.run(
            transport="streamable-http",
            host=args.host,
            port=args.port,
            streamable_http_path=args.path,
        )
    elif args.transport == "sse":
        logger.info("SSE MCP endpoint: http://%s:%d/sse", args.host, args.port)
        mcp_server.run(transport="sse", host=args.host, port=args.port)
    elif args.transport == "stdio":
        logger.info("Running on stdio transport...")
        mcp_server.run(transport="stdio")


if __name__ == "__main__":
    main()
