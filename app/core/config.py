from pydantic_settings  import BaseSettings

class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    DATABASE_URL_MASTER: str
    DATABASE_URL_TEMPLATE: str
    REDIS_URL: str
    JWT_PRIVATE_KEY_PATH: str
    JWT_PUBLIC_KEY_PATH: str
    JWT_ALGORITHM: str = "RS256"
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 3600
    S3_ENDPOINT: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_BUCKET: str

    class Config:
        env_file = ".env"

settings = Settings()
