import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = "FlowGenie"
    app_version: str = "1.0.0"
    host: str = os.getenv("HOST", "127.0.0.1")
    port: int = int(os.getenv("PORT", "8000"))
    debug: bool = os.getenv("DEBUG", "false").lower() in {"1", "true", "yes"}
    groq_api_key: str | None = os.getenv("GROQ_API_KEY")
    tavily_api_key: str | None = os.getenv("TAVILY_API_KEY")
    google_maps_api_key: str | None = os.getenv("GOOGLE_MAPS_API_KEY")


settings = Settings()