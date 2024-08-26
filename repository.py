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
   async def get_tasks(cls) -> list[STask]:
       async with new_session() as session:
           query = select(EventOrm)
           result = await session.execute(query)
           task_models = result.scalars().all()
           tasks = [STask.model_validate(task_model) for task_model in task_models]
           return tasks
   
   @classmethod
   async def update_task(event_id: int, user_id: str, task: Event):
        async with new_session() as session:  
            db_event = await session.get(EventOrm, event_id)
            if db_event:
                db_event.participants = event.participants
                await session.commit()
            else:
                raise ValueError(f"Event with id {event_id} not found") 
