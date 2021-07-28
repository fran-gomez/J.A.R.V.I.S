# -*- encoding: utf-8 -*-

from datetime import datetime

class dateManager:

    def __init__(self):
        pass

    def dateToStr(self, date):
        dateStr = date.strftime("%A, %B %d")

        return dateStr

    def timeToStr(self, time):
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

    def datetimeToStr(self, datetimeObj):
        return self.dateToStr(datetimeObj) + ' at ' + self.timeToStr(datetimeObj)

    def todayStr(self):
        return 'Today is ' + self.dateToStr(datetime.today())

    def nowStr(self):
        return 'It\'s ' + self.timeToStr(datetime.now())

motor = dateManager()
print(motor.datetimeToStr(datetime.now()))