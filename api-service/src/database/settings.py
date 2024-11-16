from pydantic_settings import BaseSettings
from pydantic import Field


class DatabaseSettings(BaseSettings):
    db_host: str = Field(..., env="DB_HOST")

    db_port: int = Field(env="DB_PORT", default=5432)

    postgres_user: str = Field(..., env="POSTGRES_USER")

    postgres_password: str = Field(..., env="POSTGRES_PASSWORD")

    postgres_db: str = Field(..., env="POSTGRES_DB")

    postgres_driver: str = Field(..., env="POSTGRES_DRIVER")

    @property
    def db_url(self) -> str:
        return f"{self.postgres_driver}://{self.postgres_user}:{self.postgres_password}@{self.db_host}:{self.db_port}/{self.postgres_db}"

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


db_settings = DatabaseSettings(_env_file='.env')
