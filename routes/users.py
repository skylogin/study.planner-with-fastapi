from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from auth.jwt_handler import create_access_token
from models.users import User, TokenResponse
from sqlmodel import select
from database.connection import get_session
from typing import List

from auth.hash_password import HashPassword


user_router = APIRouter(
    tags=["User"],
)
hash_password = HashPassword()

@user_router.post("/signup")
async def sign_new_user(new_user: User, session=Depends(get_session)) -> dict:
    user = session.get(User, new_user.email)
    if user:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail="User with supplied username exists"
        )
    
    hashed_password = hash_password.create_hash(new_user.password)
    new_user.password = hashed_password

    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {
        "message": "User successfully registered!"
    }

@user_router.post("/signin", response_model=TokenResponse)
async def sign_user_in(user: OAuth2PasswordRequestForm = Depends(), session=Depends(get_session)) -> dict:
    userInfo = session.get(User, user.username)

    if userInfo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )
    
    if hash_password.verify_hash(user.password, userInfo.password):
        access_token = create_access_token(userInfo.email)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Wrong credentials passed"
    )
    