from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./gym.db"  # Default fallback
    GUPSHUP_API_KEY: str = ""
    GUPSHUP_APP_NAME: str = ""
    GUPSHUP_SOURCE_NUMBER: str = ""
    BASE_URL: str = "https://backend-gamma-seven-22.vercel.app"  # Production URL
    SCHEDULER_HOUR: int = 8
    SCHEDULER_MINUTE: int = 0
    EXPIRY_REMINDER_DAYS: int = 5
    WHATSAPP_TOKEN: str = ""
    WHATSAPP_PHONE_ID: str = ""
    JWT_SECRET_KEY: str = "gym-management-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_MINUTES: int = 1440

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
