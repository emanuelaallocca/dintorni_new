from flask import render_template, url_for, flash, redirect, request, abort
from app import db
from app.events.forms import EventForm, JoinEventForm, ModifyEventForm
from app.events.utils import save_picture
from models import Event, JoinEvent
from flask_login import current_user, login_required
from app.events import events
from datetime import date
from PIL import Image

@events.route("/event/new", methods=['GET', 'POST'])
@login_required
def new_event():
    form = EventForm()
    if form.validate_on_submit():
         event = Event(title=form.title.data, date_event=form.date.data,
                      location = form.location.data, price = form.price.data, equipment = form.equipment.data,
                      min_users = form.min_users.data, content=form.content.data, weaknesses = form.weaknesses.data,
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
    if event.author != current_user:
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
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            event.image_event = picture_file
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
    image_event = url_for('static', filename='events_pics/' + event.image_event)
    return render_template('modify_events.html', title='Update Event', form=form, legend='Update Event', event=event)



@events.route("/event/<int:event_id>/joinevent", methods=['GET', 'POST'])
@login_required
def join_event(event_id):
    user= current_user
    user_id = user.id
    form = JoinEventForm()
    if form.validate_on_submit():
        if form.car.data:
            join_event = JoinEvent(event_id=event_id, user_id=user_id, transport_type = 'car')
            db.session.add(join_event)
            db.session.commit()
            flash('event joined', 'success')
            return redirect(url_for('main.home'))
        elif form.bus.data:
            join_event = JoinEvent(event_id=event_id, user_id=user_id, transport_type='bus')
            db.session.add(join_event)
            db.session.commit()
            flash('event joined', 'success')
            return redirect(url_for('main.home'))
        elif form.yourown.data:
            join_event = JoinEvent(event_id=event_id, user_id=user_id, transport_type='your own')
            db.session.add(join_event)
            db.session.commit()
            flash('event joined', 'success')
            return redirect(url_for('main.home'))
    return render_template('join_event.html', title='Join Event', legend='Join Event', form=form)
