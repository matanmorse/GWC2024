from flask import *
import icalendar
from pathlib import Path

app = Flask(__name__)

@app.route('/')
def hello():
    
    with open('matan_classes.ics', 'rb') as ics_file:
        calendar = icalendar.Calendar.from_ical(ics_file.read())
        print(calendar)
    return "hi"
if __name__ == "__main__":
    app.run(debug=True)