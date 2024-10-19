import icalendar
from models import Event, DateTimeRange
from datetime import time

def load_events_from_ics(calendar_name):
    events = []
    with open(f'calendars/{calendar_name}', 'rb') as ics_file:
        calendar = icalendar.Calendar.from_ical(ics_file.read())
    
    for index, event in enumerate(calendar.walk()):
        summary = event.get('summary')
        if (summary == None):
            continue
        
        start = event.get('dtstart').dt
        end = event.get('dtend').dt

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
    for event_list in all_users_events_list:
        all_users_events_on_day.append(find_events_on_day(event_list, target_day))

    for event_list in all_users_events_on_day:
        earliest_time = time(0, 0, 0)
        latest_time = time(23, 59, 59)

        print(latest_time > earliest_time)
    
    