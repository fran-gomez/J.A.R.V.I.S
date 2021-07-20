# -*- encoding: utf-8 -*-

import datetime

class DateTime:

    def __init__(self) -> None:
        pass

    def date():
        fields = datetime.date.today().strftime("%A %B %d").split(' ')

        date = f'Today is {fields[0]}, {fields[1]} {fields[2]}'

        return date

    def time():
        str = datetime.datetime.now().strftime("%I %M").split(' ')
        hour = int(str[0])
        min = int(str[1])

        time = f'It\'s '
        if min == 0:
            time += f'{hour} oh clock'
        elif 0 < min <= 30:
            time += f'{min} past {hour}'
        elif 30 < min <= 59:
            remains = 60-min
            time += f'{remains} to {hour+1}'

        return time
