import icalendar
from models import Event, DateTimeRange
from datetime import time, date
import datetime

def load_events_from_ics(calendar_name):
    events = []
    with open(f'uploads/{calendar_name}', 'rb') as ics_file:
        calendar = icalendar.Calendar.from_ical(ics_file.read())
    
    for index, event in enumerate(calendar.walk()):
        summary = event.get('summary')
        if (summary == None):
            continue
        
        start = event.get('dtstart').dt
        end = event.get('dtend').dt

        
        rrule = (event.get('rrule'))

        if rrule:
            continue

        defaultTime = time(10, 0, 0)
        if isinstance(start, date) and not isinstance(start, datetime.datetime):
                # Convert to datetime by adding a default time (e.g., 00:00)
                start = datetime.datetime.combine(start, defaultTime)  

        if isinstance(end, date) and not isinstance(end, datetime.datetime):
                end = datetime.datetime.combine(end, defaultTime)  

        end = end.replace(hour=(max(end.hour - 4, 0)))
        start = start.replace(hour=(max(start.hour - 4, 0)))
        
        parsed_event = Event(start, end, summary)
        events.append(parsed_event)
    
    return events

def convert_list_events_to_json(events_list):
    events = {}
    for event in events_list:
        jsonified = {
            "start": str(event.start),
            "end": str(event.end)
        }
        events[event.name] = jsonified
    return events

def find_events_on_day(events_list, date):
    events_on_day = []
    for event in events_list:
        if (event.start.date() == date or event.end.date() == date):
            events_on_day.append(event)
    return events_on_day

def find_available_times(all_users_events_list, target_day):
    all_users_events_on_day = []
    available_times = []

    for event_list in all_users_events_list:
        all_users_events_on_day.append(find_events_on_day(event_list, target_day))

    #compose list of all lists
    all_events = [item for sublist in all_users_events_on_day for item in sublist]

    if len(all_events) == 0:
        return []
    
    all_events.reverse()
    all_events.sort(key=lambda x: x.start) # sort events by start time
    
    if (all_events[0].start.time() > time(0,0,0)):
        available_times.append(DateTimeRange(time(0,0,0), all_events[0].start.time()))
    
    if (all_events[-1].end.time() < time(23,59,59)):
        available_times.append(DateTimeRange(all_events[-1].end.time(), time(23, 59, 59) ))


    for i in range(len(all_events) - 1):
        current_event = all_events[i]
        next_event = all_events[i + 1]
        if (current_event.end < next_event.start): #this is a free time
            available_times.append(DateTimeRange(current_event.end.time(), next_event.start.time()))
    
    print(available_times)
    return available_times

