from flask import *
import icalendar
from pathlib import Path
from models import Event
from db_models import db, User
from parse_events import *
import datetime
from jinja2 import *
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, current_user, LoginManager, login_required, logout_user, AnonymousUserMixin
import flask_login
import os

# Load the Jinja environment and template
env = Environment(loader=FileSystemLoader('templates'))


def create_app():
    app = Flask(__name__)
    login_manager = LoginManager()
    login_manager.init_app(app)
    # config dummy secret key
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['UPLOAD_FOLDER'] = 'uploads/'

    # initialize login features
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
    return app


app = create_app()
db.init_app(app)

with app.app_context():
    db.create_all()

calendar_name = "test.ics"
target_day = datetime.date(2024, 10, 21)



@login_required
@app.route('/')
def hello():
    if isinstance(current_user, AnonymousUserMixin):
        return render_template("home.html", available_times = [])
    
    calendar_name = current_user.calendar_filename

    if not calendar_name:
        return render_template("home.html", available_times = [])
    
    events_list = load_events_from_ics(calendar_name)
        
    events_on_day = find_events_on_day(events_list, target_day)
    available_times = find_available_times([events_list], target_day)
    
    return render_template("home.html", available_times = available_times )

@app.route('/profile')
@login_required
def profile():
    return render_template("profile.html", current_user=current_user)

@app.route('/upload_calendar', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part in the request", 400
    file = request.files['file']

    # If no file is selected
    if file.filename == '':
        return "No selected file", 400

    
    if file and file.filename.split('.')[-1].lower() == "ics":
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # remember the uploaded filename
        current_user.calendar_filename = filename
        db.session.add(current_user)
        db.session.commit()

        
    return redirect('/profile')
    
@app.route('/signup')
def signup_page():
    return render_template("signup.html")


@app.route('/', methods=['POST'])
def home_with_date():
    # get the target day and update it
    global target_day
    selected_date = request.form['selectedDate']
    date_split = selected_date.split('-')
    target_date = date(int(date_split[0]), int(date_split[1]), int(date_split[2]))
    target_day = target_date

    # load the calendars of the 3 participants
    participant1_email = request.form.get('participant1')
    participant2_email = request.form.get('participant2')
    participant3_email = request.form.get('participant3')

    user1 = db.session.query(User).filter_by(email=participant1_email).first()
    user2 = db.session.query(User).filter_by(email=participant2_email).first()
    user3 = db.session.query(User).filter_by(email=participant3_email).first()

    user1events = []
    user2events = []
    user3events = []

    if user1:
        if user1.calendar_filename:
            user1events = load_events_from_ics(user1.calendar_filename)
    if user2:
        if user2.calendar_filename:
            user2events = load_events_from_ics(user2.calendar_filename)
    if user3:
        if user3.calendar_filename:
            user3events = load_events_from_ics(user3.calendar_filename)


    return render_template("home.html", available_times=find_available_times([user1events, user2events, user3events], target_day))

@app.route('/add_user', methods=['POST'])
def add_user():
    password = request.form.get('password')  # Getting the 'name' field from the form
    email = request.form.get('email')  # Getting the 'email' field from the form
    new_user = User(email=email, hash=password, admin=False)
    db.session.add(new_user)
    db.session.commit()
    flask_login.login_user(new_user, remember=True)

    return redirect('/profile')

@app.route('/login_user', methods=['POST'])
def login_user():
    password = request.form.get('password')  # Getting the 'name' field from the form
    email = request.form.get('email')  # Getting the 'email' field from the form

    user = User.query.filter_by(email=email).first() # get user with this email
    if not user or user.hash != password:
        return redirect('/login')
    
    flask_login.login_user(user, remember=True)
    return redirect('/')

@app.route('/login')
def login_page():
    return render_template("login.html", current_user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

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

