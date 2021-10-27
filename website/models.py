from . import db
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__='Users' # good practice to specify table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    email = db.Column(db.String(100), index=True, nullable=False)
	#password is never stored in the DB, an encrypted password is stored
	# the storage should be at least 255 chars long
    password = db.Column(db.String(255), nullable=False)

    # relation to call user.comments and comment.created_by
    reviews = db.relationship('Review', backref='User')


class Event(db.Model):
    __tablename__ = 'Events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(200))
    long_description = db.Column(db.String(400))
    ticket_price = db.Column(db.Integer)
    organiser = db.Column(db.String(80))
    type = db.Column(db.String(80))
    street = db.Column(db.String(80))
    city = db.Column(db.String(80))
    state = db.Column(db.String(80))
    postcode = db.Column(db.String(4))
    image = db.Column(db.String(400))
    start_date = db.Column(db.DateTime, default=datetime.now())
    end_date = db.Column(db.DateTime, default=datetime.now())
    # ... Create the Comments db.relationship
	# relation to call destination.comments and comment.destination
    reviews = db.relationship('Review', backref='Event')

    
	
    def __repr__(self): #string print method
        return "<Name: {}>".format(self.name)

class Review(db.Model):
    __tablename__ = 'Review'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    date = db.Column(db.DateTime, default=datetime.now())
    #add the foreign keys
    user_name = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('Events.id'))


    def __repr__(self):
        return "<Comment: {}>".format(self.text)

class Booked_Event(db.Model):
    __tablename__ = 'Booked_Event'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now())
    #add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('Events.id'))