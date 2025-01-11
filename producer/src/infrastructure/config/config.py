from pathlib import Path

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str

    # DB
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_TYPE: str
    DB_DRIVER: str

    # MinIO
    MINIO_ENDPOINT: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_BUCKET_NAME: str

    # RabbitMQ
    RABBITMQ_URL: str
    RABBITMQ_QUEUE: str

    # Auth
    AUTH_SERVER_URL: str
    USERINFO_URI: str

    #jwt
    JWT_PUBLIC_KEY_PATH: Path
    JWT_ALGORITHM: str = "RS256"
    __public_key = None

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = 'ignore'

    @property
    def DB_URL(self):
        return f'{self.DB_TYPE}+{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    @property
    def JWT_PUBLIC_KEY(self):
        if not self.__public_key:
            with open(self.JWT_PUBLIC_KEY_PATH) as f:
                self.__public_key = f.read()
                return self.__public_key
        return self.__public_key


settings = Settings()
