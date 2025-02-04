"""Модуль календаря"""
import datetime


class InternalCalendar:
    CURRENT_DATETIME = datetime.datetime.now()

    def __init__(self, telegram_id) -> None:
        self.telegram_id = telegram_id
        self.internal_date = datetime.datetime.now().date()

    async def refresh_datetime(self) -> None:
        self.CURRENT_DATETIME = datetime.datetime.now()

    async def next_month(self) -> datetime.date:
        try:
            self.internal_date = self.internal_date.replace(self.internal_date.year, self.internal_date.month + 1, 1)
        except ValueError:
            self.internal_date = self.internal_date.replace(self.internal_date.year + 1, 1, 1)

        await self.refresh_datetime()
        return self.internal_date

    async def pre_month(self) -> datetime.date:
        day = 1
        try:
            if (self.internal_date.month == self.CURRENT_DATETIME.date().month + 1 and
                    self.internal_date.year == self.CURRENT_DATETIME.date().year):
                day = datetime.datetime.now().date().day
            self.internal_date = self.internal_date.replace(self.internal_date.year, self.internal_date.month - 1, day)
        except ValueError:
            self.internal_date = self.internal_date.replace(self.internal_date.year - 1, 12, day)

        await self.refresh_datetime()
        return self.internal_date

    async def is_pre_month(self) -> bool:
        await self.refresh_datetime()
        return self.CURRENT_DATETIME.month < self.internal_date.month and self.CURRENT_DATETIME.year == self.internal_date.year

    async def current_date(self):
        await self.refresh_datetime()
        return self.internal_date
