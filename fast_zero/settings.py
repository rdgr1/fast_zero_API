from pydantic_settigns import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
model_config = SettingsConfigDict(env=file'.env', env_file_encoding='utf-8')
    DATABASE_URL: str
