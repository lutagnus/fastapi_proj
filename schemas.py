from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class Event(BaseModel):
    name: str
    date: datetime
    maxParticipants: int
    type: str
    participants: Optional[List[str]] = None

class User(BaseModel):
    id: str
    name: str
    groupNumber: str
    type: str

class STask(Event):
    id: int
    model_config = ConfigDict(from_attributes=True)


class STaskId(BaseModel):
    ok: bool = True
    event_id: int

