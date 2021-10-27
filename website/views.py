from typing import Text
from flask import Blueprint, render_template, request, redirect, url_for, g
from flask_login import current_user
import flask_login
from flask_wtf import file
from werkzeug.utils import secure_filename
from website.models import Event , Review
from . import db
import os
from website.forms import Create, ReviewForm
from .models import *

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    FirstEvent = Event.query.first()
    Carosels = Event.query.filter(Event.id.between(2, 4))
    Events = Event.query.all()
    current = datetime.now()    
    # testing template variable input
    # 1: brunch, 2: bordeaux, 3: graze, 4: dim sum, 5: donut, 6: senses, 7: beer, 8: book, 9: massimo

    return render_template('index.html',
    events=Events,
    carosels=Carosels, current = current, First = FirstEvent)

@bp.route('/create-event', methods = ['GET', 'POST'])
def create():
    createForm = Create()
    if createForm.validate_on_submit():
        #call the function that checks and returns image
        file_path=check_upload_file(createForm)
        event = Event(name = createForm.name.data,organiser = createForm.organiser.data,
        description = createForm.description.data, type = createForm.type.data,
        street = createForm.street.data, city = createForm.city.data, state = createForm.state.data,
        postcode = createForm.postcode.data, image = file_path, start_date = createForm.start_date.data,
        end_date = createForm.end_date.data, long_description = createForm.long_description.data, ticket_price = createForm.ticket_price.data )
        # add the object to the db session
        db.session.add(event)
        # commit to the database
        db.session.commit()
        #Always end with redirect when form is valid
        print("YES")
        return redirect(url_for('main.index'))
    print("no")
    return render_template('create.html', form = createForm)

def check_upload_file(form):
  #get file data from form  
  fp=form.image.data
  filename=fp.filename
  #get the current path of the module file… store image file relative to this path  
  BASE_PATH=os.path.dirname(__file__)
  #upload file location – directory of this file/static/image
  upload_path=os.path.join(BASE_PATH,'static/img',secure_filename(filename))
  #store relative path in DB as image location in HTML is relative
  db_upload_path='/static/img/' + secure_filename(filename)
  #save the file and return the db upload path  
  fp.save(upload_path)
  return db_upload_path

@bp.route('/event-details<id>', methods = ['GET', 'POST'])
def details(id):
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(text = form.Text.data, event_id = id, user_id = current_user.id, user_name = current_user.name)
        db.session.add(review)
        db.session.commit()
    event = Event.query.filter_by(id=id).first()
    Reviews = Review.query.filter_by(event_id = id).all()
    # seed data - will replace with database queries (also needs formatting)
    
    # id, created_at, event_name, event_summary, event_description, event_date, event_time, event_price,
    # event_address, event_map, event_status, resale_platform, event_image, terms_and_conditions, ticket_type
    events = [event.id, event.start_date, event.name, event.description,event.long_description, 
    event.start_date, event.end_date, "$"+str(event.ticket_price), event.street + ","+ event.city + ","+event.state + ","+event.postcode ,
    'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3540.334032852493!2d153.03272421481861!3d-27.458858322815416!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x6b9159f3a25b26d5%3A0x1a8780632f1fcaa5!2sCloudland!5e0!3m2!1sen!2sau!4v1633571197297!5m2!1sen!2sau',
    'Upcoming', '''If you missed out on a ticket, or can no longer make the event, head to Tixel for 
    safe resale. Tixel is the only place where you can buy and sell guaranteed, genuine tickets. 
    Buy, sell or join the waitlist here.''', event.image, 
    '''Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the 
    industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and 
    scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap 
    into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the 
    release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing 
    software like Aldus PageMaker including versions of Lorem Ipsum.''', 'General Admission']


    # id, name, email, mobile

    return render_template('event_details.html',
    heading = "Event Details",
    events = events,
    Reviews = Reviews, form = form)
@bp.route('/booking-history')
def history():
    books = db.session.query(Booked_Event).filter_by(user_id = current_user.id).all()
    event_ids = []
    for book in books:
        event_ids.append(book.event_id)
    events = db.session.query(Event).filter(Event.id.in_(event_ids)).all()
    return render_template('booking_history.html',events = events )

@bp.route('/book<id>')
def book(id):
    book = db.session.query(Booked_Event).filter_by(user_id = current_user.id, event_id = id).first()
    if book:
        return redirect(url_for('main.index'))
    else:
        booked = Booked_Event(event_id = id, user_id = current_user.id)
        db.session.add(booked)
        db.session.commit()
    return redirect(url_for('main.index'))