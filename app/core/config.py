from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = Field(default="HRMS Backend")
    API_V1_STR: str = Field(default="/api/v1")

    # JWT
    SECRET_KEY: str = Field(default="CHANGE_ME")
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60)

    # Database
    DATABASE_URL: str = Field(
        default="postgresql://hrms_user:Aayush123@localhost/hrms_db"
    )

    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }


settings = Settings()
