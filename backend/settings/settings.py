from pydantic import BaseSettings
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60
    APP_NAME: str
    DATABASE_CERTIFICATE = os.path.join(BASE_DIR, "settings", "accountCertificate.json")

    class Config:
        env_file = os.path.join(BASE_DIR, ".env")


settings = Settings()