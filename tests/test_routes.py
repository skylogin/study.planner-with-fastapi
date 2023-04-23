from httpx import AsyncClient
import pytest

from auth.jwt_handler import create_access_token
from models.events import Event

from main import app

@pytest.fixture(scope="module")
async def access_token() -> str:
    return create_access_token("fastapi@packt.com")

@pytest.fixture(scope="module")
async def mock_event() -> Event:
    new_event = Event(
        creator="fastapi@packt.com",
        title="FastAPI Book Launch",
        image="https://linktomyimage.com/image.png",
        description="We will be discussing the contents of the FastAPI book in this event. Ensure to come with your own copy to win gifts!",
        tags=["python", "fastapi", "book", "launch"],
        location="Google Meet"
    )

    await Event.insert_one(new_event)

    yield new_event

@pytest.mark.asyncio
async def test_get_events(mock_event: Event) -> None:
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
      response = await ac.get("/event/")

      assert response.status_code == 200
      assert response.json()[0]["_id"] == str(mock_event.id)


@pytest.mark.asyncio
async def test_get_event(mock_event: Event) -> None:
    url = f"/event/{str(mock_event.id)}"
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
      response = await ac.get(url)

      assert response.status_code == 200
      assert response.json()["creator"] == mock_event.creator
      assert response.json()[0]["_id"] == str(mock_event.id)

@pytest.mark.asyncio
async def test_post_event(access_token: str) -> None:
   payload = {
        "title": "FastAPI Book Launch",
        "image": "https://linktomyimage.com/image.png",
        "description": "We will be discussing the contents of the FastAPI book in this event. Ensure to come with your own copy to win gifts!",
        "tags": ["python", "fastapi", "book", "launch"],
        "location": "Google Meet"
   }
   
   headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
   }
   test_response = {
        "message": "Event created successfully"
   }

   async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
      response = await ac.post("/event/new", json=payload, headers=headers)
      assert response.status_code == 200
      assert response.json() == test_response
