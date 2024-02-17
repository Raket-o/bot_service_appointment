"""Модуль работы с базой данных."""
import datetime
import sqlite3
from sqlalchemy import func, text
from typing import Any, List, Set

from database.connect import Base, engine, session
from database.models import RecordDate, UserInfo


def init_db() -> None:
    """Функция init_db. При отсутствии базы донных создаёт их."""
    Base.metadata.create_all(engine)


def deleting_records_older_7_days() -> None:
    """Функция deleting_records_older_7_days. Удаляет записи старее 7 дней."""
    sql = text(
        """
        DELETE FROM record_dates WHERE date < datetime('now', '-7 day')
        """
    )
    session.execute(sql)
    session.commit()


def deletes_old_users() -> None:
    """Функция deletes_old_users. Удаляет пользователей, которые не заходили полгода."""
    sql = text(
        """
        DELETE FROM user_info WHERE last_visit_date < datetime('now', '-6 month')
        """
    )
    session.execute(sql)
    session.commit()


def user_check(telegram_id: int) -> list[Any]:
    """Функция user_check. Проверяет создан ли пользователь и возвращает статус его блокировки."""
    res = session.query(UserInfo.blocked).where(UserInfo.telegramm_id == telegram_id).one_or_none()
    return res


def datetime_trans_str(date: datetime) -> str:
    """Функция datetime_trans_str. Переводит из формата datetime в str."""
    return f"{date.year}-{date.month}-{date.day}"


def add_user(telegram_id: int, full_name: str) -> None:
    """Функция add_user. Добавляет нового пользователя."""
    user = UserInfo(
        telegramm_id=telegram_id,
        full_name=full_name,
    )
    session.add(user)
    session.commit()


def update_visit_date(telegram_id: int) -> None:
    """Функция update_visit_date. Обновляет время посещения пользователя."""
    user = session.query(UserInfo).where(UserInfo.telegramm_id == telegram_id).one_or_none()
    user.last_visit_date = datetime.datetime.now()
    session.commit()


def count_date_rec(telegram_id: int) -> int:
    """Функция count_date_rec. Возвращает количество записей пользователя."""
    res = session.query(func.count()).where(RecordDate.telegram_id == telegram_id).one_or_none()
    return res


def get_date_time_appointment(date: datetime) -> list[Any]:
    """Функция get_date_time_appointment. Возвращает дату и время записи пользователя."""
    date = datetime_trans_str(date)
    res = session.query(RecordDate.hour, RecordDate.telegram_id).where(RecordDate.date == date).all()
    return res


def check_date_time_appointment(date: datetime) -> list[Any]:
    """Функция check_date_time_appointment. Проверяет занята дата и время записи."""
    date_execute = datetime_trans_str(date)
    res = (session.query(RecordDate.hour, UserInfo.telegramm_id).join(UserInfo, UserInfo.telegramm_id == RecordDate.telegram_id)
           .where(RecordDate.date == date_execute)).where(RecordDate.hour == date.hour).all()

    return res


def set_date_time_appointment(contact, date: datetime) -> None:
    """Функция set_date_time_appointment. Обновляет номер телефона пользователя
    и записает на его на приём."""
    phone_number = contact.phone_number
    telegram_id = contact.user_id
    date_db = datetime_trans_str(date)

    user = session.query(UserInfo).where(UserInfo.telegramm_id == telegram_id).one_or_none()
    user.telephone = phone_number

    record = RecordDate(
        telegram_id = telegram_id,
        date = date_db,
        hour = int(date.hour)
    )

    session.add(record)
    session.commit()


def view_record(telegram_id: int) -> list[Any]:
    """Функция view_record. Возвращает все записи пользователя."""
    res = session.query(RecordDate.date, RecordDate.hour).where(RecordDate.telegram_id == telegram_id).all()
    return res


def del_record(date: str, hour: int) -> None:
    """Функция del_record. Удаляет запись."""
    record = session.query(RecordDate).where(RecordDate.date == date).where(RecordDate.hour == hour).one_or_none()

    if record:
        session.delete(record)
        session.commit()


def view_clients() -> list[Any]:
    """Функция view_clients. Возвращает всех клиентов."""
    res = session.query(UserInfo).all()
    return res


def view_client_records(telegram_id: int) -> list[Any]:
    """Функция view_client_records. Возвращает все записи пользователя."""
    res = session.query(RecordDate.date, RecordDate.hour).where(RecordDate.telegram_id == telegram_id).all()
    return res


def block_unblock_user(telegram_id: int, action: str) -> None:
    """Функция block_unblock_user. Блокирует и разблокирует пользователя."""
    user = session.query(UserInfo).where(UserInfo.telegramm_id == telegram_id).one_or_none()
    user.blocked = 1 if action == "bl" else 0
    session.commit()


def del_user(telegram_id: int) -> None:
    """Функция del_user. Удаляет пользователя."""
    user = session.query(UserInfo).where(UserInfo.telegramm_id == telegram_id).one_or_none()
    session.delete(user)
    session.commit()


def search_client(search_text: str) -> list[Any]:
    """Функция search_client. Ищет пользователей по имени и номеру телефона."""
    res = session.query(UserInfo).filter(UserInfo.telephone.ilike(f'%{search_text}%')).all()
    if not res:
        res = session.query(UserInfo).filter(UserInfo.full_name.ilike(f'%{search_text}%' or UserInfo.telephone.ilike(f'%{search_text}%'))).all()
    return res


def reserve_day(
    telegram_id: int, date: datetime, beginning_working_day: int, end_working_day: int
) -> None:
    """Функция reserve_day. Резервирует день."""
    records = []
    for hour in range(beginning_working_day, end_working_day + 1):
        record = RecordDate(
            telegram_id=telegram_id,
            date = date,
            hour = hour
        )
        records.append(record)

    session.bulk_save_objects(records)
    session.commit()


def mailing_for_day(date: str) -> list[Any]:
    """Функция mailing_for_day. Возвращает всех пользователя кто записан на день."""
    res = session.query(RecordDate.telegram_id).where(RecordDate.date == date).group_by(RecordDate.telegram_id).all()
    return res


def viewing_recordings_day_db(date: datetime) -> list[Any]:
    """Функция viewing_recordings_day_db. Возвращает все записи на день."""
    date = datetime_trans_str(date)
    res = (session.query(UserInfo.full_name, UserInfo.telephone, RecordDate.hour).
           join(UserInfo, UserInfo.telegramm_id==RecordDate.telegram_id).
           where(RecordDate.date == date).all())
    return res
