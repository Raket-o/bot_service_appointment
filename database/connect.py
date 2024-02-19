"""Модуль подключения базы данных."""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


__DATABASE_URL = "sqlite+aiosqlite:///./database/database.db"
engine = create_async_engine(__DATABASE_URL, echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
session = Session()
