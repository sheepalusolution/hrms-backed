from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USER: str = "hrms_user"
    DB_PASSWORD: str = "Aayush%40123"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "hrms_db"

    # DO NOT let env override this
    SQLALCHEMY_DATABASE_URL: str = ""

    SECRET_KEY: str = "supersecretkey123"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    DEBUG: bool = True

    def __init__(self, **values):
        super().__init__(**values)

        # Force-build DB URL AFTER env parsing
        self.SQLALCHEMY_DATABASE_URL = (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

settings = Settings()
