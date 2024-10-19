from flask import *
import icalendar
from pathlib import Path
from models import Event
from db_models import db, User
from parse_events import *
import datetime
from jinja2 import *
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, current_user 

# Load the Jinja environment and template
env = Environment(loader=FileSystemLoader('templates'))


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
    return app

app = create_app()
db.init_app(app)

with app.app_context():
    db.create_all()

calendar_name = "test.ics"
target_day = datetime.date(2024, 10, 21)

@app.route('/')
def hello():
    events_list = load_events_from_ics(calendar_name)
    events_on_day = find_events_on_day(events_list, target_day)
    print(find_available_times([events_list], target_day))
    return render_template("layout.html")

@app.route('/signup')
def signup_page():
    return render_template("signup.html")

@app.route('/add_user', methods=['POST'])
def add_user():
    password = request.form.get('password')  # Getting the 'name' field from the form
    email = request.form.get('email')  # Getting the 'email' field from the form
    new_user = User(email=email, hash=password, admin=False)
    db.session.add(new_user)
    db.session.commit()
    
    print(email, password)
    return redirect('/templates')

@app.route('/templates')
def template():

    template = env.get_template('template.html')

    events_list = load_events_from_ics(calendar_name)
    events_on_day = find_events_on_day(events_list, target_day)



    # Context data to pass into the template
    context = {
        'title': 'Available Times',
        'date': target_day,
        'events': events_on_day
    }

    # Render the template with context and return it as the response
    output = template.render(context)
    return output  # Manually rendered HTML from Jinja

if __name__ == "__main__":
    app.run(debug=True)

if __name__ == "__main__":
    app.run(debug=True)

