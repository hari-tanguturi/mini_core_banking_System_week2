from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Week 2: Products CRUD API implementation for Mini Core Banking System"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/mini_core_banking"
    
    # Auth configuration
    SECRET_KEY: str = "super_secret_key_for_week2_dummy_admin_login_12345"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    model_config = SettingsConfigDict(case_sensitive=True)

settings = Settings()
