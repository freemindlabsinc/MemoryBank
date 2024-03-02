from fastapi import APIRouter
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi.responses import RedirectResponse
import gradio as gr
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from security.models import Token, TokenData, User, UserInDB
from security.fake_users import fake_users_db
from security.functions import authenticate_user, create_access_token, get_current_active_user, ACCESS_TOKEN_EXPIRE_MINUTES
                            

auth_router = APIRouter(
    prefix="",
    tags=["auth"],    
    )


@auth_router.get("/logout")
def logout(request: Request):
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    cookies = request.cookies
    for cookie in cookies:
        if cookie.startswith('access-token'):
            response.delete_cookie(cookie)
    print("Logout user!")
    return response


@auth_router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


