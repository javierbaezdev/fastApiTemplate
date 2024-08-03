import os
from dotenv import load_dotenv
load_dotenv()


ALGORITHM = "HS256"
ENV_MODE = os.environ.get('ENV')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.environ.get('REFRESH_TOKEN_EXPIRE_MINUTES'))
RECOVERY_TOKEN_EXPIRE_MINUTES = int(os.environ.get('RECOVERY_TOKEN_EXPIRE_MINUTES'))
SECRET_KEY = os.environ.get('SECRET_KEY')
REFRESH_KEY = os.environ.get('REFRESH_KEY')
RECOVERY_KEY = os.environ.get('RECOVERY_KEY')

IS_PRODUCTION = ENV_MODE == 'prod'
IS_DEVELOPMENT = ENV_MODE == 'dev'
IS_TEST = ENV_MODE == 'test'