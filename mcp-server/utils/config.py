"""Configuration settings for Intellizo Softwares MCP Server."""

import os
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

def resolve_data_json_path() -> Path:
    """Resolve data.json file path using environment or candidate directories."""
    env_path = os.environ.get("DATA_JSON_PATH")
    if env_path:
        p = Path(env_path).resolve()
        if p.is_file():
            return p

    # Candidate locations relative to mcp-server or cwd
    current_file_dir = Path(__file__).resolve().parent
    candidates = [
        current_file_dir.parent.parent / "data.json",              # <root>/data.json from utils
        current_file_dir.parent.parent.parent / "data.json",       # outer root if nested
        current_file_dir.parent / "data.json",                     # inside mcp-server
        Path.cwd() / "data.json",                                  # cwd
        Path.cwd() / "company-mcp-plugin" / "data.json",           # cwd subdirectory
        Path.cwd().parent / "data.json",                           # parent of cwd
    ]

    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()

    # Fallback to standard relative path even if file not yet found
    return (current_file_dir.parent.parent / "data.json").resolve()


class Settings(BaseSettings):
    """Application settings."""
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Intellizo Softwares MCP Server"
    app_version: str = "1.0.0"
    company_name: str = "Intellizo Softwares"
    company_website: str = "https://www.intellizosoftwares.com/"
    tagline: str = "IDEAS ReEngineered"
    
    # Server configuration
    host: str = Field(default="127.0.0.1", alias="MCP_HOST")
    port: int = Field(default=8000, alias="MCP_PORT")
    streamable_http_path: str = Field(default="/mcp", alias="MCP_PATH")
    transport: str = Field(default="streamable-http", alias="MCP_TRANSPORT")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    
    # Data configuration
    data_json_path: Path = Field(default_factory=resolve_data_json_path, alias="DATA_JSON_PATH")


settings = Settings()
