from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env")

    database_url: str
    secret_key: str
    openai_api_key: str = ""
    gemini_api_key: str = ""
    groq_api_key: str
    gmail_user: str = ""
    gmail_password: str = ""
    resend_api_key: str = ""
    scheduler_secret_key: str = ""


settings = Settings()