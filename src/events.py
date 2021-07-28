# -*- encoding: utf-8 -*-

import json
from datetime import datetime, timedelta
from dateManager import dateManager
import mimic

def datetimeObjectToList(datetimeObj):
    return [datetimeObj.year, datetimeObj.month, datetimeObj.day, datetimeObj.hour, datetimeObj.minute]

def timedeltaObjectToList(timedeltaObj):
    return [timedeltaObj.days, timedeltaObj.seconds]

class eventManager():
    
    def __init__(self, file):
        self.events = []
        self.amountOfEvents = len(self.events)
        self.file = file

    def deleteFileContent(self, file):
        with open(file, 'w'):
            pass

    def searchIndexByDate(self, date):
        i = 0
        for event in self.events:
            if event.date - date >= timedelta(0):
                break                    
            i += 1

        return i

    def searchIndexByNoticeTime(self, noticeTime):
        i = 0
        for event in self.events:
            if event.noticeTime - noticeTime >= timedelta(0):
                break                    
            i += 1

        return i

    def addLoadedEvent(self, title, date, description, noticeTimeGap):
        self.events.append(event(title, datetime(*date), description, noticeTimeGap))

    # noticeTimeGap recibe una lista de este tipo: [días, horas, minutos]
    def addNewEvent(self, title, date, description = None, noticeTimeGap = [0, 0, 15]):
        newEvent = event(title, datetime(*date), description, timedelta(days = noticeTimeGap[0], hours = noticeTimeGap[1], minutes = noticeTimeGap[2]))

        if self.events == []:
            self.events.append(newEvent)
        else:
            self.events.insert(self.searchIndexByNoticeTime(newEvent.noticeTime), newEvent)

    def dumpEvents(self):
        
        if self.events != []:    
            eventDictList = []

            for event in self.events:
                eventDictList.append(event.dumpDict())

            with open(self.file, 'w') as eventsFile:
                eventsFile.write(json.dumps(eventDictList, indent = 4))
        else:
            self.deleteFileContent(self.file)

    def loadEvents(self):
        eventsDictList = None
        fileContent = None

        with open(self.file, 'r') as eventsFile:
            fileContent = eventsFile.read()

        if not fileContent == '':
            eventsDictList = json.loads(fileContent)

            for eventDict in eventsDictList:
                self.addLoadedEvent(eventDict['title'], eventDict['date'], eventDict['description'], eventDict['notice_time'])

    def eraseEvent(self, index):
        self.events.pop(index)

    def eraseAllEvents(self):
        self.events.clear()

    def getTimeToEvent(self, index):
        timeToEvent = self.events[index].date - datetime.now()
        return timedelta(days = timeToEvent.days, minutes = timeToEvent.seconds//60)

    def listEventsInRange(self, start, final):
        return self.events[self.searchIndexByDate(start):self.searchIndexByDate(final)]

    def getEventsInformationInRange(self, start, final):
        listOfEvents = self.listEventsInRange(start, final)
        eventsInformation = [f'From {dateManager.datetimeToStr(start)}', 'to', f'{dateManager.datetimeToStr(final)}.']

        if listOfEvents == []:
            eventsInformation.append('You don\'t have nothing to do.')
        else:
            eventsInformation.append('You have in your events list.')
            for event in listOfEvents:
                eventsInformation + [f'{event.title}', f'on {dateManager.datetimeToStr(event.date)}.']

        return eventsInformation

    def isTimeToEvent(self):
        pass

class event():

    def __init__(self, title, date, description, noticeTimeGap):
        self.title = title
        self.date = date
        self.description = description
        self.noticeTimeGap = noticeTimeGap
        self.noticeTime = date - noticeTimeGap

    def dumpDict(self):
        dict = {'title': self.title,
                'date': datetimeObjectToList(self.date),
                'description': self.description,
                'notice_time': timedeltaObjectToList(self.noticeTimeGap),}

        return dict

JARVISeventManager = eventManager('../data/events/events.json')
engine = mimic.mimic()

#JARVISeventManager.loadEvents()
JARVISeventManager.eraseAllEvents()
JARVISeventManager.addNewEvent('test', datetimeObjectToList(datetime.now()+timedelta(days = 1)))
JARVISeventManager.addNewEvent('test', datetimeObjectToList(datetime.now()+timedelta(hours = 4)))
JARVISeventManager.addNewEvent('test', datetimeObjectToList(datetime.now()+timedelta(days = 3)))
#engine.say(*JARVISeventManager.getEventsInformationInRange(datetime.now(),datetime.now()+timedelta(days=3)))
JARVISeventManager.dumpEvents()