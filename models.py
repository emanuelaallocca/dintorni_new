from datetime import datetime

from flask import current_app
from sqlalchemy.orm import relationship

from app import db, login_manager
from flask_login import UserMixin

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


# logico che fa capire che utente si è loggato
# metto condizione di if per capire chi si sta loggando

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    business = Business.query.get(int(user_id))
    if user != None:
        return User.query.get(int(user_id))
    elif business != None:
        return Business.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    telephone = db.Column(db.Integer(), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    events = relationship("JoinEvent")

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return "User(" + self.username + "," + self.email + "," + self.image_file + ")"


# post class per mettere i post


class Business(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    vat_number = db.Column(db.Integer(), nullable=False)
    telephone = db.Column(db.Integer(), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(30), nullable=False)
    events = db.relationship('Event', backref='creator', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            business_id = s.loads(token)['user_id']
        except:
            return None
        return Business.query.get(business_id)

    def __repr__(self):
        return "Business(" + self.name + "," + self.email + ")"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # unic id
    title = db.Column(db.String(100), nullable=False)  # db string di 20 caratteri
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow())  # default è listante corrente in cui posto
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)  # db integer, è una chiave devo specificare la relazione

    def __repr__(self):
        return "Post(" + self.title + "," + self.date_posted + ")"


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_event = db.Column(db.Date, nullable=False)
    location = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    equipment = db.Column(db.Text, nullable=False)
    min_users = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow())  # default è listante corrente in cui posto
    content = db.Column(db.Text, nullable=False)
    weaknesses = db.Column(db.Text, nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'),
                            nullable=False)  # db integer, è una chiave devo specificare la relazione
    partecipanti = relationship("JoinEvent")

    def __repr__(self):
        return "Event(" + self.title + "," + self.date_event + "," + self.location + "," + self.price + "," + self.equipment + "," + self.min_users + "," + self.date_posted + "," + self.content + "," + self.weaknesses + ")"


class JoinEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    transport_type = db.Column(db.String, nullable=False)
    user = relationship("Event")
    event = relationship("User")

    def __repr__(self):
        return "JoinEvent(" + self.transport_type + ")"
