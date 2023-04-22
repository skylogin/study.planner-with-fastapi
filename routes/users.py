from fastapi import APIRouter, Depends, HTTPException, status
from models.users import User, UserSignIn
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

@user_router.post("/signin")
async def sign_user_in(user: UserSignIn, session=Depends(get_session)) -> dict:
    userInfo = session.get(User, user.email)

    isSamePassword = hash_password.verify_hash(user.password, userInfo.password)

    if user.email != userInfo.email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )
    if isSamePassword != True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Wrong credentials passed"
        )
    
    return {
        "message": "User signed in successfully."
    }