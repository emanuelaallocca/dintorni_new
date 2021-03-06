from datetime import datetime

from flask import render_template, url_for, flash, redirect, request

from app import bcrypt, db
from app.users.forms import RegistrationForm, RegistrationBusinessForm, LoginForm, UpdateAccountForm, RequestResetForm, \
    ResetPasswordForm, UpdateAccountBusinessForm
from app.users.utils import save_picture
from models import User, Post, Business, Event, JoinEvent, Private
from flask_login import login_user, current_user, logout_user, login_required
from app.users import users

from PIL import Image #- non so perche non vada min 38.18 lezione 7

@users.route("/registration", methods=['GET', 'POST'])
def general():
 return render_template('registration.html', title='Registration')

@users.route("/<usertype>/registration", methods=['GET', 'POST'])
def registration(usertype):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    if usertype == 'private':
        form = RegistrationForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            # create a new user
            user = Private(name = form.name.data, surname = form.surname.data, username=form.username.data, email=form.email.data, telephone=form.telephone.data,
                        password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('your account has been created! now you can login', 'success')
            return redirect(url_for('users.login'))
        return render_template('registration_user.html', title='Registration User', form=form)

    elif usertype == 'business':
        form = RegistrationBusinessForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            # create a new user
            business = Business(name=form.name.data, email=form.email.data, vat_number=form.vat_number.data,
                                telephone=form.telephone.data, city=form.city.data, address=form.address.data,
                                password=hashed_password )
            db.session.add(business)
            db.session.commit()
            flash('your account has been created! now you can loging', 'success')
            return redirect(url_for('users.login'))
        return render_template('registration_business.html', title='Registration Business', form=form)

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form= UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.name = form.name.data
        current_user.surname = form.surname.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.telephone = form.telephone.data
        db.session.commit()
        flash('your account has been updated', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.surname.data = current_user.surname
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.telephone.data = current_user.telephone
    image_file = url_for('static', filename='profile_pics/'+current_user.image_file)
    return render_template('update_account_user.html', title='Account',image_file=image_file, form=form)

@users.route("/account_business", methods=['GET', 'POST'])
@login_required
def account_business():
    form= UpdateAccountBusinessForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.vat_number = form.vat_number.data
        current_user.telephone = form.telephone.data
        current_user.city = form.city.data
        current_user.address = form.address.data
        db.session.commit()
        flash('your account has been updated', 'success')
        return redirect(url_for('users.account_business'))
    elif request.method == 'GET':
            form.name.data = current_user.name
            form.email.data = current_user.email
            form.vat_number.data = current_user.vat_number
            form.telephone.data = current_user.telephone
            form.city.data = current_user.city
            form.address.data = current_user.address

    image_file = url_for('static', filename='profile_pics/'+current_user.image_file)#devo mettere la cartella+la route
    return render_template('update_account_business.html', title='Account Business',image_file=image_file, form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = Private.query.filter_by(email=form.email.data).first()
        business = Business.query.filter_by(email=form.email.data).first()
        if user != None:
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('main.home'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
        elif business!=None:
            if business and bcrypt.check_password_hash(business.password, form.password.data):
                login_user(business, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('main.home'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/user/events_joined")
@login_required
def user_events():
    page = request.args.get('page', 1, type=int)
    jevents = JoinEvent.query.filter_by(user_id= current_user.id).all()
    events = []
    for e in jevents:
        ev = Event.query.filter_by(id = e.event_id).first()
        if ev:
            if ev.date_event > datetime.today().date():
                events.append(ev)
    events_already_done = []
    for e in jevents:
        ev = Event.query.filter_by(id=e.event_id).first()
        if ev:
            if ev.date_event < datetime.today().date():
                events_already_done.append(ev)
    return render_template('user_events.html', user=current_user, events = events, e_tot = len(events),
                           ea_tot = len(events_already_done), events_already_done=events_already_done)

@users.route("/eventscreated")
@login_required
def events_created():
    page = request.args.get('page', 1, type=int)
    business = Business.query.filter_by(name=current_user.name).first_or_404()
    events = Event.query.filter_by(creator=business).order_by(Event.date_posted.desc()).paginate(page=page, per_page=9)
    return render_template('events_created.html', events=events, business=business)

@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = Private.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)

@users.route("/<string:name>")
def business_events(name):
    page = request.args.get('page', 1, type=int)
    business = Business.query.filter_by(name=name).first_or_404()
    events = Event.query.filter_by(creator=business).order_by(Event.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('business_events.html', events=events, business=business)

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    form = RequestResetForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):

    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        user.password = hashed_password
        db.session.commit()
        flash('your psw has been updated! now you can loging', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

