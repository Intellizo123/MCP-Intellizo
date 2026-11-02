"""Intellizo Softwares Production MCP Server Application.

Exposes company knowledge, services, AI capabilities, MCP information,
contact details, careers, research articles, and site navigation through
the Model Context Protocol (MCP) using FastMCP / Streamable HTTP.
"""

import argparse
import sys
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mcp.server.streamable_http_manager import TransportSecuritySettings
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

    return server


# Global FastMCP server instance
mcp_server = create_mcp_server()

# Configure transport security (disabling DNS rebinding protection for cloud hosts like Vercel)
transport_security = TransportSecuritySettings(enable_dns_rebinding_protection=False)
mcp_asgi_app = mcp_server.streamable_http_app(
    streamable_http_path=settings.streamable_http_path,
    transport_security=transport_security,
)

# Top-level FastAPI instance (required by Vercel, Uvicorn, and cloud ASGI runtimes)
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Intellizo Softwares Production MCP Server",
    lifespan=mcp_asgi_app.router.lifespan_context,
)

# Enable CORS for web and cloud MCP clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring, Vercel, and container probes."""
    return {
        "status": "healthy",
        "server": settings.app_name,
        "version": settings.app_version,
        "company": settings.company_name,
        "transport": settings.transport,
        "endpoint": settings.streamable_http_path,
        "tools_count": len(ALL_TOOLS),
    }


@app.get("/")
async def root():
    """Root endpoint providing service information."""
    return {
        "status": "online",
        "server": settings.app_name,
        "version": settings.app_version,
        "docs_url": "/docs",
        "health_url": "/health",
        "mcp_endpoint": settings.streamable_http_path,
    }


# Mount the MCP Streamable HTTP app
app.mount("", mcp_asgi_app)


def get_asgi_app():
    """Return the ASGI application instance."""
    return app


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
        import uvicorn

        uvicorn.run(
            app,
            host=args.host,
            port=args.port,
            log_level=settings.log_level.lower(),
        )
    elif args.transport == "sse":
        logger.info("SSE MCP endpoint: http://%s:%d/sse", args.host, args.port)
        mcp_server.run(transport="sse", host=args.host, port=args.port)
    elif args.transport == "stdio":
        logger.info("Running on stdio transport...")
        mcp_server.run(transport="stdio")


if __name__ == "__main__":
    main()
