# Intellizo Softwares MCP Server Application

> **Tagline:** IDEAS ReEngineered  
> **Official Website:** [https://www.intellizosoftwares.com/](https://www.intellizosoftwares.com/)  
> **Protocol:** Model Context Protocol (MCP)  
> **Transport:** Streamable HTTP (Default), Stdio, SSE  

A complete, production-ready Model Context Protocol (MCP) server application for **Intellizo Softwares**. This server connects AI hosts and MCP clients (including ChatGPT, Claude, Cursor, and custom agentic frameworks) directly to Intellizo's verified company knowledge base, service catalogues, AI agent capabilities, research articles, careers, and contact channels.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Folder Structure](#folder-structure)
4. [Technology Stack](#technology-stack)
5. [Installation](#installation)
6. [Environment Setup](#environment-setup)
7. [Running the MCP Server](#running-the-mcp-server)
8. [MCP Endpoints](#mcp-endpoints)
9. [Available MCP Tools (10 Implemented)](#available-mcp-tools-10-implemented)
10. [Example Tool Calls](#example-tool-calls)
11. [Testing Instructions](#testing-instructions)
12. [Guardrails & Response Accuracy](#guardrails--response-accuracy)
13. [ChatGPT Integration Instructions](#chatgpt-integration-instructions)
14. [Production Deployment Instructions](#production-deployment-instructions)
15. [Troubleshooting](#troubleshooting)

---

## Project Overview

Intellizo Softwares is an end-to-end software and AI consultancy focused on intelligent, scalable, tailor-made software products for operational excellence and growth.

This MCP server application exposes Intellizo's source-backed knowledge base (`data.json`) across ten dedicated tools. ChatGPT or any compatible MCP client acts as the reasoning engine, invoking tools on this server to retrieve grounded facts, URLs, and capabilities without hallucinating services, SLAs, or unverified claims.

### Key Capabilities

- **Zero External LLM Cost for Retrieval:** Uses deterministic, tokenized keyword matching with synonym expansion and category filtering.
- **RAG Response Policies & Guardrails:** Built-in safeguards report conflicting metrics, email address discrepancies, and time-sensitive job listings without inventing unlisted data.
- **Streamable HTTP & SSE Transport:** Supports modern Streamable HTTP protocol (`/mcp`) with session management, alongside stdio for local IDE tools.
- **Health-Check Mechanism:** Built-in `/health` endpoint for monitoring and uptime probes.

---

## Architecture

The application adopts a clean, layered service-oriented architecture:

```
[ MCP Client: ChatGPT / Cursor / Claude ]
                  │
                  ▼  (JSON-RPC 2.0 over Streamable HTTP / Stdio)
       [ Starlette / FastMCP App ]
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
  [ /health Route ]   [ Tool Manager ]
                            │
       ┌────────────────────┼────────────────────┐
       ▼                    ▼                    ▼
 [ Company Tools ]   [ Service Tools ]    [ AI & MCP Tools ]
 [ Contact Tools ]   [ Career Tools  ]    [ Search Tools   ]
       └────────────────────┬────────────────────┘
                            │
                            ▼
                    [ Services Layer ]
     ┌──────────────────────┼──────────────────────┐
     ▼                      ▼                      ▼
[ Company Service ] [ Retrieval Service ] [ Response Service ]
     └──────────────────────┼──────────────────────┘
                            │
                            ▼
                  [ utils / data_loader ]
                            │
                            ▼
              [ data.json Knowledge Base ]
```

- **Tools Layer (`tools/`):** Pure MCP tool definitions with Pydantic validation, explicit typing, and docstrings.
- **Services Layer (`services/`):** Domain logic, fuzzy service resolution, deterministic keyword indexing, and guardrail enforcement.
- **Models Layer (`models/`):** Pydantic schemas for request validation and structured response output.
- **Utils Layer (`utils/`):** Config resolution, structured logging, and schema-validated data loading.

---

## Folder Structure

```
company-mcp-plugin/
├── plugin.json                 # Plugin / App manifest metadata
├── mcp.json                    # MCP connection & endpoint configuration
├── data.json                   # Verified source knowledge base
├── README.md                   # Complete application documentation
├── .env.example                # Example environment variables
├── .gitignore                  # Git exclusions
├── assets/                     # App assets and icons
└── mcp-server/
    ├── server.py               # FastMCP server entrypoint & ASGI app factory
    ├── requirements.txt        # Pinned Python dependencies
    ├── tools/                  # 10 MCP tool implementations
    │   ├── __init__.py         # Tool registry & registration logic
    │   ├── search_tools.py     # search_company_knowledge
    │   ├── company_tools.py    # get_company_profile, get_company_navigation
    │   ├── service_tools.py    # get_services, get_service_details
    │   ├── ai_tools.py         # get_ai_capabilities, get_mcp_information
    │   ├── contact_tools.py    # get_company_contact
    │   ├── career_tools.py     # get_careers
    │   └── research_tools.py   # get_research_articles
    ├── services/               # Core business & retrieval logic
    │   ├── __init__.py
    │   ├── knowledge_service.py # Chunking & category indexing
    │   ├── retrieval_service.py # Deterministic keyword matching & synonyms
    │   ├── company_service.py   # Domain handlers for all 10 tools
    │   └── response_service.py  # Guardrail policies & conflict transparency
    ├── models/                 # Pydantic schemas
    │   ├── __init__.py
    │   ├── request_models.py   # Validated tool request inputs
    │   └── response_models.py  # Machine-readable response schemas
    ├── utils/                  # Core utilities
    │   ├── __init__.py
    │   ├── config.py           # Settings management with pydantic-settings
    │   ├── logger.py           # Structured logging setup
    │   └── data_loader.py      # JSON loading & structural validation
    └── tests/                  # Pytest automated test suite (37 tests)
        ├── __init__.py
        ├── test_data_loader.py
        ├── test_retrieval.py
        ├── test_company_tools.py
        ├── test_service_tools.py
        ├── test_ai_tools.py
        ├── test_contact_tools.py
        ├── test_research_career_tools.py
        └── test_client_integration.py
```

---

## Technology Stack

- **Python:** 3.10+ (tested on Python 3.14)
- **MCP Python SDK / FastMCP:** `mcp>=2.3.0`
- **Web & ASGI Engine:** `starlette`, `uvicorn[standard]`
- **Data Validation:** `pydantic>=2.8.0`, `pydantic-settings`
- **Testing:** `pytest`, `pytest-asyncio`, `httpx`
- **Knowledge Base:** JSON-based deterministic retrieval (`data.json`)

---

## Installation

### 1. Prerequisites

Ensure Python 3.10 or higher is installed:
```bash
python --version
```

### 2. Clone / Open Project

Navigate to the project root:
```bash
cd company-mcp-plugin/mcp-server
```

### 3. Create Virtual Environment

```bash
python -m venv .venv

# On Linux / macOS:
source .venv/bin/activate

# On Windows PowerShell:
.\.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Setup

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Configure parameters as needed:
```ini
# Host and port
MCP_HOST=127.0.0.1
MCP_PORT=8000

# Streamable HTTP endpoint path
MCP_PATH=/mcp

# Transport: streamable-http (default), stdio, or sse
MCP_TRANSPORT=streamable-http

# Logging
LOG_LEVEL=INFO

# Optional explicit path to data.json
DATA_JSON_PATH=../data.json
```

---

## Running the MCP Server

### Default: Streamable HTTP (Recommended for Web Clients & ChatGPT)

```bash
python server.py --transport streamable-http --host 127.0.0.1 --port 8000
```

### Stdio Transport (For local Claude Desktop or Cursor)

```bash
python server.py --transport stdio
```

### SSE Transport

```bash
python server.py --transport sse --host 127.0.0.1 --port 8000
```

---

## MCP Endpoints

When running in Streamable HTTP mode on `127.0.0.1:8000`:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/mcp` | `POST` | MCP JSON-RPC 2.0 protocol endpoint (Streamable HTTP with SSE streaming responses) |
| `/health` | `GET` | Health check endpoint returning server status, tools count, and version |

Verify server health:
```bash
curl http://127.0.0.1:8000/health
```
Response:
```json
{
  "status": "healthy",
  "server": "Intellizo Softwares MCP Server",
  "version": "1.0.0",
  "company": "Intellizo Softwares",
  "transport": "streamable-http",
  "endpoint": "/mcp",
  "tools_count": 10
}
```

---

## Available MCP Tools (10 Implemented)

### 1. `search_company_knowledge`
- **Purpose:** Search across all company information using deterministic keyword matching.
- **Inputs:**
  - `query` (string, required): Search phrase or keywords.
  - `category` (string, optional): One of `company`, `services`, `AI`, `MCP`, `research`, `contact`, `careers`, `privacy`, `navigation`.
  - `max_results` (integer, optional, default: 5): Maximum items to return.
- **Returns:** List of ranked results with title, content, category, source URL, source context, and relevance score.

### 2. `get_company_profile`
- **Purpose:** Retrieve the full company profile.
- **Inputs:** None.
- **Returns:** Name, tagline, description, mission, vision, operating priorities, principles, culture, global presence, teams overview, and metrics conflict disclosures.

### 3. `get_services`
- **Purpose:** Retrieve all six official company service categories.
- **Inputs:** None.
- **Returns:**
  1. System Design & Consultancy
  2. Web Application Development
  3. Mobile & Smart TV App Development
  4. AI Development & Integration
  5. Indoor Navigation Solutions
  6. Blockchain & NFT Development
  Plus technology stack labels and service overview URL.

### 4. `get_service_details`
- **Purpose:** Retrieve comprehensive details for a specific service with fuzzy/approximate matching.
- **Inputs:**
  - `service_name` (string, required): e.g. `"smart tv"`, `"indoor navigation"`, `"web dev"`, `"blockchain"`.
- **Returns:** Detailed capabilities, process stages, platform support, source URL, and fallback list if not found.

### 5. `get_ai_capabilities`
- **Purpose:** Retrieve AI capabilities, AI agent operational pillars, integration environments, and FAQs.
- **Inputs:** None.
- **Returns:** AI development services, core strategy capabilities, the 6 agent pillars (*Observe & Monitor, Analyze & Reason, Recommend & Support Decisions, Automate & Execute, Learn & Improve Over Time, Communicate & Collaborate*), integration environments, and FAQs.

### 6. `get_mcp_information`
- **Purpose:** Retrieve Intellizo MCP specifications.
- **Inputs:** None.
- **Returns:** Exact published expansion (*Model Context & Orchestration Layer*), summary, 3 use cases, listed environments (*Claude, Cursor, GitHub, OpenAI, Model Context Protocol*), and FAQs.

### 7. `get_company_contact`
- **Purpose:** Retrieve verified contact channels and inquiry information.
- **Inputs:** None.
- **Returns:** Business contact (`info@intellizo.in`), support contact (`support@intellizo.in`), meeting form fields, project enquiry form fields, email discrepancies, and action guardrail prohibiting simulated form submissions.

### 8. `get_careers`
- **Purpose:** Retrieve catalogued job openings.
- **Inputs:** None.
- **Returns:** Current listings (*Custom Software Engineer*, *UI / UX Designer*), department filters (*Tech, Design, Marketing, HR*), experience requirements, and time-sensitivity warning directing to the official careers page.

### 9. `get_research_articles`
- **Purpose:** Retrieve published research articles and whitepapers.
- **Inputs:** None.
- **Returns:** 6 published articles (*Beyond the Bot*, *The Efficiency Dividend*, *The 10x Developer*, *From Debt to Value*, *Building Stable and Scalable Digital Ecosystems*, *Integrating APIs, ERP and UX Excellence*), publication dates, read times, summaries, key points, URLs, and insights cards.

### 10. `get_company_navigation`
- **Purpose:** Retrieve official website links and navigation hierarchy.
- **Inputs:** None.
- **Returns:** Complete catalog of verified URLs categorized into Core, Services, AI & Tech, and Company & Governance.

---

## Example Tool Calls

### Call `search_company_knowledge` (via JSON-RPC)
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "search_company_knowledge",
    "arguments": {
      "query": "smart tv tizen webos",
      "category": "services"
    }
  }
}
```

### Call `get_service_details`
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "get_service_details",
    "arguments": {
      "service_name": "indoor navigation"
    }
  }
}
```

---

## Testing Instructions

The project includes an automated test suite verifying all 15 required scenarios across 37 test cases.

### Run All Unit and Integration Tests

```bash
# From company-mcp-plugin/mcp-server:
python -m pytest tests -v
```

### Test Coverage Highlights

- `test_data_loader.py`: Validates schema, required keys, and missing-file handling.
- `test_retrieval.py`: Tests keyword scoring, category filters, synonyms, empty queries, and unknown categories.
- `test_company_tools.py`: Tests company profile, metric discrepancies, and navigation URLs.
- `test_service_tools.py`: Tests all 6 services, exact matches, approximate/fuzzy matches, and unknown queries.
- `test_ai_tools.py`: Tests AI capabilities, 6 agent pillars, and exact MCP expansion preservation.
- `test_contact_tools.py`: Tests contact channels, email discrepancies, and inquiry submission guardrails.
- `test_research_career_tools.py`: Tests job openings, research articles, dates, read times, and claims notes.
- `test_client_integration.py`: Tests FastMCP tool discovery (all 10 tools), tool execution via MCP protocol, and HTTP health-check endpoint.

---

## Guardrails & Response Accuracy

This server implements the mandatory guardrails defined in `data.json`:

1. **No Fabricated Services:** Only the 6 published services are returned. Any unknown service request returns `found: false` with the official list.
2. **No Invented Pricing or SLAs:** Pricing, delivery timelines, certifications, and specific SLAs are not published; tools explicitly instruct the client to state this.
3. **Metric Discrepancy Transparency:** When reporting metrics, the server discloses the conflict between the homepage claim (108+ clients, 8+ countries) and the resources page (which showed 0 in rendered text, and 106 clients in indexed text).
4. **Email Address Integrity:** Reports contact email variations without silently picking one, and flags the known typo published on the privacy policy page (`info@intellizosofwtares.com`).
5. **Exact MCP Expansion Preserved:** Always preserves Intellizo's published expansion: *"Model Context & Orchestration Layer"*.
6. **No Simulated Submissions:** Prohibits pretending to send consultation requests or submit forms; returns official links to forms instead.

---

## ChatGPT Integration Instructions

To connect ChatGPT to your Intellizo Softwares MCP Server:

### Step 1: Deploy to Public HTTPS Endpoint
ChatGPT requires an accessible public HTTPS URL. Deploy the server using the instructions in the next section (e.g. `https://mcp.yourdomain.com`).

### Step 2: Configure ChatGPT / Custom GPT
1. In OpenAI ChatGPT, create or edit a Custom GPT (or use the Developer Actions / MCP connection setting).
2. Set the server URL to:
   ```
   https://mcp.yourdomain.com/mcp
   ```
3. Set Transport to **Streamable HTTP**.
4. ChatGPT will discover all 10 registered tools automatically via MCP tool discovery.

### Step 3: Local Development with ngrok / Cloudflare Tunnel
For local development and testing:
```bash
# Start your MCP server locally on port 8000
python server.py --host 127.0.0.1 --port 8000

# In another terminal, expose via ngrok or cloudflared:
ngrok http 8000
```
Use the provided `https://<subdomain>.ngrok-free.app/mcp` URL in your MCP client or ChatGPT.

---

## Production Deployment Instructions

### 1. Production ASGI Server (Gunicorn / Uvicorn)

Run using Uvicorn with multiple workers behind an ASGI factory:
```bash
uvicorn server:get_asgi_app --factory --host 0.0.0.0 --port 8000 --workers 4
```

### 2. Nginx Reverse Proxy Configuration with TLS

```nginx
server {
    listen 443 ssl http2;
    server_name mcp.intellizosoftwares.com;

    ssl_certificate /etc/letsencrypt/live/mcp.intellizosoftwares.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/mcp.intellizosoftwares.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;

        # Critical for Streamable HTTP and SSE chunked streaming
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Disable buffering for real-time SSE streaming
        proxy_buffering off;
        proxy_cache off;
        chunked_transfer_encoding on;
    }
}
```

### 3. Docker Deployment

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY mcp-server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY data.json .
COPY mcp-server/ ./mcp-server/

WORKDIR /app/mcp-server
ENV DATA_JSON_PATH=/app/data.json
ENV MCP_HOST=0.0.0.0
ENV MCP_PORT=8000

EXPOSE 8000

CMD ["python", "server.py", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t intellizo-mcp-server .
docker run -p 8000:8000 intellizo-mcp-server
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `FileNotFoundError: data.json` | `data.json` not located in search paths. | Set `DATA_JSON_PATH` environment variable pointing to the absolute path of `data.json`. |
| `ConnectionRefusedError` | Server is not running or listening on wrong interface. | Ensure server is started with `--host 0.0.0.0` or `127.0.0.1`. Check `/health` endpoint. |
| SSE / Streaming drops in ChatGPT | Nginx or proxy buffering SSE response stream. | Ensure `proxy_buffering off;` and `X-Accel-Buffering: no` are set on reverse proxy. |
| Tool returns "Service not found" | Query did not match any of the 6 official services. | Use `get_services` to inspect the 6 official categories. |

---

## License & Ownership

Copyright © 2026 Intellizo Softwares. All rights reserved.  
Knowledge content sourced from published materials at [https://www.intellizosoftwares.com/](https://www.intellizosoftwares.com/).
