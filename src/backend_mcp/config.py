
"""Configuration-Restaurant Backend MCP Server"""

import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional


class Setting(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"  # -----Ignore extra fields in .env
    )

    # -----API Configuration
    backend_url: str = Field(default="http://localhost:8080", description="Backend URL")
    backend_timeout: int = Field(default=30, description="HTTP request timeout")

    # -----API Authentication
    api_key: Optional[str] = Field(default=None, description="API key")
    api_secret: Optional[str] = Field(default=None, description="API secret")

    # -----Logging
    log_level: str = Field(default="INFO", description="Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)")

    # -----Environment
    environment: str = Field(default="development", description="Environment name (development, production, staging)")


settings = Setting() # -----Global setting instance
