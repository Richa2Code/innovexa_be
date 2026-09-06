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

    model_config = {
        "env_file": ".env",
        "extra": "ignore",
        "case_sensitive": True,
        "enable_decoding": "utf-8",
    }

    # Local Server
    # model_config = {
    #     "env_file": f".env.{ServerEnv().ENV}",
    #     "extra": "ignore",
    #     "case_sensitive": True,
    #     "enable_decoding": "utf-8",
    # }


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
