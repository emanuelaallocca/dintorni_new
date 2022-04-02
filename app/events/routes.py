from flask import render_template, url_for, flash, redirect, request, abort
from sqlalchemy import null

from app import db
from app.events.forms import EventForm, JoinEventForm, ModifyEventForm, UseYourCarForm
from app.events.utils import save_picture
from models import Event, JoinEvent, User
from flask_login import current_user, login_required
from app.events import events
from datetime import date, time, datetime
from PIL import Image

@events.route("/event/new", methods=['GET', 'POST'])
@login_required
def new_event():
    form = EventForm()
    if form.validate_on_submit():
        if form.picture1.data and form.picture2.data==null and form.picture3.data==null:
            picture1 = save_picture(form.picture1.data)
            event = Event(title=form.title.data, date_event=form.date.data,
                      location = form.location.data, price = form.price.data, equipment = form.equipment.data,
                      min_users = form.min_users.data, content=form.content.data, weaknesses = form.weaknesses.data,
                      creator=current_user, image_event1 = picture1)
            db.session.add(event)
            db.session.commit()
            flash('event created', 'success')
            return redirect(url_for('main.home'))
        elif form.picture1.data and form.picture2.data and form.picture3.data==null:
            picture1 = save_picture(form.picture1.data)
            picture2 = save_picture(form.picture2.data)
            event = Event(title=form.title.data, date_event=form.date.data,
                      location = form.location.data, price = form.price.data, equipment = form.equipment.data,
                      min_users = form.min_users.data, content=form.content.data, weaknesses = form.weaknesses.data,
                      creator=current_user, image_event1 = picture1, image_event2 = picture2)
            db.session.add(event)
            db.session.commit()
            flash('event created', 'success')
            return redirect(url_for('main.home'))
        elif form.picture1.data and form.picture2.data and form.picture3.data:
            picture1 = save_picture(form.picture1.data)
            picture2 = save_picture(form.picture2.data)
            picture3 = save_picture(form.picture2.data)
            event = Event(title=form.title.data, date_event=form.date.data,
                      location = form.location.data, price = form.price.data, equipment = form.equipment.data,
                      min_users = form.min_users.data, content=form.content.data, weaknesses = form.weaknesses.data,
                      creator=current_user, image_event1 = picture1, image_event2 = picture2, image_event3 = picture3)
            db.session.add(event)
            db.session.commit()
            flash('event created', 'success')
            return redirect(url_for('main.home'))
        else:
            event = Event(title=form.title.data, date_event=form.date.data,
                          location=form.location.data, price=form.price.data, equipment=form.equipment.data,
                          min_users=form.min_users.data, content=form.content.data, weaknesses=form.weaknesses.data,
                          creator=current_user)
            db.session.add(event)
            db.session.commit()
            flash('event created', 'success')
            return redirect(url_for('main.home'))
    return render_template('create_event.html', title='New Event', form=form, legend='New Event')

@events.route("/event/<int:event_id>", methods=['GET', 'POST'])
def event(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('event.html', title='Event', event=event)

@events.route("/event/<int:event_id>/delete", methods=['POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.creator != current_user:
        abort(403)
    db.session.delete(event)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))

@events.route("/event/<int:event_id>/update", methods=['GET', 'POST'])
@login_required
def update_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.creator!=current_user:
        abort(403) #risposta per forbidden route
    form = ModifyEventForm()
    if form.validate_on_submit():
        if form.picture1.data:
            picture_file1 = save_picture(form.picture1.data)
            event.image_event1 = picture_file1
        if form.picture2.data:
            picture_file2 = save_picture(form.picture2.data)
            event.image_event2 = picture_file2
        if form.picture3.data:
            picture_file3 = save_picture(form.picture3.data)
            event.image_event3 = picture_file3
        event.title=form.title.data
        event.content=form.content.data
        event.date_event = form.date.data
        event.location = form.location.data
        event.price = form.price.data
        event.equipment = form.equipment.data
        event.min_users = form.min_users.data
        event.weaknesses = form.weaknesses.data
        db.session.commit()
        flash('update done', 'success')
        return redirect(url_for('users.events_created', event_id=event_id))
    elif request.method=='GET':
        form.title.data = event.title
        form.content.data = event.content
        form.date.data = event.date_event
        form.location.data = event.location
        form.price.data = event.price
        form.equipment.data = event.equipment
        form.min_users.data = event.min_users
        form.weaknesses.data = event.weaknesses
    form.title.data=event.title
    form.content.data=event.content
    form.date.data = event.date_event
    form.location.data = event.location
    form.price.data = event.price
    form.equipment.data = event.equipment
    form.min_users.data = event.min_users
    form.weaknesses.data = event.weaknesses
    image_event = url_for('static', filename='events_pics/' + event.image_event1)
    return render_template('modify_events.html', title='Update Event', form=form, legend='Update Event', image_event=image_event, event=event)

@events.route("/event/<int:event_id>/joinevent", methods=['GET', 'POST'])
@login_required
def join_event(event_id):
    user= current_user
    user_id = user.id
    form = JoinEventForm()
    if form.validate_on_submit():
        if form.someonescar.data:
            u= current_user.joined
            for e in u:
                if e.event_id == event_id:
                    flash('You have already joined this event', 'unsuccess')
                    return redirect(url_for('main.home'))
            join_event = JoinEvent(event_id=event_id, user_id=user_id, transport_type='someonescar', time=datetime.utcnow(), place='null', number_of_sits=0)
            db.session.add(join_event)
            db.session.commit()
            return redirect(url_for('events.event_joined', event_id=event_id, transport_type='someonescar'))
        elif form.yourcar.data:
                u = current_user.joined
                for e in u:
                    if e.event_id == event_id:
                        flash('You have already joined this event', 'unsuccess')
                        return redirect(url_for('main.home'))
                join_event = JoinEvent(event_id=event_id, user_id=user_id, transport_type='yourcar', time_hour= 0, time_minute= 0, place='null', number_of_sits=0)
                db.session.add(join_event)
                db.session.commit()
                return redirect(url_for('events.your_car_info', event_id=event_id, transport_type='yourcar'))
        elif form.bus.data:
                u = current_user.joined
                for e in u:
                    if e.event_id == event_id:
                        flash('You have already joined this event', 'unsuccess')
                        return redirect(url_for('main.home'))
                join_event = JoinEvent(event_id=event_id, user_id=user_id, transport_type='bus', time_hour= 0, time_minute= 0, place=null, number_of_sits=null)
                db.session.add(join_event)
                db.session.commit()
                return redirect(url_for('events.event_joined', event_id=event_id, transport_type='bus'))
        elif form.yourown.data:
                u = current_user.joined
                for e in u:
                    if e.event_id == event_id:
                        flash('You have already joined this event', 'unsuccess')
                        return redirect(url_for('main.home'))
                join_event = JoinEvent(event_id=event_id, user_id=user_id, transport_type='yourown', time_hour= 0, time_minute= 0, place=null, number_of_sits=null)
                db.session.add(join_event)
                db.session.commit()
                return redirect(url_for('events.event_joined', event_id=event_id, transport_type='yourown'))
    return render_template('join_event.html', title='Join Event', legend='Join Event', form=form)

@events.route("/event/<int:event_id>/<string:transport_type>/event_joined", methods=['GET', 'POST'])
@login_required
def event_joined(event_id, transport_type):
    return render_template('event_joined.html', transport_type = transport_type)

@events.route("/<int:event_id>/business_info", methods=['GET', 'POST'])
def business_info(event_id):
    e = Event.query.get_or_404(event_id)
    return render_template('account_business.html', event = e)

@events.route("/event/<int:event_id>/<string:transport_type>/yourcar_info", methods=['GET', 'POST'])
@login_required
def your_car_info(event_id, transport_type):
    user = current_user
    form = UseYourCarForm()
    if form.validate_on_submit():
        u = current_user.joined
        for e in u:
            if e.event_id == event_id:
                e.time_hour = form.time_hour.data
                e.time_minute = form.time_minute.data
                e.place = form.place.data
                e.number_of_sits = form.number_of_sits.data
                db.session.commit()
                flash('You have update your info', 'success')
                return render_template('your_car_info_lastpage.html')
    return render_template('your_car_info.html', title='Join Event', legend='Join Event', form=form)

@events.route("/event/<int:event_id>/<string:transport_type>/someonescar_info", methods=['GET', 'POST'])
@login_required
def someonescar_info(event_id, transport_type):
    user = current_user
    join_event = JoinEvent.query.filter_by(event_id=event_id)
    id_users_with_car = []
    for j in join_event:
        if j.transport_type == 'yourcar':
            id_users_with_car.append(j.user_id)
    if id_users_with_car.isempty():
        return render_template('no_car.html')
    else:
        users_with_car =[]
        for i in id_users_with_car:
            user = User.get_or_404(id = i)
            users_with_car.append(user)
    return render_template('someonescar.html', users = users_with_car)