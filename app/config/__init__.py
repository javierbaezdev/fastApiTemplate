import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self):
        self.env = self._get_env_variable("ENV")
        self.SECRET_KEY = self._get_env_variable("SECURITY_SECRET_KEY")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(
            self._get_env_variable("SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES")
        )
        self.REFRESH_KEY = self._get_env_variable("REFRESH_SECRET_KEY")
        self.REFRESH_TOKEN_EXPIRE_MINUTES = int(
            self._get_env_variable("REFRESH_ACCESS_TOKEN_EXPIRE_MINUTES")
        )
        self.RECOVERY_KEY = self._get_env_variable("RECOVERY_SECRET_KEY")
        self.RECOVERY_TOKEN_EXPIRE_MINUTES = int(
            self._get_env_variable("RECOVERY_ACCESS_TOKEN_EXPIRE_MINUTES")
        )

        self.AWS_REGION_NAME = self._get_env_variable("AWS_REGION")
        self.AWS_ACCESS_KEY_ID = self._get_env_variable("AWS_ACCESS_KEY_ID")
        self.AWS_SECRET_ACCESS_KEY = self._get_env_variable("AWS_SECRET_ACCESS_KEY")
        self.AWS_BUCKET_NAME = self._get_env_variable("AWS_BUCKET_NAME")
        self.FRONTEND_URL = self._get_env_variable("FRONTEND_URL")
        if self.env == "development":
            self.database_url = self._get_env_variable("DATABASE_URL_DEV")
        elif self.env == "testing":
            self.database_url = self._get_env_variable("DATABASE_URL_TEST")
        elif self.env == "production":
            self.database_url = self._get_env_variable("DATABASE_URL_PROD")
        else:
            raise ValueError(f"Unsupported environment: {self.env}")

    def _get_env_variable(self, variable_name: str):
        value = os.getenv(variable_name)
        if value is None:
            raise ValueError(f"Environment variable {variable_name} not set.")
        return value


config = Config()
