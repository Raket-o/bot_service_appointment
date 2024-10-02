"""Модуль подключения базы данных."""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

__DATABASE_URL = "sqlite+aiosqlite:///./database/database.db"
engine = create_async_engine(__DATABASE_URL, echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
session = Session()
