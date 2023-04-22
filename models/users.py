from pydantic import BaseModel, EmailStr
from typing import Optional, List
from models.events import Event
from sqlmodel import Field, SQLModel, JSON, Column

class User(SQLModel, table=True):
    email: EmailStr = Field(default=None, primary_key=True)
    password: str
    events: Optional[List[Event]] = Field(sa_column=Column(JSON))

    class Config:
      arbitrary_types_allowed = True
      schema_extra = {
         "example": {
           "email": "fastapi@packt.com",
           "username": "strong!!!",
           "events": [], 
         }
      }

class UserSignIn(SQLModel):
  email: EmailStr
  password: str

  class Config:
    schema_extra = {
      "example": {
        "email": "fastapi@packt.com",
        "username": "strong!!!",
        "events": [], 
      }
    }