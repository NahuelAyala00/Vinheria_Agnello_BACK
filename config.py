from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Configurações do Banco de Dados
    DATABASE_URL: str = "postgresql://postgres:161102@localhost:5432/postgres"
    
    # Google OAuth
    GOOGLE_CLIENT_ID: str = "210589865475-o09jvfs1i2o8hrfqhq2mstbn7pdc280r.apps.googleusercontent.com"
    GOOGLE_CLIENT_SECRET: str = "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"
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/auth/google/callback"
    
    # JWT Settings
    SECRET_KEY: str = "nahuelisaiasayalamolinas"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Configurações da aplicação
    APP_NAME: str = "Sistema de Login"
    DEBUG: bool = True

settings = Settings()
