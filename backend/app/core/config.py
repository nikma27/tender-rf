from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    app_name: str = "Tender RF API"
    debug: bool = False
    database_url: str = "postgresql://postgres:postgres@localhost:5432/tender_rf"

    class Config:
        env_file = ".env"


settings = Settings()
