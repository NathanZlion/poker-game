from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    DB_NAME: str
    DB_USER: str
    DB_HOST: str
    DB_PORT: int
    DB_PASSWORD: str

    model_config = SettingsConfigDict(env_file=".env")
