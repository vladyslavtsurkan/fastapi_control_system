from pydantic import IPvAnyAddress
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    class Config:
        env_file = (".env", "../.env")
        env_file_encoding = "utf-8"

    DB_HOST: IPvAnyAddress | str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    SECRET_AUTH: str

    REDIS_HOST: IPvAnyAddress | str
    REDIS_PORT: int

    SMTP_HOST: IPvAnyAddress | str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str
