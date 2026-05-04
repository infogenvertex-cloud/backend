from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database Configuration - Individual components
    DB_HOST: str = "gateway01.ap-northeast-1.prod.aws.tidbcloud.com"
    DB_PORT: int = 4000
    DB_USERNAME: str = "CrR1v2rQYoMqsCW.root"
    DB_PASSWORD: str = ""  # Set in environment variables
    DB_DATABASE: str = "gym_db"
    
    # Legacy DATABASE_URL support (fallback)
    DATABASE_URL: str = ""
    
    GUPSHUP_API_KEY: str = ""
    GUPSHUP_APP_NAME: str = ""
    GUPSHUP_SOURCE_NUMBER: str = ""
    BASE_URL: str = "https://backend-gamma-seven-22.vercel.app"
    FRONTEND_URL: str = ""  # Frontend URL for CORS
    SCHEDULER_HOUR: int = 8
    SCHEDULER_MINUTE: int = 0
    EXPIRY_REMINDER_DAYS: int = 5
    WHATSAPP_TOKEN: str = ""
    WHATSAPP_PHONE_ID: str = ""
    JWT_SECRET_KEY: str = "gym-management-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_MINUTES: int = 1440

    model_config = SettingsConfigDict(env_file=".env")
    
    @property
    def database_url(self) -> str:
        """Construct database URL from individual components"""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        
        if self.DB_PASSWORD:
            # TiDB Cloud requires SSL - use proper SSL parameters
            return f"mysql+pymysql://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}?ssl_ca=&ssl_verify_cert=true&ssl_verify_identity=true"
        else:
            # Fallback to SQLite if no database credentials
            return "sqlite:///./gym.db"


settings = Settings()
