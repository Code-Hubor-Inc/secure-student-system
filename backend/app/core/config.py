from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Secure Student System"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"

    DATABASE_URL: str
    REDIS_URL: str = "redis://localhost:6379"

    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ENCRYPTION_KEY: str

    UPLOAD_DIR: str = "./storage/uploads"
    MAX_FILE_SIZE: int = 104857600

    class Config:
        env_file = ".env"


settings = Settings()
