import secrets
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API: str = "/api/v1"
    PROJECT_NAME: str = "LSC"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 30 days
    SERVER_HOST: AnyHttpUrl
    BACKEND_CORS_ORIGIN: list[AnyHttpUrl] | str = []
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_URL: str

    @field_validator("BACKEND_CORS_ORIGIN", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list | str):
            return v
        raise ValueError(v)

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
