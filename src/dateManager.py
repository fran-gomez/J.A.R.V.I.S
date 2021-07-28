# -*- encoding: utf-8 -*-

from datetime import datetime

class dateManager:

    def __init__(self):
        pass

    def dateToStr(date):
        dateStr = date.strftime("%A, %B %d")

        return dateStr

    def timeToStr(time):
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

    def datetimeToStr(datetimeObj):
        return dateManager.dateToStr(datetimeObj) + ' at ' + dateManager.timeToStr(datetimeObj)

    def todayStr():
        return 'Today is ' + dateManager.dateToStr(datetime.today())

    def nowStr(self):
        return 'It\'s ' + dateManager.timeToStr(datetime.now())