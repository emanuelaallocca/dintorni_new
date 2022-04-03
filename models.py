from datetime import datetime
from flask import current_app
from sqlalchemy.orm import relationship
from app import db, login_manager
from flask_login import UserMixin
from sqlalchemy.orm import class_mapper
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# logico che fa capire che utente si è loggato
# metto condizione di if per capire chi si sta loggando

@login_manager.user_loader
def load_user(email):
    user = User.query.get(email)
    return user


class User(db.Model, UserMixin):
    _tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    telephone = db.Column(db.Integer(), nullable=False)
    type= db.Column(db.String(20))

    __mapper_args__={
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }
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

class Private(User, db.Model):
    _tablename__ = 'private'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    username = db.Column(db.String(20), unique=True, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    joined = db.relationship("JoinEvent", backref = 'joined')

    __mapper_args__ = {
        'polymorphic_identity': 'private',
    }

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

class Business(User, db.Model):
    _tablename__ = 'business'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    vat_number = db.Column(db.Integer())#rimettere i nullable
    city = db.Column(db.String(20))
    address = db.Column(db.String(30))
    events = db.relationship('Event', backref='creator', lazy=True)
    link_facebook = db.Column(db.String())
    link_instagram = db.Column(db.String())
    link_twitter = db.Column(db.String())
    link_website = db.Column(db.String())

    __mapper_args__ = {
        'polymorphic_identity': 'business',
    }

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
    #event_title = db.Column(db.String, nullable=False)
    def __repr__(self):
        return "Post(" + self.title + "," + self.date_posted + ")"

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_event = db.Column(db.Date, nullable=False)
    location = db.Column(db.Text, default='eccolo', nullable=False)
    price = db.Column(db.Float, default=1, nullable = True)
    equipment = db.Column(db.Text, default='eccolo', nullable=True)
    min_users = db.Column(db.Integer, default=2, nullable=True)
    date_posted = db.Column(db.DateTime,
                            default=datetime.utcnow())  # default è listante corrente in cui posto
    content = db.Column(db.Text, default='eccolo', nullable=False)
    weaknesses = db.Column(db.Text, default='eccolo', nullable=True)
    image_event1 = db.Column(db.String(20), nullable=False, default='default.jpg')
    image_event2 = db.Column(db.String(20), nullable=False, default='default.jpg')
    image_event3 = db.Column(db.String(20), nullable=False, default='default.jpg')
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'))  # db integer, è una chiave devo specificare la relazi

    def __repr__(self):
        return "Event(" + self.title +str(self.date_posted) +")"

class JoinEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    transport_type = db.Column(db.String, nullable=False)
    time_hour = db.Column(db.Integer, nullable=False, default=0)
    time_minute = db.Column(db.Integer, nullable=False, default=0)
    place = db.Column (db.String, nullable=False, default='null')
    number_of_sits = db.Column(db.Integer, nullable=False, default=0)
    user = db.relationship("Event")
    event = db.relationship("User")

    def __repr__(self):
        return "JoinEvent(" + self.transport_type + ")"

