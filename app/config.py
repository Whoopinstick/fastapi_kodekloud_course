from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_host: str
    database_port: str
    database_name: str
    database_user: str
    database_password: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    test_database_host: str
    test_database_port: str
    test_database_name: str
    test_database_user: str
    test_database_password: str

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
