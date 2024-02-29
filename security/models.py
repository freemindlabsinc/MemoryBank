from pydantic import BaseModel

# These classes were inspired by the FastAPI documentation 
# at https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str

