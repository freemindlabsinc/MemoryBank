from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from security.models import TokenData, User, UserInDB
from security.fake_users import fake_users_db

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Authentication(object):
    # TODO: Replace this with a real database
    fake_db = fake_users_db
    # TODO: Read these from config
    secret_key = SECRET_KEY
    algorithm = ALGORITHM
    # TODO: make these optional    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")    
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
    
    @staticmethod    
    def _verify_password(plain_password, hashed_password):
        return Authentication.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def _get_password_hash(password):
        return Authentication.pwd_context.hash(password)

    @staticmethod
    def get_user(username: str) -> UserInDB | None:
        if username in Authentication.fake_db:
            user_dict = Authentication.fake_db[username]
            return UserInDB(**user_dict)

    @staticmethod
    def authenticate_user(username: str, password: str) -> UserInDB | bool:
        user = Authentication.get_user(username)
        if not user:
            return False
        if not Authentication._verify_password(password, user.hashed_password):
            return False
        return user

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        user = Authentication.get_user(username=token_data.username)
        if user is None:
            raise credentials_exception
        return user

    @staticmethod
    def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)]
    ):
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user
