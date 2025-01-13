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
           {"id": "508068988", "name": "Дятлова Анна Павловна", "groupNumber": "6.6.11", "type": "new"},
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
           {"id": "961020159", "name": "Рождественский Артем", "groupNumber": "МГУ", "type": "old"},
           {"id": "326736744", "name": "Жупник Виктория Кирилловна", "groupNumber": "2.6.15", "type": "new"},
           {"id": "444736323", "name": "Уланова Ульяна Александровна", "groupNumber": "2.5.16", "type": "new"},
           {"id": "469027781", "name": "Пилясова Анна Дмитриевна", "groupNumber": "2.5.16", "type": "new"},
           {"id": "728152301", "name": "Литко Ангелина Андреевна", "groupNumber": "2.4.10", "type": "new"},
           {"id": "770671077", "name": "Митина Полина Владимировна", "groupNumber": "1.3.10", "type": "new"},
           {"id": "847299130", "name": "Максимова Александра Дмитриевна", "groupNumber": "7.2.03", "type": "new"},
           {"id": "884346012", "name": "Журавлева Арина Александровна", "groupNumber": "3.3.62", "type": "new"},
           {"id": "900922192", "name": "Бусалаева Дарья Игоревна", "groupNumber": "2.6.19", "type": "new"},
           {"id": "917108826", "name": "Мурюкина Анна Игоревна", "groupNumber": "7.3.01", "type": "new"},
           {"id": "1031316250", "name": "Резник Арина Сергеевна", "groupNumber": "3.3.62", "type": "new"},
           {"id": "1098670149", "name": "Арапханова Роза Юнусовна", "groupNumber": "3.2.41", "type": "new"},
           {"id": "1147652789", "name": "Гонопольская Юлия Генадьевна", "groupNumber": "3.4.12", "type": "new"},
           {"id": "1340422814", "name": "Осина Ксения Александровна", "groupNumber": "7.2.03", "type": "new"},
           {"id": "1807184525", "name": "Замотохина Анна Александровна", "groupNumber": "3.3.62", "type": "new"},
           {"id": "1970654106", "name": "Данилова Софья", "groupNumber": "1.2.09", "type": "new"},
           {"id": "1988552515", "name": "Чухин Иван Михайлович", "groupNumber": "3.4.22", "type": "new"},
           {"id": "1994490195", "name": "Болорцэцэг Санчирмаа", "groupNumber": "6.4.54б", "type": "new"},
           {"id": "5305858292", "name": "Мифтиханова Екатерина Сергеевна", "groupNumber": "2.3.01", "type": "new"},
           {"id": "5408738242", "name": "Батхуяг Уянга", "groupNumber": "6.3.54", "type": "new"},
           {"id": "5436104037", "name": "Андреевских Денис Анатольевич", "groupNumber": "7.2.01", "type": "new"},
           {"id": "5648396825", "name": "Турсунов Манучехрджон Мансурджонович", "groupNumber": "6.4.53", "type": "new"},
           {"id": "444063735", "name": "Антонова Екатерина Павловна", "groupNumber": "3.5.21", "type": "new"},
           {"id": "1244440429", "name": "Лазарева Мария Александровна", "groupNumber": "3.5.21", "type": "new"},
           {"id": "716875730", "name": "Анис Марсиа бинти Афанди", "groupNumber": "6.5.01а", "type": "new"},
           {"id": "1002509125", "name": "Дмитриева Полина Сергеевна", "groupNumber": "7.2.01", "type": "new"},
           {"id": "917529729", "name": "Иванова Мария Николаевна", "groupNumber": "3.4.62а", "type": "new"},
           {"id": "6142674297", "name": "Зелинская Алина Максимовна", "groupNumber": "академ", "type": "new"},
           {"id": "1729671336", "name": "Хювенен Майя Валерьевна", "groupNumber": "1.1.21", "type": "new"},
           {"id": "1311648733", "name": "Сидорова Екатерина Сергеевна", "groupNumber": "1.6.08", "type": "new"},
           {"id": "922747237", "name": "Цымбалова Валерия Сергеевна", "groupNumber": "2.2.12", "type": "new"},
           {"id": "714080332", "name": "Яковлева Ангелина Владимировна", "groupNumber": "7.1.02", "type": "new"},
           {"id": "928250354", "name": "Рамазанов Имам Нарудинович", "groupNumber": "4.1.05А", "type": "new"},
           {"id": "1707231120", "name": "Кислицына Анастасия Максимовна", "groupNumber": "1.6.13", "type": "new"},
           {"id": "1802932269", "name": "Стратий Ангелина Андреевна", "groupNumber": "2.6.12б", "type": "new"},
           {"id": "1231842503", "name": "Фролова Анастасия Максимовна", "groupNumber": "3.2.01б", "type": "new"},
           {"id": "1187813043", "name": "Евдокимова Ольга Андреевна", "groupNumber": "Орд.1.18", "type": "new"},
           {"id": "1694026110", "name": "Миша", "groupNumber": "....", "type": "new"},
           {"id": "1186568851", "name": "Жихарева Евгения Александровна", "groupNumber": "2.2.18а", "type": "new"},
           {"id": "1573404642", "name": "Рудова Полина Дмитриевна", "groupNumber": "3.2.01", "type": "new"},
           {"id": "759883589", "name": "Гончарова Валерия Геннадьевна", "groupNumber": "1.3.21", "type": "new"},
           {"id": "801548690", "name": "Филатова Виолетта Андреевна", "groupNumber": "2.1.09", "type": "new"},
           {"id": "991460231", "name": "Кокарева Полина Юрьевна", "groupNumber": "2.1.18", "type": "new"},
           {"id": "733470425", "name": "Тараскина Элона Олеговна", "groupNumber": "1.4.16а", "type": "new"},
           {"id": "1028906973", "name": "Пискунова Ксения Валерьевна", "groupNumber": "3.1.61", "type": "new"},
           {"id": "1246820018", "name": "Ясинецкая Екатерина", "groupNumber": "3.1.71", "type": "new"},
           {"id": "806711079", "name": "Минзакирова Алина Максимовна", "groupNumber": "2.1.20", "type": "new"},
           {"id": "969867709", "name": "Саная Вера Сережаевна", "groupNumber": "1.26", "type": "new"},
           {"id": "5505130124", "name": "Кухаренко Анастасия Павловна", "groupNumber": "7.1.01", "type": "new"},
           {"id": "828257010", "name": "Воеводская Анастасия Александровна", "groupNumber": "7.2.04", "type": "new"},
           {"id": "1168721145", "name": "Химионова Юлия Витальевна", "groupNumber": "1.3.22Б", "type": "new"},
           {"id": "1472079080", "name": "Шишкинская Екатерина Сергеевна", "groupNumber": "4.2.03б", "type": "new"},
        ]
