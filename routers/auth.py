from fastapi import APIRouter
from datetime import timedelta
from typing import Annotated
from fastapi.responses import RedirectResponse
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import  OAuth2PasswordRequestForm
from security.models import Token
from security.functions import Authentication, ACCESS_TOKEN_EXPIRE_MINUTES
                            

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
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth: Annotated[Authentication, Depends(Authentication)]
) -> Token:
    user = auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


