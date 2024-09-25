from logging import config as logging_config
from pydantic import Field
from pydantic_settings import BaseSettings

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    DEBUG: bool = Field(default=1, env='DEBUG')

    SECRET_KEY: str = Field(..., env='SECRET_KEY')
    ALGORITHM: str = Field(..., env='ALGORITHM')
    ACCESS_TOKEN_EXPIRE_DAYS:  int = Field(..., env='ACCESS_TOKEN_EXPIRE_DAYS')
    REFRESH_TOKEN_EXPIRE_DAYS:  int = Field(..., env='REFRESH_TOKEN_EXPIRE_DAYS')

    PROJECT_NAME: str = Field(..., env='PROJECT_NAME')

    POSTGRES_HOST: str = Field(..., env='POSTGRES_HOST')
    POSTGRES_PORT: str = Field(..., env='POSTGRES_PORT')
    POSTGRES_USER: str = Field(..., env='POSTGRES_USER')
    POSTGRES_PASSWORD: str = Field(..., env='POSTGRES_PASSWORD')
    POSTGRES_DB: str = Field(..., env='POSTGRES_DB')

    class Config:
        env_file = '.env'


settings = Settings()
