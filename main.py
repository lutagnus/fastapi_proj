from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
from typing import List
from contextlib import asynccontextmanager
from database import create_tables, delete_tables
from router import router


@asynccontextmanager
async def lifespan(app: FastAPI):
   await create_tables()
   print("База готова")
   yield
   await delete_tables()
   print("База очищена")

app = FastAPI(lifespan=lifespan)

app.include_router(router)
