import datetime


class InternalCalendar:
    CURRENT_DATETIME = datetime.datetime.now()
    CURRENT_DATE = CURRENT_DATETIME.date()

    def __init__(self):
        self.calen_date = self.CURRENT_DATE

    def next_month(self):
        # self.calen_date = self.calen_date.replace(day=1, month=self.calen_date.month + 1)
        try:
            self.calen_date = self.calen_date.replace(self.calen_date.year, self.calen_date.month + 1, 1)
        except ValueError:
            self.calen_date = self.calen_date.replace(self.calen_date.year + 1, 1, 1)
        return self.calen_date

    def previous_month(self):
        # self.calen_date = self.calen_date.replace(day=1, month=self.calen_date.month - 1)
        try:
            self.calen_date = self.calen_date.replace(self.calen_date.year, self.calen_date.month - 1, 1)
        except ValueError:
            self.calen_date = self.calen_date.replace(self.calen_date.year - 1, 12, 1)
        return self.calen_date

    def is_previous_month(self):
        return self.CURRENT_DATE.month == self.calen_date.month and self.CURRENT_DATE.year == self.calen_date.year
