from datetime import datetime
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import JSON

#подключение к бд
engine = create_async_engine("sqlite+aiosqlite:///events.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)

class Model(DeclarativeBase):
    pass

#определение таблицы
class EventOrm(Model):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    date: Mapped[datetime]
    max_participants: Mapped[int]
    type: Mapped[str]
    participants: Mapped[list[str]] = mapped_column(JSON, default=[])

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
