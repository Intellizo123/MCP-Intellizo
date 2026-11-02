"""Root server entrypoint for Vercel and local ASGI runners."""

import importlib.util
import sys
from pathlib import Path

current_dir = Path(__file__).resolve().parent
mcp_server_dir = current_dir / "mcp-server"
if str(mcp_server_dir) not in sys.path:
    sys.path.insert(0, str(mcp_server_dir))

spec = importlib.util.spec_from_file_location("mcp_server_main", mcp_server_dir / "server.py")
mcp_mod = importlib.util.module_from_spec(spec)
sys.modules["mcp_server_main"] = mcp_mod
spec.loader.exec_module(mcp_mod)

app = mcp_mod.app
mcp_server = mcp_mod.mcp_server
get_asgi_app = mcp_mod.get_asgi_app
main = mcp_mod.main

if __name__ == "__main__":
    main()
