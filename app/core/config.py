from pydantic_settings  import BaseSettings
from pydantic import Field

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
    JWT_PRIVATE_KEY_PATH: str = Field(..., env="JWT_PRIVATE_KEY_PATH")
    JWT_PUBLIC_KEY_PATH: str = Field(..., env="JWT_PUBLIC_KEY_PATH")
    JWT_ALGORITHM: str = Field("RS256", env="JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60 * 24, env="ACCESS_TOKEN_EXPIRE_MINUTES")  # default 1 day
    REFRESH_TOKEN_EXPIRE_DAYS: int
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
settings = Settings()
