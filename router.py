from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from repository import TaskRepository
from schemas import Event, STask, User, DataModel
from fastapi import APIRouter, HTTPException
import pandas as pd
import os
import requests
import gspread
from google.oauth2.service_account import Credentials
# ----------------------------------
import pickle
import numpy as np
from pydantic import BaseModel

# Авторизация для Google Sheets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("cred.json", scopes=SCOPES)
client = gspread.authorize(creds)

# Идентификатор таблицы и листа
SPREADSHEET_ID = "1Oj0Y_C_Kybib47WrYHySIBPMhlyzdfUd-r1cJdJjJuA"
SHEET_NAME = "list"
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

# В router.py изменим проверку при регистрации
@router.post("/api/events/{event_id}/register", response_model=STask)
async def register_for_event(event_id: int, user_id: str):
    events = await TaskRepository.get_tasks()
    event = next((event for event in events if event.id == event_id), None)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.is_registration_closed:
        raise HTTPException(status_code=400, detail="Registration is closed for this event")
    if user_id in event.participants:
        raise HTTPException(status_code=400, detail="User already registered for this event")
    if len(event.participants) >= event.maxParticipants:
        raise HTTPException(status_code=400, detail="Event is full")
    
    # Получаем данные пользователя
    
    
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

@router.post("/api/events/{event_id}/close-registration", response_model=STask)
async def close_registration(event_id: int):
    events = await TaskRepository.get_tasks()
    event = next((event for event in events if event.id == event_id), None)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    event.is_registration_closed = True  # Закрываем регистрацию
    await TaskRepository.update_task(event_id, event)
    return event

@router.post("/api/events/{event_id}/open-registration", response_model=STask)
async def open_registration(event_id: int):
    events = await TaskRepository.get_tasks()
    event = next((event for event in events if event.id == event_id), None)
    if event is None:
        raise HTTPException(status_code=404, detail="Мероприятие не найдено")
    
    event.is_registration_closed = False  # Открываем регистрацию
    await TaskRepository.update_task(event_id, event)
    return event

#new
def update_google_sheet(event: Event):
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
    id_to_fio = {
            "1041805457": "Сунгатуллин Адель Рафаэльевич"
    }
    search_date = event.date.strftime('%d.%m.%y')
        # Получаем данные из таблицы
    all_values = sheet.get_all_values()
    # Находим столбец с датой
    date_row = all_values[2]  # Строка 3 (нумерация с 0)
    date_indexes = [i for i, value in enumerate(date_row) if value.strip() == event.date.strftime('%d.%m.%y')]

    #if not date_indexes:
     #   raise HTTPException(status_code=404, detail="Дата не найдена")

    # Находим участников в столбце A
    participant_rows = {row[0]: idx for idx, row in enumerate(all_values)}
    requests = []
    updates = []
    date_row = all_values[2]  # Строка с датами
    date_cols = []
    for i in range(0, len(date_row), 2):
        if date_row[i].strip() == search_date:
            date_cols.extend([i, i+1]) 
    for participant_id in event.participants:
            # Получаем ФИО по ID участника
        participant_fio = id_to_fio.get(participant_id)
        if not participant_fio or participant_fio not in participant_rows:
            continue
                
        row_idx = participant_rows[participant_fio]
            
        for col_idx in date_cols:
                # Для первой колонки - чекбокс
            if date_cols.index(col_idx) % 2 == 0:
                requests.append({
                    'setDataValidation': {
                        'range': {
                            'sheetId': sheet.id,
                            'startRowIndex': row_idx,
                            'endRowIndex': row_idx+1,
                            'startColumnIndex': col_idx,
                            'endColumnIndex': col_idx+1
                            },
                            'rule': {
                                'condition': {
                                    'type': 'BOOLEAN'
                                }
                            }
                        }
                    })
                updates.append({
                    'range': f"{gspread.utils.rowcol_to_a1(row_idx+1, col_idx+1)}",
                    'values': [[True]]
                    })
                # Для второй колонки - отметка о присутствии
            else:
                updates.append({
                        'range': f"{gspread.utils.rowcol_to_a1(row_idx+1, col_idx+1)}",
                        'values': [[True]]
                    })

        # Выполняем обновления
    if requests:
        sheet.spreadsheet.batch_update({'requests': requests})
        
    if updates:
            # Группируем обновления по 10 для избежания лимитов API
        for i in range(0, len(updates), 10):
            batch = updates[i:i+10]
            sheet.batch_update(batch)


    return {"message": "Обновление завершено.",
           "name": event.name,
                "date": event.date.strftime('%Y-%m-%d'),
                "maxParticipants": event.maxParticipants,
                "type": event.type,
                "id": event.id,
                "participants": event.participants}

@router.post("/api/events/update_google", response_model=STask)
async def update_event(event_id: int):
    events = await TaskRepository.get_tasks()  # Получаем список всех событий
    event = next((event for event in events if event.id == event_id), None)  # Ищем нужное

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    try:
        result = update_google_sheet(event)  # Обновляем Google-таблицу
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot7822968867:AAHYneM1jRfOlYHlDsnFgwUiyzvbmLAY0nY/sendMessage"
    payload = {
        "chat_id": -4678833750,
        "text": message
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        raise Exception(f"Ошибка отправки сообщения в Telegram: {response.text}")

@router.get("/api/data/")
async def receive_data(
    trader_id: str = Query(..., description="ID трейдера"),  # Обязательный параметр
    reg: str = Query(..., description="reg")             # Обязательный параметр
                 # Обязательный параметр
):
    try:
        # Формируем сообщение для Telegram
        message = (f"Игрок: {trader_id} Зарегистрировался {reg} "
        )

        # Отправляем сообщение в Telegram
        send_telegram_message(message)

        return {"status": "success", "message": "Data sent to Telegram successfully"}
    except Exception as e:
        # Отправляем сообщение об ошибке в Telegram
        send_telegram_message(f"Ошибка: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/dep/")
async def receive_data(
     trader_id: str = Query(..., description="ID трейдера"),
    ftd: str = Query(..., description="ftd"),             # Обязательный параметр
    dep: str = Query(..., description="dep"),
    sumdep: str = Query(..., description="sumdep") 
):
    try:
        # Формируем сообщение для Telegram
        message = (f"Игрок: {trader_id} Внес первый депозит {ftd} Внес депозит {dep}. Сумма: {sumdep}"
        )

        # Отправляем сообщение в Telegram
        send_telegram_message(message)

        return {"status": "success", "message": "Data sent to Telegram successfully"}
    except Exception as e:
        # Отправляем сообщение об ошибке в Telegram
        send_telegram_message(f"Ошибка: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


#-----------------------------------------
class KidneyInput(BaseModel):
    age: float
    blood_pressure: float
    specific_gravity: float
    albumin: float
    urea: float
    sodium: float
    sugar: float = 0
    potassium: float = 0
    hemoglobin: float = 0
    creatinine: float = None

class KidneyResult(BaseModel):
    creatinine_level: float
    ckd_probability: float
    risk_class: str
    recommendations: str

# Добавьте где-то в начале (после авторизации Google Sheets)
# Загрузка модели (укажите правильный путь к вашему .pkl файлу)
#try:
 #   with open('kidney_model.pkl', 'rb') as f:
  #      kidney_model = pickle.load(f)
#except Exception as e:
 #   print(f"Error loading kidney model: {e}")
  #  kidney_model = None


@router.post("/api/events/calculate-kidney", response_model=KidneyResult)
async def calculate_kidney(data: KidneyInput):
    try:
        # 1. Расчет креатинина (ваша формула)
        if data.creatinine is None:
            creatinine = 18.8995 + \
                0.0011 * data.age + \
                0.0045 * data.blood_pressure + \
                (-16.9356) * data.specific_gravity + \
                0.0845 * data.albumin + \
                0.0058 * data.sugar + \
                0.0064 * data.urea + \
                (-0.0095) * data.sodium + \
                0.017 * data.potassium + \
                (-0.0169) * data.hemoglobin
        else:
            creatinine = data.creatinine
        with open('kidney_model.pkl', 'rb') as f:
            kidney_model = pickle.load(f)
        # 2. Расчет вероятности ХПН с помощью модели
        if kidney_model is None:
            raise HTTPException(status_code=500, detail="Kidney model not loaded")
        
        # Подготовка данных для модели (должно соответствовать формату, на котором обучалась модель)
        input_data = np.array([
            data.age,
            data.blood_pressure,
            data.specific_gravity,
            data.albumin,
            data.urea,
            data.sodium,
            data.sugar,
            data.potassium,
            data.hemoglobin,
            creatinine
        ]).reshape(1, -1)
        
        # Получение вероятности
        probability = kidney_model.predict_proba(input_data)[0][1] * 100  # Вероятность класса 1 (ХПН)
        probability = round(probability, 1)
        
        # Определение класса риска
        if probability < 30:
            risk_class = "Низкий"
            recommendations = "Риск ХПН низкий. Рекомендуется контроль показателей через 6-12 месяцев."
        elif probability < 60:
            risk_class = "Средний"
            recommendations = "Умеренный риск ХПН. Рекомендуется консультация нефролога."
        else:
            risk_class = "Высокий"
            recommendations = "Высокий риск ХПН. Необходима срочная консультация специалиста."
        
        return {
            "creatinine_level": round(creatinine, 2),
            "ckd_probability": probability,
            "risk_class": risk_class,
            "recommendations": recommendations
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Подключение роутера к основному приложению
app.include_router(router)
