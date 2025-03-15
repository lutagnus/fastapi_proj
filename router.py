from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from repository import TaskRepository
from schemas import Event, STask, User
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
import os
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

@router.post("/api/events/{event_id}/register", response_model=STask)
async def register_for_event(event_id: int, user_id: str):
    events = await TaskRepository.get_tasks()
    event = next((event for event in events if event.id == event_id), None)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    if user_id in event.participants:
        raise HTTPException(status_code=400, detail="User already registered for this event")
    if len(event.participants) >= event.maxParticipants:
        raise HTTPException(status_code=400, detail="Event is full")
    
    event.participants.append(user_id)
    await TaskRepository.update_task(event_id, event)
    return event

@router.post("/api/events/{event_id}/unregister", response_model=STask)
async def unregister_from_event(event_id: int, user_id: str):
    events = await TaskRepository.get_tasks()
    event = next((event for event in events if event.id == event_id), None)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    if user_id not in event.participants:
        raise HTTPException(status_code=400, detail="User is not registered for this event")
    event.participants.remove(user_id)
    await TaskRepository.update_task(event_id, event)
    return event

@router.get("/api/events/{event_id}/participants", response_model=List[User])
async def get_event_participants(event_id: int):
    events = await TaskRepository.get_tasks()
    event = next((event for event in events if event.id == event_id), None)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    all_users = await TaskRepository.get_users()
    participants = [user for user in all_users if user["id"] in event.participants]
    return participants

@router.put("/api/events/{event_id}/details", response_model=STask)
async def update_event_details(event_id: int, updated_event: Event):
    try:
        event = await TaskRepository.update_event_details(event_id, updated_event)
        return event
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

#new
class DataModel(BaseModel):
    name: str
    age: int
    email: str

# Функция для записи данных в Excel
def write_to_excel(data: dict):
    # Если файл уже существует, загружаем его
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
    else:
        df = pd.DataFrame()

    # Добавляем новые данные
    new_row = pd.DataFrame([data])
    df = pd.concat([df, new_row], ignore_index=True)

    # Сохраняем данные в Excel
    df.to_excel(EXCEL_FILE, index=False)

@router.post("/api/data")
async def receive_data(data: DataModel):
    # Преобразуем данные в словарь
    data_dict = data.dict()

    # Записываем данные в Excel
    write_to_excel(data_dict)

    # Возвращаем ответ
    return {"status": "success", "message": "Data saved successfully"}

# Подключение роутера к основному приложению
app.include_router(router)
