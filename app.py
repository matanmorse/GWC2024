from flask import *
import icalendar
from pathlib import Path
from models import Event
from parse_events import *
import datetime
from jinja2 import *

app = Flask(__name__)

calendar_name = "test.ics"
target_day = datetime.date(2024, 11, 21)

@app.route('/')
def hello():
    events_list = load_events_from_ics(calendar_name)
    events_on_day = find_events_on_day(events_list, target_day)
    print(find_available_times([events_list], target_day))
    return convert_list_events_to_json(events_on_day)

@app.route('/templates')
def template():

    # Load the Jinja environment and template
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('template.html')

    # Context data to pass into the template
    context = {
        'title': 'My Shopping List',
        'items': ['Milk', 'Eggs', 'Bread']
    }

    # Render the template with context and return it as the response
    output = template.render(context)
    return output  # Manually rendered HTML from Jinja

if __name__ == "__main__":
    app.run(debug=True)

if __name__ == "__main__":
    app.run(debug=True)

