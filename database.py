from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Укажите строку подключения к вашей базе данных
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/fsrnrmu"

# Создайте движок
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Создайте сессию
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()
