from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    openai_api_key: str = ""
    gemini_api_key: str = ""
    groq_api_key: str
    gmail_user: str = ""
    gmail_password: str = ""

    class Config:
        env_file = ".env"


settings = Settings()