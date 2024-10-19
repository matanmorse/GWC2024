import json

class Event:
    def __init__(self, start, end, name):
        self.name = name
        self.end = end
        self.start = start

    def to_json(self):
        jsonified = {
            "name": self.name,
            "start": str(self.start),
            "end": str(self.end),
        }
        return json.dumps(jsonified, indent=4)

class DateTimeRange:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __str__(self):
        return f"Start: {self.start.strftime('%I:%M %p')}, End: {self.end.strftime('%I:%M %p')}"