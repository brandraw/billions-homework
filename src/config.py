from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSettings(BaseSettings):
    JWT_SECRET: str = "change-this-secret"
    JWT_ALG: str = "HS256"
    JWT_EXP_MINUTES: int = 60
    REFRESH_TOKEN_EXP_DAYS: int = 30


class Settings(AuthSettings):
    ENV: str = "development"
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/lms_db"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
