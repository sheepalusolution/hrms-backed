from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database configuration
    DB_USER: str = "hrms_user"
    DB_PASSWORD: str = "Aayush%40123"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "hrms_db"
    SQLALCHEMY_DATABASE_URL: str = ""  # Will be auto-built

    # JWT configuration
    SECRET_KEY: str = "supersecretkey123"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # 1 hour
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    DEBUG: bool = True

    def __init__(self, **values):
        super().__init__(**values)
        # Build the DB URL dynamically
        self.SQLALCHEMY_DATABASE_URL = (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


# Create a single settings instance to use across the app
settings = Settings()
