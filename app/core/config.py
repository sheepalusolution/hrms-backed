from pydantic import BaseSettings

class Settings(BaseSettings):
    # Database settings
    DB_USER: str = "hrms_user"
    DB_PASSWORD: str = "Aayush@123"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "hrms_db"

    # SQLAlchemy database URL
    SQLALCHEMY_DATABASE_URL: str = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    # JWT / security settings
    SECRET_KEY: str = "supersecretkey123"  # Change for production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # 1 hour
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7  # 7 days
    DEBUG: bool = True  # Set False in production

# Single settings instance
settings = Settings()
