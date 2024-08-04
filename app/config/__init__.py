import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self):
        self.env = self._get_env_variable("ENV")
        self.SECRET_KEY = self._get_env_variable("SECRET_KEY")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(
            self._get_env_variable("ACCESS_TOKEN_EXPIRE_MINUTES")
        )
        self.REFRESH_KEY = self._get_env_variable("REFRESH_KEY")
        self.REFRESH_TOKEN_EXPIRE_MINUTES = int(
            self._get_env_variable("REFRESH_TOKEN_EXPIRE_MINUTES")
        )
        self.RECOVERY_KEY = self._get_env_variable("RECOVERY_KEY")
        self.RECOVERY_TOKEN_EXPIRE_MINUTES = int(
            self._get_env_variable("RECOVERY_TOKEN_EXPIRE_MINUTES")
        )
        
        if self.env == "dev":
            self.database_url = self._get_env_variable("DATABASE_URL_DEV")
            self.IS_PRODUCTION = False
        elif self.env == "test":
            self.database_url = self._get_env_variable("DATABASE_URL_TEST")
            self.IS_PRODUCTION = True
        elif self.env == "prod":
            self.database_url = self._get_env_variable("DATABASE_URL_PROD")
            self.IS_PRODUCTION = True
        else:
            raise ValueError(f"Unsupported environment: {self.env}")

    def _get_env_variable(self, variable_name: str):
        value = os.getenv(variable_name)
        if value is None:
            raise ValueError(f"Environment variable {variable_name} not set.")
        return value


config = Config()
