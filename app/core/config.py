from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os
# Load environment variables from .env
load_dotenv()

# Fetch database variables
USER = os.getenv("dbuser")
PASSWORD = os.getenv("dbpassword")
HOST = os.getenv("dbhost")
PORT = os.getenv("dbport")
DBNAME = os.getenv("dbname")
SECRET = os.getenv("JWT_SECRET")
ALGORITHM=os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES=os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

# Google OAuth
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

# Frontend URL
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:7010")

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PROJECT_NAME: str = "JaneJase API"
    VERSION: str = "0.1.0"

    # 개발: http://localhost:7010 (React)
    CORS_ORIGINS: list[str] = ["http://localhost:7010", "http://127.0.0.1:7010"]

    # Database connection parameters
    DB_USER: str = USER
    DB_PASSWORD: str = PASSWORD
    DB_HOST: str = HOST
    DB_PORT: str = PORT
    DB_NAME: str = DBNAME

    # JWT
    JWT_SECRET: str = SECRET
    JWT_ALGORITHM: str = ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES: int = ACCESS_TOKEN_EXPIRE_MINUTES

    # Google OAuth
    GOOGLE_CLIENT_ID: str = GOOGLE_CLIENT_ID
    GOOGLE_CLIENT_SECRET: str = GOOGLE_CLIENT_SECRET
    GOOGLE_REDIRECT_URI: str = GOOGLE_REDIRECT_URI

    # Frontend URL
    FRONTEND_URL: str = FRONTEND_URL

settings = Settings()
