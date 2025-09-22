from typing import Annotated
from uuid import UUID

from pydantic import AfterValidator, Field, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


def _validate_openai_api_key(v: str | None) -> str | None:
    """Validate that the OpenAI API key starts with 'sk-'."""
    if v and not v.startswith("sk-"):
        raise ValueError("OpenAI API key must start with 'sk-'")
    return v


def _validate_exa_api_key(v: str | None) -> str | None:
    """Validate that the Exa API key is a valid UUID4."""
    if v:
        try:
            UUID(v, version=4)
        except ValueError:
            raise ValueError("Exa API key must be a valid UUID4") from None
    return v


def _validate_tavily_api_key(v: str | None) -> str | None:
    """Validate that the Tavily API key starts with 'tvly-'."""
    if v and not v.startswith("tvly-"):
        raise ValueError("Tavily API key must start with 'tvly-'")
    return v


OpenAIAPIKey = Annotated[str | None, AfterValidator(_validate_openai_api_key)]
ExaAPIKey = Annotated[str | None, AfterValidator(_validate_exa_api_key)]
TavilyAPIKey = Annotated[str | None, AfterValidator(_validate_tavily_api_key)]


class Settings(BaseSettings):
    """Manages application settings and environment variables."""

    openai_api_key: OpenAIAPIKey = Field(default=None, alias="OPENAI_API_KEY")
    exa_api_key: ExaAPIKey = Field(default=None, alias="EXA_API_KEY")
    tavily_api_key: TavilyAPIKey = Field(default=None, alias="TAVILY_API_KEY")
    redis_uri: RedisDsn = Field(default="redis://localhost:6379", alias="REDIS_URL")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )


settings = Settings()
