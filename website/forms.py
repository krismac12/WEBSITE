from flask_wtf import FlaskForm, form
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields.core import DateTimeField, IntegerField
from wtforms.fields.simple import FileField, PasswordField, TextAreaField
from wtforms.validators import Email, InputRequired, EqualTo, Length
from flask_wtf.file import FileRequired, FileField, FileAllowed
from wtforms.fields.html5 import DateTimeLocalField

ALLOWED_FILE = {'PNG','JPG','png','jpg'}

class Register(FlaskForm): # inherits from FlaskForm
    username = StringField("Username:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired(),EqualTo('confirm_password')])
    confirm_password = PasswordField("Confirm Password:", validators=[InputRequired()])

    email_id = StringField("Email:", validators=[Email()])
    contact_number = StringField("Phone Number:")
    submit = SubmitField("Submit")

class Login(FlaskForm):
    username = StringField("Username:")
    password = PasswordField("Password:")
    submit = SubmitField("Submit")

class Create(FlaskForm):
    name = StringField('Event Name', validators=[InputRequired()])
    description = TextAreaField('Description', 
              validators=[InputRequired()])
    long_description = TextAreaField('Long Description', 
              validators=[InputRequired()])
    organiser  = StringField('Organiser', validators=[InputRequired()])
    type = StringField('Type', validators=[InputRequired()])
    ticket_price = IntegerField('Ticket Price', validators=[InputRequired()])     
    street = StringField('Street', validators=[InputRequired()])     
    city = StringField('City', validators=[InputRequired()])     
    state = StringField('State', validators=[InputRequired()])
    postcode = StringField('Postcode', validators=[InputRequired()])
    start_date = DateTimeLocalField('Start Date/Time', format='%Y-%m-%dT%H:%M', validators=[InputRequired()])
    end_date = DateTimeLocalField('End Date/Time',format='%Y-%m-%dT%H:%M', validators=[InputRequired()])
    image = FileField('Destination Image', validators=[
      FileRequired(message='Image cannot be empty'),
      FileAllowed(ALLOWED_FILE, message='Only supports png,jpg,JPG,PNG')])       
    submit = SubmitField("Save Event")

class Edit(FlaskForm):
    name = StringField('Event Name')
    description = TextAreaField('Description')
    long_description = TextAreaField('Long Description')
    organiser  = StringField('Organiser')
    type = StringField('Type')
    ticket_price = IntegerField('Ticket Price')     
    street = StringField('Street')     
    city = StringField('City')     
    state = StringField('State')
    postcode = StringField('Postcode')
    start_date = DateTimeLocalField('Start Date/Time', format='%Y-%m-%dT%H:%M')
    end_date = DateTimeLocalField('End Date/Time',format='%Y-%m-%dT%H:%M')
    image = FileField('Destination Image', validators=[FileAllowed(ALLOWED_FILE, message='Only supports png,jpg,JPG,PNG')])       
    submit = SubmitField("Save Event")

class ReviewForm(FlaskForm):
    Text = TextAreaField('Review Text', validators=[InputRequired()])
    submit = SubmitField("Post Review")
