from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Media/Content Service"
    DATABASE_URL: str
    RABBITMQ_URL: str
    S3_ENDPOINT_URL: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_BUCKET_NAME: str
    JWT_SECRET_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
