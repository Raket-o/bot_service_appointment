"""Модуль календаря"""
import datetime


CURRENT_DATETIME = datetime.datetime.now()


class InternalCalendar:
    def __init__(self, telegram_id) -> None:
        self.telegram_id = telegram_id
        self.internal_date = CURRENT_DATETIME.date()

    async def next_month(self) -> datetime.date:
        try:
            self.internal_date = self.internal_date.replace(self.internal_date.year, self.internal_date.month + 1, 1)
        except ValueError:
            self.internal_date = self.internal_date.replace(self.internal_date.year + 1, 1, 1)
        return self.internal_date

    async def pre_month(self) -> datetime.date:
        try:
            self.internal_date = self.internal_date.replace(self.internal_date.year, self.internal_date.month - 1, 1)
        except ValueError:
            self.internal_date = self.internal_date.replace(self.internal_date.year - 1, 12, 1)
        return self.internal_date

    async def is_pre_month(self) -> bool:
        return CURRENT_DATETIME.month < self.internal_date.month and CURRENT_DATETIME.year == self.internal_date.year

    async def current_date(self):
        return self.internal_date
