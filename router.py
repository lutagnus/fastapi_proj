from fastapi import FastAPI, HTTPException, Path, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from repository import TaskRepository
from schemas import Event, STask
from fastapi import APIRouter, HTTPException

# Инициализация FastAPI приложения
app = FastAPI()


# Инициализация роутера
router = APIRouter(
    tags=["Мероприятия"],
)

@router.post("/api/events/", response_model=STask)
async def create_event(event: Event):
    event_id = await TaskRepository.add_task(event)
    return {**event.dict(), "id": event_id}

@router.get("/api/events/", response_model=List[STask])
async def get_events():
    return await TaskRepository.get_tasks()

@router.get("/api/events/{event_id}", response_model=STask)
async def get_event(event_id: int):
    events = await TaskRepository.get_tasks()
    event = next((event for event in events if event.id == event_id), None)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.delete("/api/events/{event_id}", response_model=STask)
async def delete_event(event_id: int):
    events = await TaskRepository.get_tasks()
    event = next((event for event in events if event.id == event_id), None)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    await TaskRepository.delete_task(event_id)
    return event

@app.post("/api/events/{event_id}/register")
async def register_for_event(event_id: int, request: Request):
    # Получаем данные из тела запроса
    request_data = await request.json()
    user_id = request_data.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    event = await TaskRepository.get_tasks()  
    event = next((e for e in event if e.id == event_id), None)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if len(event.participants) >= event.max_participants:
        raise HTTPException(status_code=400, detail="Event is full")
    if user_id in event.participants:
        raise HTTPException(status_code=400, detail="User is already registered")
    event.participants.append(user_id)
    await TaskRepository.update_task(event_id, Event(**event.dict()))
    return event


# Подключение роутера к основному приложению
app.include_router(router)
