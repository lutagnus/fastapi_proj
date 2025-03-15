from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from repository import TaskRepository
from schemas import Event, STask, User, DataModel
from fastapi import APIRouter, HTTPException
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


def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot7822968867:AAHYneM1jRfOlYHlDsnFgwUiyzvbmLAY0nY/sendMessage"
    payload = {
        "chat_id": -4678833750,
        "text": message
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        raise Exception(f"Ошибка отправки сообщения в Telegram: {response.text}")

@app.post("/api/data")
async def receive_data(data: DataModel):
    try:
        # Формируем сообщение для Telegram
        message = (
            "Новые данные получены:\n"
            f"Имя: {data.name}\n"
            f"Возраст: {data.age}\n"
            f"Email: {data.email}"
        )

        # Отправляем сообщение в Telegram
        send_telegram_message(message)

        return {"status": "success", "message": "Data sent to Telegram successfully"}
    except Exception as e:
        # Отправляем сообщение об ошибке в Telegram
        send_telegram_message(f"Ошибка: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Подключение роутера к основному приложению
app.include_router(router)
