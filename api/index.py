"""Vercel serverless function entrypoint for Intellizo Softwares MCP Server."""

import importlib.util
import sys
from pathlib import Path

current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent
mcp_server_dir = project_root / "mcp-server"

if str(mcp_server_dir) not in sys.path:
    sys.path.insert(0, str(mcp_server_dir))
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

spec = importlib.util.spec_from_file_location("mcp_server_main", mcp_server_dir / "server.py")
mcp_mod = importlib.util.module_from_spec(spec)
sys.modules["mcp_server_main"] = mcp_mod
spec.loader.exec_module(mcp_mod)

app = mcp_mod.app
