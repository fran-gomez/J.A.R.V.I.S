import json
from datetime import datetime, timedelta


from date_manager import DateManager
import mimic


def datetime_object_to_list(datetime_obj):
    """Extracts the main datetime attributes to a list.
    Ignores the seconds and microseconds.
    """
    return [datetime_obj.year, datetime_obj.month, datetime_obj.day,
            datetime_obj.hour, datetime_obj.minute]


def timedelta_object_to_list(timedelta_obj):
    """Extracts the main timedelta attributes to a list.
    Ignores the microseconds.
    """
    return [timedelta_obj.days, timedelta_obj.seconds]


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

    def search_index_by_notify_time(self, notify_time):
        i = 0
        for event in self.events:
            if event.notify_time - notify_time >= timedelta(0):
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

    # notify_time_gap recieves a list of this type: [days, hours, minutes]
    def add_new_event(self, title, date, description = None,
                      notify_time_gap = [0, 0, 15]):
        """Adds a new event to the event manager list.
        It recieves the same parameters as the event class recieve.
        """
        notify_time_gap = timedelta(days = notify_time_gap[0],
                                  hours = notify_time_gap[1],
                                  minutes = notify_time_gap[2])

        new_event = Event(title, datetime(*date),
                          description, notify_time_gap)

        if self.events == []:
            self.events.append(new_event)
        else:
            self.events.insert(
                self.search_index_by_notify_time(new_event.notify_time),
                new_event)


    def _add_loaded_event(self, title, date, description, notify_time_gap):
        """Loads an event to the event manager list.
        Its use is specific to work with the load_events method.
        """
        self.events.append(Event(title, datetime(*date),
                                 description, timedelta(*notify_time_gap)))

    def dump_events(self):
        """Dumps the event manager list of events to a json file.
        It uses the self.file variable.
        """
        if self.events != []:    
            events_dict_list = []

            for event in self.events:
                events_dict_list.append(event.dump_dict())

            with open(self.file, 'w') as events_file:
                events_file.write(json.dumps(events_dict_list, indent = 4))
        else:
            self.delete_file_content(self.file)

    def load_events(self):
        """Reads the json file with the saved events.
        Calls the _add_loaded_event method to add 
        them to the event manager list.
        """
        events_dict_list = None
        file_content = None

        with open(self.file, 'r') as events_file:
            file_content = events_file.read()

        if not file_content == '':
            events_dict_list = json.loads(file_content)

            for event_dict in events_dict_list:
                self._add_loaded_event(event_dict['title'],
                                       event_dict['date'],
                                       event_dict['description'],
                                       event_dict['notify_time'])

    def delete_event(self, index):
        self.events.pop(index)

    def delete_all_events(self):
        self.events.clear()

    def get_time_to_event(self, index):
        time_to_event = self.events[index].date - datetime.now()
        return timedelta(days = time_to_event.days,
                         minutes = time_to_event.seconds//60)

    def get_amout_of_events(self):
        return len(self.events)

    def get_event_information(self, event, return_date = True, return_description = False):
        """Gets basic infomation of an event. Always return the title,
        but only returns the date if return_date is True.
        Which by default is True.
        """
        event_information = [f'{event.title}']

        if return_description:
            event_information.append(event.description)

        if return_date:
            date_str = f'on {DateManager.datetime_to_str(event.date)}.'
            event_information.append(date_str)

        return event_information

    def get_events_information_range(self, start_date, final_date):
        """Returns a list of strings with the output of
        get_event_information of the events between the
        start and final date.
        """

        start_index = self.search_index_by_date(start_date)
        final_index = self.search_index_by_date(final_date)

        events_information = [f'From {DateManager.datetime_to_str(start_date)}',
                            'to', f'{DateManager.datetime_to_str(final_date)}.']

        if start_index == None and final_index == None:
            events_information.append("You don't have nothing to do.")
        elif start_index == None or final_index == None:
            events_information.append("An error occurred.")
        else:
            events_information.append('You have this events.')
            for event in self.events[start_index:final_index]:
                events_information += self.get_event_information(event)

        return events_information


    # Current working section

    def check_notify_events(self):
        last_event_to_notify = 0
        one_more_time = False
        now = datetime(*datetime_object_to_list(datetime.now()))
        i = 0

        for event in self.events:
            if  event.notify_time < now < event.date:
                last_event_to_notify = i
                one_more_time = True
                i += 1 
            elif not one_more_time:
                break

        return last_event_to_notify

    def check_past_events(self):
        pass

    def notify_events(self):
        
        notify = []
        last_event_to_notify = self.check_notify_events()

        if self.events[:last_event_to_notify + 1] == []:
            notify.append(None)
        else:
            notify.append('You have near events.')
            for event in self.events[:last_event_to_notify + 1]:
                notify.extend(self.get_event_information(event))

        return notify


class Event():

    """Class for events objects."""

    def __init__(self, title, date, description, notify_time_gap):
        self.title = title
        self.date = date
        self.description = description
        self.notify_time_gap = notify_time_gap
        self.notify_time = date - notify_time_gap

    def dump_dict(self):
        """Returns a dictionary with the attributes of the object.
        Its propuse is to work with the event manager dump_events method.
        """
        dict = {'title': self.title,
                'date': datetime_object_to_list(self.date),
                'description': self.description,
                'notify_time': timedelta_object_to_list(self.notify_time_gap),
            }

        return dict


JARVISeventManager = EventManager('../data/events/events.json')
engine = mimic.Mimic()

JARVISeventManager.load_events()
""" JARVISeventManager.delete_all_events()
JARVISeventManager.add_new_event('test', datetime_object_to_list(datetime.now()+timedelta(minutes = 5)))
JARVISeventManager.add_new_event('test', datetime_object_to_list(datetime.now()+timedelta(minutes = 15)))
JARVISeventManager.add_new_event('test', datetime_object_to_list(datetime.now()+timedelta(minutes = 15)))
JARVISeventManager.add_new_event('test', datetime_object_to_list(datetime.now()+timedelta(minutes = 16)))
JARVISeventManager.add_new_event('test', datetime_object_to_list(datetime.now()+timedelta(days = 3))) """
print(JARVISeventManager.notify_events())
engine.say(*JARVISeventManager.notify_events())

JARVISeventManager.dump_events()