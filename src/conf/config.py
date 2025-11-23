from pydantic_settings import BaseSettings
from pathlib import Path
from dotenv import load_dotenv

# Construct an absolute path to the .env file and load it
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
if env_path.is_file():
    load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    redis_url: str = "redis://localhost:6379"
    REDIS_URL: str = "redis://localhost:6379"
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/db"

    class Config:
        # Pydantic will now read the settings from the environment variables
        # We don't need to specify env_file here as we've already loaded it.
        pass


settings = Settings()
