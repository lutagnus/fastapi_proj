from sqlalchemy import select
from database import EventOrm, new_session
from schemas import Event, STask

class TaskRepository:
   @classmethod
   async def add_task(cls, task: Event):
       async with new_session() as session:
           data = task.model_dump()
           new_task = EventOrm(**data)
           session.add(new_task)
           await session.flush()
           await session.commit()
           return new_task.id

   @classmethod
   async def delete_task(cls, event_id: int):
        async with new_session() as session:
            event = await session.get(EventOrm, event_id)
            await session.delete(event)
            await session.commit()

   @classmethod
   async def get_tasks(cls) -> list[STask]:
       async with new_session() as session:
           query = select(EventOrm)
           result = await session.execute(query)
           task_models = result.scalars().all()
           tasks = [STask.model_validate(task_model) for task_model in task_models]
           return tasks
   
   @staticmethod
   async def update_task(event_id: int, event: Event):
        async with new_session() as session:  
            db_event = await session.get(EventOrm, event_id)
            if db_event:
                db_event.participants = event.participants
                await session.commit()
            else:
                raise ValueError(f"Event with id {event_id} not found") 

   @staticmethod
   async def update_event_details(event_id: int, updated_event: Event):
        async with new_session() as session:
            db_event = await session.get(EventOrm, event_id)
            if db_event:
                db_event.name = updated_event.name
                db_event.date = updated_event.date
                db_event.maxParticipants = updated_event.maxParticipants
                db_event.type = updated_event.type

                await session.commit()
                await session.refresh(db_event)
                return db_event
            else:
                raise ValueError(f"Мероприятие с id {event_id} не найдено")
   
   @staticmethod
   async def get_users():
        return [
           {"id": "1041805457", "name": "Сунгатуллин Адель Рафаэльевич", "groupNumber": "3.4.21", "type": "old"},
           {"id": "100924009", "name": "Корж Вероника Евгеньевна", "groupNumber": "3.3.62", "type": "old"},
           {"id": "285754597", "name": "Землякова Екатерина Андреевна", "groupNumber": "6.6.22", "type": "old"},
           {"id": "458231189", "name": "Ерошенко Арина Кирилловна", "groupNumber": "6.4.22", "type": "old"},
           {"id": "461512390", "name": "Новикова Марина Валерьевна", "groupNumber": "2.4.16", "type": "old"},
           {"id": "508068988", "name": "Дятлова Анна Павловна", "groupNumber": "6.6.11", "type": "old"},
           {"id": "521704177", "name": "Чигряева Светлана Алексеевна", "groupNumber": "2.3.07", "type": "old"},
           {"id": "552177520", "name": "Баранникова Анастасия Вадимовна", "groupNumber": "2.2.09", "type": "old"},
           {"id": "585314188", "name": "Джепбарова Лачын Бегмурадовна", "groupNumber": "1.5.02", "type": "old"},
           {"id": "710726763", "name": "Бабина Анастасия Леонидовна", "groupNumber": "2.2.20", "type": "old"},
           {"id": "834191555", "name": "Буракова Владислава Евгеньевна", "groupNumber": "2.4.10", "type": "old"},
           {"id": "932075637", "name": "Чернова Екатерина Сергеевна", "groupNumber": "2.4.09", "type": "old"},
           {"id": "1056018335", "name": "Музалевская Елизавета Владимировна", "groupNumber": "1.3.08", "type": "old"},
           {"id": "1078335445", "name": "Кнулова Мария Ивановна", "groupNumber": "2.4.10", "type": "old"},
           {"id": "1092981720", "name": "Мищенко Валерия Васильевна", "groupNumber": "3.4.12", "type": "old"},
           {"id": "1242393664", "name": "Сычева Анастасия Ильинична", "groupNumber": "1.4.05", "type": "old"},
           {"id": "1252545267", "name": "Жукова Мария Сергеевна", "groupNumber": "1.4.20", "type": "old"},
           {"id": "1368820272", "name": "Бабарицкая Ольга Анатольевна", "groupNumber": "2.4.15", "type": "old"},
           {"id": "1384600874", "name": "Рыбакова Виктория Валерьевна", "groupNumber": "1.3.15", "type": "old"},
           {"id": "1385237100", "name": "Егорова Полина Сергеевна", "groupNumber": "1.4.20", "type": "old"},
           {"id": "1645783771", "name": "Карунатилаке Асири Аржуна", "groupNumber": "6.6.01", "type": "old"},
           {"id": "1654966824", "name": "Пайо Мисс Фатен", "groupNumber": "6.6.01", "type": "old"},
           {"id": "1905087744", "name": "Бабаева Акменли", "groupNumber": "6.4.52", "type": "old"},
           {"id": "5132531551", "name": "Суровцева Злата Андреевна", "groupNumber": "3.2.61", "type": "old"},
           {"id": "5252024403", "name": "Фофонова Дарья Эдуардовна", "groupNumber": "1.02.16", "type": "old"},
           {"id": "5807891871", "name": "Пулатова Камилла Рустамовна", "groupNumber": "2.4.14", "type": "old"},
        ]
