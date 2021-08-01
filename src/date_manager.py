from datetime import datetime


class DateManager:

    """Functions to transform datetime objects into strings"""

    # Base methods.
    @classmethod
    def date_to_str(cls, date):
        """Returns a date as a string from a datetime object."""
        dateStr = date.strftime("%A, %B %d")
        return dateStr

    @classmethod
    def time_to_str(cls, time):
        """Returns a time as a string from a datetime object,
        it ignores seconds and microseconds.
        """
        hour = time.hour
        min = time.minute
        timeStr = ''

        if min == 0:
            timeStr += f'{hour} oh clock'
        elif 0 < min <= 30:
            timeStr += f'{min} past {hour}'
        elif 30 < min <= 59:
            remains = 60-min
            timeStr += f'{remains} to {hour+1}'

        return timeStr


    # Specific methods, built on the base ones.
    @classmethod
    def datetime_to_str(cls, datetimeObj):
        """Returns a complete datetime object transformed into a string
        using the date_to_str and time_to_str class methods.
        """
        return cls.date_to_str(datetimeObj) + ' at ' \
            + cls.time_to_str(datetimeObj)

    @classmethod
    def today_str(cls):
        """Returns a string expressing the current day."""
        return 'Today is ' + cls.date_to_str(datetime.today())

    @classmethod
    def now_str(cls):
        """Returns a string expressing the current time"""
        return 'It\'s ' + cls.time_to_str(datetime.now())