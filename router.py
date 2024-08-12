from typing import List
from repository import TaskRepository
from fastapi import APIRouter, HTTPException
from schemas import Event, STask

router = APIRouter(
    tags=["Мероприятия"],
)

@router.post("/events/", response_model=STask)
async def create_event(event: Event):
    event_id = await TaskRepository.add_task(event)
    return {**event.dict(), "id": event_id}

@router.get("/events/", response_model=List[STask])
async def get_events():
    return await TaskRepository.get_tasks()

@router.get("/events/{event_id}", response_model=STask)
async def get_event(event_id: int):
    events = await TaskRepository.get_tasks()
    event = next((event for event in events if event.id == event_id), None)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.delete("/events/{event_id}", response_model=STask)
async def delete_event(event_id: int):
    events = await TaskRepository.get_tasks()
    event = next((event for event in events if event.id == event_id), None)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    await TaskRepository.delete_task(event_id)  # Необходимо добавить этот метод в TaskRepository
    return event
