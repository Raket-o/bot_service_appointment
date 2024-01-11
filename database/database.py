"""Модуль работы с базой данных."""
import datetime
import sqlite3
from typing import Any, List, Set

PATH_DB = "database/database.db"


def init_db() -> None:
    """Функция init_db. При отсутствии базы донных создаёт их."""
    with sqlite3.connect(PATH_DB) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.executescript("PRAGMA foreign_keys = ON;")

        cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS user_info (
            telegramm_id INTEGER PRIMARY KEY NOT NULL,
            full_name TEXT DEFAULT NULL,
            telephone TEXT DEFAULT NULL,
            blocked BOOLEAN DEFAULT False,
            last_visit_date DATE
            );               
            """
        )

        cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS record_dates (

            telegram_id INTEGER DEFAULT 0,
            date DATE,
            hour INTEGER DEFAULT 0,
            FOREIGN KEY (telegram_id) REFERENCES user_info (telegramm_id) ON DELETE CASCADE
            );
            """
        )
        #             id INTEGER PRIMARY KEY AUTOINCREMENT,
        conn.commit()


def deleting_records_older_7_days() -> None:
    """Функция deleting_records_older_7_days. Удаляет записи старее 7 дней."""
    with sqlite3.connect(PATH_DB) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            DELETE FROM record_dates WHERE date < datetime('now', '-7 day')
            """
        )
        conn.commit()


def deletes_old_users() -> None:
    """Функция deletes_old_users. Удаляет пользователей, которые не заходили полгода."""
    with sqlite3.connect(PATH_DB) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            DELETE FROM user_info WHERE last_visit_date < datetime('now', '-6 month')
            """
        )
        conn.commit()


def user_check(telegram_id: int) -> list[Any]:
    """Функция user_check. Проверяет создан ли пользователь и возвращает статус его блокировки."""
    with sqlite3.connect(PATH_DB) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT blocked
            FROM user_info
            WHERE telegramm_id = ?;
            """,
            (telegram_id,),
        )
        res = cursor.fetchone()
        return res


def datetime_trans_str(date: datetime) -> str:
    """Функция datetime_trans_str. Переводит из формата datetime в str."""
    return f"{date.year}-{date.month}-{date.day}"


def add_user(telegram_id: int, full_name: str) -> None:
    """Функция add_user. Добавляет нового пользователя."""
    with sqlite3.connect(PATH_DB) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
                INSERT INTO user_info (telegramm_id, full_name, last_visit_date) VALUES (?, ?, ?);
            """,
            (telegram_id, full_name, datetime.datetime.now()),
        )
        conn.commit()


def update_visit_date(telegram_id: int) -> None:
    """Функция update_visit_date. Обновляет время посещения пользователя."""
    with sqlite3.connect(PATH_DB) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE user_info
            SET last_visit_date = ?
            WHERE telegramm_id = ?;            
            """,
            (datetime.datetime.now(), telegram_id),
        )
        conn.commit()


def count_date_rec(telegram_id: int) -> int:
    """Функция count_date_rec. Возвращает количество записей пользователя."""
    with sqlite3.connect(PATH_DB) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT count()
            FROM record_dates
            WHERE telegram_id = ?           
            """,
            (telegram_id,),
        )
    res = cursor.fetchone()[0]
    return res


def get_date_time_appointment(date: datetime) -> list[Any]:
    """Функция get_date_time_appointment. Возвращает дату и время записи пользователя."""
    with sqlite3.connect(PATH_DB) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT rd.hour, rd.telegram_id
            FROM record_dates as rd
            WHERE rd.date = ?;
            """,
            (f"{date.year}-{date.month}-{date.day}",),
        )
        res = cursor.fetchall()
        return res


def check_date_time_appointment(date: datetime) -> list[Any]:
    """Функция check_date_time_appointment. Проверяет занята дата и время записи."""
    with sqlite3.connect(PATH_DB) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT rd.hour, ui.telegramm_id
            FROM record_dates as rd
            JOIN user_info as ui on rd.telegram_id = ui.telegramm_id
            WHERE rd.date = '{date.year}-{date.month}-{date.day}' AND rd.hour == {date.hour};
            """
        )
        res = cursor.fetchall()
        return res


def set_date_time_appointment(contact, date: datetime) -> None:
    """Функция set_date_time_appointment. Обновляет номер телефона пользователя
    и записает на его на приём."""
    phone_number = contact.phone_number
    telegram_id = contact.user_id
    date_db = f"{date.year}-{date.month}-{date.day}"

    with sqlite3.connect(PATH_DB) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE user_info
            SET telephone = ?
            WHERE telegramm_id = ?;
            """,
            (
                phone_number,
                telegram_id,
            ),
        )

        cursor.execute(
            """
                INSERT INTO record_dates (telegram_id, date, hour) VALUES (?, ?, ?);
            """,
            (
                telegram_id,
                date_db,
                int(date.hour),
            ),
        )
        conn.commit()


def view_record(telegram_id: int) -> list[Any]:
    """Функция view_record. Возвращает все записи пользователя."""
    with sqlite3.connect(PATH_DB) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT date, hour
            FROM record_dates
            WHERE telegram_id == ?;
            """,
            (telegram_id,),
        )
        res = cursor.fetchall()
        return res


def del_record(date: str, hour: int) -> None:
    """Функция del_record. Удаляет запись."""
    with sqlite3.connect(PATH_DB) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            DELETE FROM record_dates
            WHERE date == ? AND hour == ?;
            """,
            (
                date,
                hour,
            ),
        )
        conn.commit()


def view_clients() -> list[Any]:
    """Функция view_clients. Возвращает всех клиентов."""
    with sqlite3.connect(PATH_DB) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT telegramm_id, full_name, telephone, blocked, last_visit_date
            FROM user_info
            """
        )
        res = cursor.fetchall()
        return res


def view_client_records(telegram_id: int) -> list[Any]:
    """Функция view_client_records. Возвращает все записи пользователя."""
    with sqlite3.connect(PATH_DB) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT date, hour
            FROM record_dates
            WHERE telegram_id = ?
            ORDER BY date;
            """,
            (telegram_id,),
        )
        res = cursor.fetchall()
        return res


def block_unblock_user(telegram_id: int, action: str) -> None:
    """Функция block_unblock_user. Блокирует и разблокирует пользователя."""
    with sqlite3.connect(PATH_DB) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE user_info
            SET blocked = ?
            WHERE telegramm_id = ?;
            """,
            (1 if action == "bl" else 0, telegram_id),
        )
        conn.commit()


def del_user(telegram_id: int) -> None:
    """Функция del_user. Удаляет пользователя."""
    with sqlite3.connect(PATH_DB) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.executescript("PRAGMA foreign_keys = ON;")
        cursor.execute(
            "DELETE FROM record_dates WHERE telegram_id = ?;",
            (telegram_id,),
        )

        conn.commit()


def search_client(search_text: str) -> set[Any]:
    """Функция search_client. Ищет пользователей по имени и номеру телефона."""
    with sqlite3.connect(PATH_DB) as conn:
        cursor: sqlite3.Cursor = conn.cursor()

        sql = "SELECT * FROM user_info WHERE full_name like ?"
        args = (f"%{search_text}%",)
        cursor.execute(sql, args)
        res = cursor.fetchall()

        sql = "SELECT * FROM user_info WHERE telephone like ?"
        args = (f"%{search_text}%",)
        cursor.execute(sql, args)
        res.extend(cursor.fetchall())
        res = set(res)
        return res


def reserve_day(
    telegram_id: int, date: datetime, beginning_working_day: int, end_working_day: int
) -> None:
    """Функция reserve_day. Резервирует день."""
    date = datetime_trans_str(date)
    with sqlite3.connect(PATH_DB) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM record_dates WHERE date == ?;",
            (date,),
        )

        for hour in range(beginning_working_day, end_working_day + 1):
            cursor.execute(
                "INSERT INTO record_dates(telegram_id, date, hour) VALUES(?, ?, ?);",
                (
                    telegram_id,
                    date,
                    hour,
                ),
            )
        conn.commit()


def mailing_for_day(date: datetime.date) -> set[Any]:
    """Функция mailing_for_day. Возвращает всех пользователя кто записан на день."""
    date = datetime_trans_str(date)
    with sqlite3.connect(PATH_DB) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT telegram_id FROM record_dates WHERE date = ?;
            """,
            (date,),
        )
        res = set(cursor.fetchall())
        return res


def viewing_recordings_day_db(date: datetime) -> list[Any]:
    """Функция viewing_recordings_day_db. Возвращает все записи на день."""
    date = datetime_trans_str(date)
    with sqlite3.connect(PATH_DB) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT full_name, telephone, hour
            FROM record_dates
            JOIN main.user_info ui on ui.telegramm_id = record_dates.telegram_id
            WHERE date = ?;
            """,
            (date,),
        )
        res = cursor.fetchall()
        return res
