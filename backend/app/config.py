from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Local dev default: SQLite file, no setup needed.
    # For production: postgresql+psycopg2://user:pass@rds-endpoint:5432/foodshare
    database_url: str = "sqlite:///./foodshare.db"

    jwt_secret: str = "change-me-in-.env"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

    # AWS (leave blank for local dev; S3 upload / SNS notify are stubbed until set)
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_region: str = "ap-south-1"
    s3_bucket: str = ""
    sns_topic_arn: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
