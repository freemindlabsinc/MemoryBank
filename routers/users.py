from fastapi import APIRouter
from typing import Annotated
from fastapi import Depends
from security.models import User
from security.functions import Authentication

users_router = APIRouter(
    prefix="/users",
    tags=["users"],
    #dependencies=[Depends(validate_token)],
    )

@users_router.get("/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(Authentication.get_current_active_user)]
):
    return current_user


@users_router.get("/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(Authentication.get_current_active_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]