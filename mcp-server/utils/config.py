"""Configuration settings for Intellizo Softwares MCP Server."""

import os
from pathlib import Path
from typing import Any, Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def resolve_data_json_path(candidate_path: Optional[Any] = None) -> Path:
    """Resolve data.json file path reliably across environments (Render, Docker, local, Vercel)."""
    if candidate_path:
        p = Path(str(candidate_path))
        if p.is_file():
            return p.resolve()

    env_path = os.environ.get("DATA_JSON_PATH")
    if env_path:
        p = Path(env_path)
        if p.is_file():
            return p.resolve()

    # Candidate locations relative to mcp-server or cwd
    current_file_dir = Path(__file__).resolve().parent
    candidates = [
        current_file_dir.parent.parent / "data.json",              # <root>/data.json from utils
        current_file_dir.parent / "data.json",                     # inside mcp-server
        current_file_dir.parent.parent.parent / "data.json",       # outer root if nested
        Path.cwd() / "data.json",                                  # cwd
        Path.cwd() / "mcp-server" / "data.json",                   # cwd/mcp-server
        Path.cwd().parent / "data.json",                           # parent of cwd
        Path("/opt/render/project/src/data.json"),                 # Render root
        Path("/opt/render/project/src/mcp-server/data.json"),      # Render mcp-server
        Path("/app/data.json"),                                    # Docker container root
        Path("/app/mcp-server/data.json"),                         # Docker mcp-server
    ]

    for candidate in candidates:
        try:
            if candidate.is_file():
                return candidate.resolve()
        except Exception:
            continue

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

    @field_validator("data_json_path", mode="before")
    @classmethod
    def validate_data_json_path(cls, v: Any) -> Path:
        """Ensure data_json_path resolves to an actual existing file."""
        return resolve_data_json_path(v)


settings = Settings()
