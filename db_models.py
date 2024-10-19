from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    hash = db.Column(db.String(100))
    admin = db.Column(db.Boolean)
    calendar_filename = db.Column(db.String(100))
    
    def is_admin(self):
         return self.admin

