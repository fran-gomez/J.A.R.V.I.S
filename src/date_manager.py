from datetime import date, datetime


class DateManager:

    """Functions to transform datetime objects into strings"""

    # Base methods.
    @classmethod
    def date_to_str(cls, date):
        """Returns a date as a string from a datetime object."""
        date_str = date.strftime("%A, %B %d")
        return date_str

    @classmethod
    def time_to_str(cls, time):
        """Returns a time as a string from a datetime object,
        it ignores seconds and microseconds.
        """
        hour = time.hour
        min = time.minute
        time_str = ''

        if min == 0:
            time_str += f'{hour} oh clock'
        elif 0 < min <= 30:
            time_str += f'{min} past {hour}'
        elif 30 < min <= 59:
            remains = 60-min
            time_str += f'{remains} to {hour+1}'

        return time_str


    # Specific methods, built on the base ones.
    @classmethod
    def datetime_to_str(cls, datetime_obj):
        """Returns a complete datetime object transformed into a string
        using the date_to_str and time_to_str class methods.
        """
        return ''.join([cls.date_to_str(datetime_obj), ' at ',
                        cls.time_to_str(datetime_obj)])

    @classmethod
    def today_str(cls):
        """Returns a string expressing the current day."""
        return f'Today is {cls.date_to_str(datetime.today())}'

    @classmethod
    def now_str(cls):
        """Returns a string expressing the current time"""
        return f'It\'s {cls.time_to_str(datetime.now())}'

print(DateManager.datetime_to_str(datetime.now()))