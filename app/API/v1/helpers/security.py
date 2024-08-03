from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
from ..constans.security import ALGORITHM, SECRET_KEY, REFRESH_KEY, RECOVERY_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES, RECOVERY_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")





def create_access_token(subject: Union[str, Any]) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any]) -> str:
    expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, REFRESH_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_recovery_token(subject: Union[str, Any]) -> str:
    expire = datetime.utcnow() + timedelta(minutes=RECOVERY_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, RECOVERY_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def decodeJWT(token: str) -> dict:
    try:
        
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        
        return (
            decoded_token
            if decoded_token["exp"] >= datetime.utcnow().timestamp()
            else None
        )
    except Exception as e:
        print(e)
        return {}


def decodeRefreshJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, REFRESH_KEY, algorithms=ALGORITHM)
        return (
            decoded_token
            if decoded_token["exp"] >= datetime.utcnow().timestamp()
            else None
        )
    except Exception as e:
        print(e)
        return {}


def decodeRecoverJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, RECOVERY_KEY, algorithms=ALGORITHM)
        return (
            decoded_token
            if decoded_token["exp"] >= datetime.utcnow().timestamp()
            else None
        )
    except Exception as e:
        print(e)
        return {}
