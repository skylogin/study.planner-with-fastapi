from httpx import AsyncClient
import pytest
from main import app

@pytest.mark.asyncio
async def test_sign_new_user() -> None:
    payload = {
        "email": "testuseergddr123@test.com",
        "password": "testpassword"
    }

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    test_response = {
        "message": "User successfully registered!"
    }

    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
      response = await ac.post("/user/signup", json=payload, headers=headers)
      assert response.status_code == 200
      assert response.json() == test_response



@pytest.mark.asyncio
async def test_sign_user_in() -> None:
  payload = {
    "username": "fastapi@packt.com",
    "password": "Str@ng!"
  }

  headers = {
    "accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded"
  }

  async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
      response = await ac.post("/user/signin", data=payload, headers=headers)
      assert response.status_code == 200
      assert response.json()["token_type"] == "Bearer"
