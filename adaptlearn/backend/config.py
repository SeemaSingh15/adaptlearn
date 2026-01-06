from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    LLM_PROVIDER: str = "ollama"
    OLLAMA_BASE_URL: str = "http://localhost:11434/api"
    OLLAMA_MODEL: str = "qwen3-coder:480b-cloud"
    
    GEMINI_API_KEY: Optional[str] = None
    
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    
    DATABASE_URL: str = "sqlite:///./adaptlearn.db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
