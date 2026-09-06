from functools import lru_cache
from pydantic_settings import BaseSettings


class ServerEnv(BaseSettings):
    ENV: str = "dev"

    model_config = {
        "env_file": ".env",
        "extra": "ignore",
        "case_sensitive": True,
        "enable_decoding": "utf-8",
    }


class Settings(BaseSettings):
    APP_NAME: str = "Innovexa"

    # Database
    DATABASE_URL: str

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRY: int = 60
    JWT_REFRESH_TOKEN_EXPIRY: int = 1440

    # Services
    BREVO_API_KEY: str = ""
    BREVO_SENDER_EMAIL: str = "noreply@example.com"
    BREVO_SENDER_NAME: str = "Innovexa"

    # CORS Configuration
    CORS_ORIGINS: list[str] = [
        "https://scheme-setu-ai.netlify.app",
        "https://scheme-setu-ai.netlify.app/",
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ]

    model_config = {
        "env_file": ".env",
        "extra": "ignore",
        "case_sensitive": True,
        "enable_decoding": "utf-8",
    }


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
