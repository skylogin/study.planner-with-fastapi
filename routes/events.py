from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import select
from database.connection import get_session
from models.events import Event, EventUpdate
from typing import List
from auth.authenticate import authenticate


event_router = APIRouter(
    tags=["Events"]
)

@event_router.get("/", response_model=List[Event])
async def retrieve_all_events(session=Depends(get_session)) -> List[Event]:
    statement = select(Event)
    events = session.exec(statement).all()
    return events

@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: int, session=Depends(get_session)) -> Event:
    event = session.get(Event, id)
    if event:
        return event
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID deos not exist"
    )
    
@event_router.post("/new")
async def create_event(new_event: Event, user: str = Depends(authenticate), session=Depends(get_session)) -> dict:
    new_event.creator = user

    session.add(new_event)
    session.commit()
    session.refresh(new_event)

    return {
        "message": "Event created successfully"
    }

@event_router.put("/edit/{id}", response_model=Event)
async def update_event(id: int, new_data: EventUpdate, user: str = Depends(authenticate), session=Depends(get_session)) -> Event:
    event = session.get(Event, id)

    if event.creator != user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Operation not allowed"
        )

    if event:
        event_data = new_data.dict(exclude_unset=True)
        for key, value in event_data.items():
            setattr(event, key, value)
        session.add(event)
        session.commit()
        session.refresh(event)

        return event

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )


@event_router.delete("/{id}")
async def delete_event(id: int, user: str = Depends(authenticate), session=Depends(get_session)) -> dict:
    event = session.get(Event, id)

    if event.creator != user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Operation not allowed"
        )

    if event:
        session.delete(event)
        session.commit()
        return {
            "message": "Event deleted successfully."
        }
        
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )