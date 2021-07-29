# -*- encoding: utf-8 -*-

import json
from datetime import datetime, timedelta
from dateManager import dateManager
import mimic
import time

def datetimeObjectToList(datetimeObj):
    return [datetimeObj.year, datetimeObj.month, datetimeObj.day,
            datetimeObj.hour, datetimeObj.minute]

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

    def searchIndexByNotifyTime(self, notifyTime):
        i = 0
        for event in self.events:
            if event.notifyTime - notifyTime >= timedelta(0):
                break
            i += 1

        return i

    def searchIndexByTitle(self, title):
        i = 0
        for event in self.events:
            if event.title == title:
                break
            i += 1

        return i

    # notifyTimeGap y notifyFrecuency reciben una lista de este tipo: [días, horas, minutos]
    def addNewEvent(self, title, date, description = None,
                    notifyTimeGap = [0, 0, 15], notifyFrecuency = [0, 0, 5]):

        notifyTimeGap = timedelta(days = notifyTimeGap[0],
                                  hours = notifyTimeGap[1],
                                  minutes = notifyTimeGap[2])

        notifyFrecuency = timedelta(days = notifyFrecuency[0],
                                    hours = notifyFrecuency[1],
                                    minutes = notifyFrecuency[2])

        newEvent = event(title, datetime(*date), description, notifyTimeGap, notifyFrecuency)

        if self.events == []:
            self.events.append(newEvent)
        else:
            self.events.insert(self.searchIndexByNotifyTime(newEvent.notifyTime), newEvent)

    def addLoadedEvent(self, title, date, description, notifyTimeGap, notifyFrecuency):
        self.events.append(event(title, datetime(*date), description,
                                timedelta(*notifyTimeGap), timedelta(*notifyFrecuency)))

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
                self.addLoadedEvent(eventDict['title'],
                                    eventDict['date'],
                                    eventDict['description'],
                                    eventDict['notify_time'],
                                    eventDict['notify_frecuency'])

    def deleteEvent(self, index):
        self.events.pop(index)

    def deleteAllEvents(self):
        self.events.clear()

    def getTimeToEvent(self, index):
        timeToEvent = self.events[index].date - datetime.now()
        return timedelta(days = timeToEvent.days, minutes = timeToEvent.seconds//60)

    def listEventsInRange(self, start, final):
        return self.events[self.searchIndexByDate(start):self.searchIndexByDate(final)]

    def getEventInformation(self, event, returnDate = True):
        eventInformation = [f'{event.title}']
        if returnDate:
            eventInformation.append(f'on {dateManager.datetimeToStr(event.date)}.')

        return eventInformation

    def getEventsInformationInRange(self, start, final):
        listOfEvents = self.listEventsInRange(start, final)
        eventsInformation = [f'From {dateManager.datetimeToStr(start)}',
                            'to', f'{dateManager.datetimeToStr(final)}.']

        if listOfEvents == []:
            eventsInformation.append('You don\'t have nothing to do.')
        else:
            eventsInformation.append('You have in your events list.')
            for event in listOfEvents:
                eventsInformation += self.getEventInformation(event)

        return eventsInformation

    def checkNotifyEvents(self):
        eventsToNotify = []
        eventsToDelete = []

        for event in self.events:

            event.getNextNotify()
            print(datetime(*datetimeObjectToList(datetime.now())))
            if event.nextNotify == None:
                eventsToDelete.append(event)
            elif datetime(*datetimeObjectToList(datetime.now())) == event.nextNotify:
                eventsToNotify.append(event)
            else:
                break

        for event in eventsToDelete:
            self.deleteEvent(0)
        
        return eventsToNotify

    def notifyEvents(self):
        pass

class event():

    def __init__(self, title, date, description, notifyTimeGap, notifyFrecuency):
        self.title = title
        self.date = date
        self.description = description
        self.notifyTimeGap = notifyTimeGap
        self.notifyTime = date - notifyTimeGap
        self.notifyFrecuency = notifyFrecuency
        self.nextNotify = self.notifyTime
        self.getNextNotify()

    def getNextNotify(self):
        diff = self.notifyTime - datetime(*datetimeObjectToList(datetime.now()))

        if diff < timedelta(0):
            self.nextNotify = self.notifyTime + self.notifyFrecuency * (-diff//self.notifyFrecuency + 1)

        if self.nextNotify > self.date:
            self.nextNotify = None

        print(self.nextNotify)

    def dumpDict(self):
        dict = {'title': self.title,
                'date': datetimeObjectToList(self.date),
                'description': self.description,
                'notify_time': timedeltaObjectToList(self.notifyTimeGap),
                'notify_frecuency': timedeltaObjectToList(self.notifyFrecuency)}

        return dict

JARVISeventManager = eventManager('../data/events/events.json')
engine = mimic.mimic()

JARVISeventManager.loadEvents()
JARVISeventManager.deleteAllEvents()
JARVISeventManager.addNewEvent('test', datetimeObjectToList(datetime.now()+timedelta(days = 1)))
JARVISeventManager.addNewEvent('test', datetimeObjectToList(datetime.now()+timedelta(minutes = 15)))
JARVISeventManager.addNewEvent('test', datetimeObjectToList(datetime.now()+timedelta(minutes = 15)))
JARVISeventManager.addNewEvent('test', datetimeObjectToList(datetime.now()+timedelta(minutes = 16)))
JARVISeventManager.addNewEvent('test', datetimeObjectToList(datetime.now()+timedelta(days = 3)))
#engine.say(*JARVISeventManager.getEventsInformationInRange(datetime.now(),datetime.now()+timedelta(days=3)))

while True:
    JARVISeventManager.events[0].getNextNotify()
    time.sleep(60)

JARVISeventManager.dumpEvents()