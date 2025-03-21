from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class Event(BaseModel):
    name: str
    date: datetime
    maxParticipants: int
    type: str
    participants: Optional[List[str]] = None
    is_registration_closed: bool = False

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


#new
class DataModel(BaseModel):
    name: str
    age: int
    email: str
