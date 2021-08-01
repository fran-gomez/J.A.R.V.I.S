# -*- encoding: utf-8 -*-

import json
from datetime import datetime, timedelta


from date_manager import DateManager
import mimic


def datetime_object_to_list(datetimeObj):
    """Extracts the main datetime attributes to a list.
    Ignores the seconds and microseconds.
    """
    return [datetimeObj.year, datetimeObj.month, datetimeObj.day,
            datetimeObj.hour, datetimeObj.minute]

def timedelta_object_to_list(timedeltaObj):
    """Extracts the main timedelta attributes to a list.
    Ignores the microseconds.
    """
    return [timedeltaObj.days, timedeltaObj.seconds]


class EventManager():
    
    """An event manager implementation.
    It provides a basic event management.
    """

    def __init__(self, file):
        self.events = []
        self.file = file

    def _delete_file_content(self, file):
        with open(file, 'w'):
            pass


    # Search functions
    def search_index_by_date(self, date):
        i = 0
        for event in self.events:
            if event.date - date >= timedelta(0):
                break
            i += 1

        return i

    def search_index_by_notify_time(self, notifyTime):
        i = 0
        for event in self.events:
            if event.notifyTime - notifyTime >= timedelta(0):
                break
            i += 1

        return i

    def search_index_by_title(self, title):
        i = 0
        for event in self.events:
            if event.title == title:
                break
            i += 1

        return i


    # Event management section

    # notifyTimeGap recieves a list of this type: [days, hours, minutes]
    def add_new_event(self, title, date, description = None,
                      notifyTimeGap = [0, 0, 15]):
        """Adds a new event to the event manager list.
        It recieves the same parameters as the event class recieve.
        """
        notifyTimeGap = timedelta(days = notifyTimeGap[0],
                                  hours = notifyTimeGap[1],
                                  minutes = notifyTimeGap[2],
                                  )

        newEvent = Event(title, datetime(*date), description, notifyTimeGap)

        if self.events == []:
            self.events.append(newEvent)
        else:
            self.events.insert(
                self.search_index_by_notify_time(newEvent.notifyTime),
                newEvent,
            )


    def _add_loaded_event(self, title, date, description, notifyTimeGap):
        """Loads an event to the event manager list.
        Its use is specific to work with the load_events method.
        """
        self.events.append(Event(title, datetime(*date),
                                 description, timedelta(*notifyTimeGap)))

    def dump_events(self):
        """Dumps the event manager list of events to a json file.
        It uses the self.file variable.
        """
        if self.events != []:    
            eventDictList = []

            for event in self.events:
                eventDictList.append(event.dump_dict())

            with open(self.file, 'w') as eventsFile:
                eventsFile.write(json.dumps(eventDictList, indent = 4))
        else:
            self.delete_file_content(self.file)

    def load_events(self):
        """Reads the json file with the saved events.
        Calls the _add_loaded_event method to add 
        them to the event manager list.
        """
        eventsDictList = None
        fileContent = None

        with open(self.file, 'r') as eventsFile:
            fileContent = eventsFile.read()

        if not fileContent == '':
            eventsDictList = json.loads(fileContent)

            for eventDict in eventsDictList:
                self._add_loaded_event(eventDict['title'],
                                    eventDict['date'],
                                    eventDict['description'],
                                    eventDict['notify_time'],
                                )

    def delete_event(self, index):
        self.events.pop(index)

    def delete_all_events(self):
        self.events.clear()

    def get_time_to_event(self, index):
        timeToEvent = self.events[index].date - datetime.now()
        return timedelta(days = timeToEvent.days,
                         minutes = timeToEvent.seconds//60)

    def get_amout_of_events(self):
        return len(self.events)

    def list_events_in_range(self, start, final):
        """Returns a list of the events objects in the
        event manager between start and final dates.
        """
        return self.events[self.search_index_by_date(start):self.search_index_by_date(final)]

    def get_event_information(self, event, returnDate = True):
        """Gets basic infomation of an event.
        Always return the title, but only returns the date if returnDate is True.
        By default returnDate is True.
        """
        eventInformation = [f'{event.title}']
        if returnDate:
            eventInformation.append(f'on {DateManager.datetime_to_str(event.date)}.')

        return eventInformation

    def get_events_information_in_range(self, start, final):
        """Returns a list of strings with the output of
        get_event_information of the events between the
        start and final date.
        """
        listOfEvents = self.list_events_in_range(start, final)
        eventsInformation = [f'From {DateManager.datetime_to_str(start)}',
                            'to', f'{DateManager.datetime_to_str(final)}.']

        if listOfEvents == []:
            eventsInformation.append("You don't have nothing to do.")
        else:
            eventsInformation.append('You have this events.')
            for event in listOfEvents:
                eventsInformation += self.get_event_information(event)

        return eventsInformation

    # Current working section

    def checkNotifyEvents(self):
        eventsToNotify = []
        oneMoreTime = False
        now = datetime(*datetime_object_to_list(datetime.now()))

        for event in self.events:
            if  event.notifyTime < now < event.date:
                eventsToNotify.append(event)
                oneMoreTime = True
            elif not oneMoreTime:
                oneMoreTime = False
                break

        return eventsToNotify

    def checkPastEvents(self):
        pass

    def notifyEvents(self):
        pass


class Event():

    """Class for events objects."""

    def __init__(self, title, date, description, notifyTimeGap):
        self.title = title
        self.date = date
        self.description = description
        self.notifyTimeGap = notifyTimeGap
        self.notifyTime = date - notifyTimeGap

    def dump_dict(self):
        """Returns a dictionary with the attributes of the object.
        Its propuse is to work with the event manager dump_events method.
        """
        dict = {'title': self.title,
                'date': datetime_object_to_list(self.date),
                'description': self.description,
                'notify_time': timedelta_object_to_list(self.notifyTimeGap),
            }

        return dict


JARVISeventManager = EventManager('../data/events/events.json')
engine = mimic.mimic()

JARVISeventManager.load_events()
JARVISeventManager.delete_all_events()
JARVISeventManager.add_new_event('test', datetime_object_to_list(datetime.now()+timedelta(minutes = 5)))
JARVISeventManager.add_new_event('test', datetime_object_to_list(datetime.now()+timedelta(minutes = 15)))
JARVISeventManager.add_new_event('test', datetime_object_to_list(datetime.now()+timedelta(minutes = 15)))
JARVISeventManager.add_new_event('test', datetime_object_to_list(datetime.now()+timedelta(minutes = 16)))
JARVISeventManager.add_new_event('test', datetime_object_to_list(datetime.now()+timedelta(days = 3)))
#engine.say(*JARVISeventManager.get_events_information_in_range(datetime.now(),datetime.now()+timedelta(days=3)))

JARVISeventManager.dump_events()