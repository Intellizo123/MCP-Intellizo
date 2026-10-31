# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DATA_JSON_PATH=/app/data.json \
    MCP_HOST=0.0.0.0 \
    MCP_PORT=8000 \
    MCP_PATH=/mcp \
    MCP_TRANSPORT=streamable-http \
    LOG_LEVEL=INFO

WORKDIR /app

# Install curl for container health check
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY mcp-server/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy knowledge base and server source code
COPY data.json /app/data.json
COPY mcp-server /app/mcp-server

WORKDIR /app/mcp-server

# Expose internal MCP server port
EXPOSE 8000

# Container health probe
HEALTHCHECK --interval=15s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://127.0.0.1:8000/health || exit 1

# Start the MCP server using Streamable HTTP transport
CMD ["python", "server.py", "--host", "0.0.0.0", "--port", "8000", "--transport", "streamable-http"]

