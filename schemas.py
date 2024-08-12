from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class Event(BaseModel):
    name: str
    date: datetime
    max_participants: int
    for_who: str


class STask(Event):
    id: int
    model_config = ConfigDict(from_attributes=True)


class STaskId(BaseModel):
    ok: bool = True
    event_id: int