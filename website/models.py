from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime



class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    role = db.Column(db.String(50), default='organizer')
    notes = db.relationship('Note')

class Locker(db.Model):
    __tablename__ = 'locker'

    id = db.Column(db.Integer, primary_key=True)
    name1 = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    item_type = db.Column(db.String(50))  
    attendee_type = db.Column(db.String(50))
    color = db.Column(db.String(50))  
    notes = db.Column(db.Text)
    paid = db.Column(db.Boolean, default=False)  
    item_status = db.Column(db.String(20), default='Inside') 
    cost = db.Column(db.Float)
    time = db.Column(db.DateTime, default=datetime.utcnow)
    start_time = db.Column(db.DateTime)
    cost_per_hour = db.Column(db.Float, default=30.0) 

    def __repr__(self):
        return f'<Locker {self.id} - {self.name1}>'
    
    @property
    def calculated_cost(self):
        if self.item_status == "Outside":
            return 0.0

        if not self.time:
            return 0.0

        elapsed_time = datetime.utcnow() - self.time
        elapsed_seconds = int(elapsed_time.total_seconds())

        if elapsed_seconds <= 3600:
            return 30.0 
        elif 3601 <= elapsed_seconds <= 7200:
            return 60.0 
        elif 7201 <= elapsed_seconds <= 10800:
            return 90.0 
        elif 10801 <= elapsed_seconds <= 14400:
            return 120.0  
        elif 14401 <= elapsed_seconds <= 18000:
            return 150.0  
        elif 18001 <= elapsed_seconds <= 21600:
            return 180.0  
        elif 21601 <= elapsed_seconds <= 25200:
            return 210.0  
        elif 25201 <= elapsed_seconds <= 28800:
            return 240.0 
        elif 28801 <= elapsed_seconds <= 32400:
            return 270.0  
        elif 32401 <= elapsed_seconds <= 36000:
            return 300.0  
        else:
            return 0.0 