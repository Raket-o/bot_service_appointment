"""Модуль моделей с баз данных."""
import datetime

from sqlalchemy import Column, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, backref
from sqlalchemy.types import Boolean, Date, Integer, Text, String

from sqlalchemy import Column, String, Integer
from database.connect import Base, engine, session


class UserInfo(Base):
    """Класс UserInfo. Является моделью таблицы user_info"""

    __tablename__ = "user_info"
    __table_args__ = {'extend_existing': True}

    telegramm_id = Column(Integer, nullable=False, primary_key=True)
    full_name = Column(String(50), nullable=False)
    telephone = Column(String(20), nullable=True)
    blocked = Column(Boolean)
    last_visit_date = Column(String(50), nullable=True)
    record = relationship("RecordDate", cascade="all,delete", backref=backref('telegramm_id', passive_deletes=True), lazy="select")


class RecordDate(Base):
    """Класс RecordDate. Является моделью таблицы record_dates"""
    __tablename__ = "record_dates"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, ForeignKey('user_info.telegramm_id', ondelete='CASCADE'), nullable=False)
    record_date = Column(String(50), nullable=False)
    hour = Column(Integer, nullable=False)
