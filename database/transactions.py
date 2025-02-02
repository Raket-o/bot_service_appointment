"""Модуль работы с базой данных."""
import datetime
from typing import Any

from sqlalchemy import func, select, text

from database.connect import Base, engine, session
from database.models import RecordDate, UserInfo


async def init_db() -> None:
    """Функция init_db. При отсутствии базы донных создаёт их."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def deleting_records_older_7_days() -> None:
    """Функция deleting_records_older_7_days. Удаляет записи старее 7 дней."""
    sql = text(
        """
        DELETE FROM record_dates WHERE record_date < datetime('now', '-7 days')
        """
    )
    await session.execute(sql)
    await session.commit()


async def deletes_old_users() -> None:
    """Функция deletes_old_users. Удаляет пользователей, которые не заходили полгода."""
    sql = text(
        """
        DELETE FROM user_info WHERE last_visit_date < datetime('now', '-6 month')
        """
    )
    await session.execute(sql)
    await session.commit()


async def user_check(telegram_id: int) -> tuple[Any]:
    """Функция user_check. Проверяет создан ли пользователь и возвращает статус его блокировки."""
    res = await session.execute(select(UserInfo.blocked).where(UserInfo.telegramm_id == telegram_id))
    return res.one_or_none()


async def add_user(telegram_id: int, full_name: str) -> None:
    """Функция add_user. Добавляет нового пользователя."""
    user = UserInfo(
        telegramm_id=telegram_id,
        full_name=full_name,
    )
    session.add(user)
    await session.commit()


async def update_visit_date(telegram_id: int) -> None:
    """Функция update_visit_date. Обновляет время посещения пользователя."""
    user = await session.execute(select(UserInfo).where(UserInfo.telegramm_id == telegram_id))
    user = user.scalar()
    user.last_visit_date = datetime.datetime.now()
    await session.commit()


async def count_date_rec(telegram_id: int) -> int:
    """Функция count_date_rec. Возвращает количество записей пользователя."""
    res = await session.execute(select(func.count()).where(RecordDate.telegram_id == telegram_id))
    return res.one_or_none()


async def get_date_time_appointment(date: datetime) -> list[Any]:
    """Функция get_date_time_appointment. Возвращает дату и время записи пользователя."""
    # date = datetime_trans_str(date)
    res = await session.execute(select(RecordDate.hour, RecordDate.telegram_id).where(RecordDate.record_date == date))
    return res.all()


async def check_date_time_appointment(date: datetime, hour: int) -> list[Any]:
    """Функция check_date_time_appointment. Проверяет занята дата и время записи."""
    res = await (session.execute(
        select(RecordDate.hour, UserInfo.telegramm_id).join(UserInfo, UserInfo.telegramm_id == RecordDate.telegram_id)
        .where(RecordDate.record_date == date, RecordDate.hour == hour)))
    return res.all()


async def set_date_time_appointment(contact, date: datetime, hour: int) -> None:
    """Функция set_date_time_appointment. Обновляет номер телефона пользователя
    и записает на его на приём."""
    phone_number = contact.phone_number
    telegram_id = contact.user_id

    res = await user_check(telegram_id)
    if res:
        user = await session.execute(select(UserInfo).where(UserInfo.telegramm_id == telegram_id))
        user = user.scalar()
        user.telephone = phone_number
    else:
        full_name = [contact.last_name if contact.last_name else "", contact.first_name if contact.first_name else ""]
        full_name = " ".join(full_name)
        await add_user(telegram_id, full_name)

    record = RecordDate(
        telegram_id=telegram_id,
        record_date=date,
        hour=hour
    )

    session.add(record)
    await session.commit()


async def del_record(date: datetime, hour: int) -> None:
    """Функция del_record. Удаляет запись."""
    record = await session.execute(select(RecordDate).where(RecordDate.record_date == date, RecordDate.hour == hour))
    record = record.scalar()

    if record:
        await session.delete(record)
    await session.commit()


async def del_record_all_day(date: datetime) -> None:
    """Функция del_record. Удаляет все записи на день."""
    res = await session.execute(select(RecordDate).where(RecordDate.record_date == date))
    res = res.all()

    if res:
        for obj in res:
            await session.delete(obj[0])
    await session.commit()


async def view_clients() -> list[Any]:
    """Функция view_clients. Возвращает всех клиентов."""
    res = await session.execute(select(UserInfo))
    return res.all()


async def view_record(telegram_id: int) -> list[Any]:
    """Функция view_record. Возвращает все записи пользователя."""
    res = await session.execute(
        select(RecordDate.record_date, RecordDate.hour).where(RecordDate.telegram_id == telegram_id).order_by(
            RecordDate.record_date, RecordDate.hour))
    return res.all()


async def block_unblock_user(telegram_id: int, action: str) -> None:
    """Функция block_unblock_user. Блокирует и разблокирует пользователя."""
    user = await session.execute(select(UserInfo).where(UserInfo.telegramm_id == telegram_id))
    user = user.scalar()
    user.blocked = 1 if action == "bl" else 0
    await session.commit()


async def del_user(telegram_id: int) -> None:
    """Функция del_user. Удаляет пользователя."""
    user = await session.execute(select(UserInfo).where(UserInfo.telegramm_id == telegram_id))
    user = user.scalar()
    await session.delete(user)
    await session.commit()


async def search_client(search_text: str) -> list[Any]:
    """Функция search_client. Ищет пользователей по имени и номеру телефона."""
    res = await session.execute(select(UserInfo).where(UserInfo.telephone.ilike(f'%{search_text}%')))
    res = res.all()

    if not res:
        res = await session.execute(select(UserInfo).where(UserInfo.full_name.ilike(f'%{search_text}%')))
        res = res.all()
    return res


async def reserve_day(
        telegram_id: int, date: datetime, beginning_working_day: int, end_working_day: int
) -> None:
    """Функция reserve_day. Резервирует день."""
    records = (
        RecordDate(
            telegram_id=telegram_id,
            record_date=date,
            hour=hour
        )
        for hour in range(beginning_working_day, end_working_day + 1)
    )

    session.add_all(records)
    await session.commit()


async def mailing_for_day(date: datetime) -> list[Any]:
    """Функция mailing_for_day. Возвращает всех пользователя кто записан на день."""
    res = await session.execute(
        select(RecordDate.telegram_id, RecordDate.hour).where(RecordDate.record_date == date).group_by(RecordDate.telegram_id))
    return res.all()


async def viewing_recordings_day_db(date: datetime) -> list[Any]:
    """Функция viewing_recordings_day_db. Возвращает все записи на день."""
    res = await (session.execute(select(UserInfo.full_name, UserInfo.telephone, RecordDate.hour).
                                 join(UserInfo, UserInfo.telegramm_id == RecordDate.telegram_id).
                                 where(RecordDate.record_date == date).order_by(RecordDate.hour)))
    return res.all()


async def get_info_user(date: datetime, hour: int) -> UserInfo:
    """Функция get_info_user. Возвращает ид пользователя."""
    res = await (session.execute(select(RecordDate.telegram_id).
                                 join(UserInfo, UserInfo.telegramm_id == RecordDate.telegram_id).
                                 where(RecordDate.record_date == date, RecordDate.hour == hour)))
    return res.one_or_none()
