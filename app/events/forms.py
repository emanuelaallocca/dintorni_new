import wtforms
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, DateField, IntegerField, FloatField, ValidationError, \
    FileField, TimeField
from wtforms.validators import DataRequired, Regexp, ValidationError
from datetime import date, datetime


class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()], render_kw={'placeholder':'Title'})
    date = DateField('Date', validators=[DataRequired()], render_kw={'placeholder':'Date'})
    location = TextAreaField('Location', validators=[DataRequired()], render_kw={'placeholder':'Location'})
    content = TextAreaField('Content', validators=[DataRequired()], render_kw={'placeholder':'Description'})
    price = FloatField('Price', render_kw={'placeholder':'Price'})
    equipment = TextAreaField('Equipment Required', render_kw={'placeholder':'Equipment needed'})
    min_users= IntegerField ('Min Partecipant', render_kw={'placeholder':'Min partecipants'})
    weaknesses = TextAreaField('Weaknesses', render_kw={'placeholder':'Weaknesses'})
    picture1 = FileField('Update Event Image', validators=[FileAllowed(['jpeg', 'png', 'jpg'])])
    picture2 = FileField('Update Event Image', validators=[FileAllowed(['jpeg', 'png', 'jpg'])])
    picture3 = FileField('Update Event Image', validators=[FileAllowed(['jpeg', 'png', 'jpg'])])
    submit = SubmitField('Create')

    def validate_date(self, date):
        if date.data<datetime.today().date():
            raise ValidationError('Date should be grater than today')

class ModifyEventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()], render_kw={'placeholder':'New title'})
    date = DateField('Date', validators=[DataRequired()], render_kw={'placeholder':'New date'})
    location = TextAreaField('Location', validators=[DataRequired()], render_kw={'placeholder':'New location'})
    content = TextAreaField('Content', validators=[DataRequired()], render_kw={'placeholder':'New description'})
    price = FloatField('Price', render_kw={'placeholder':'New price'})
    equipment = TextAreaField('Equipment Required',render_kw={'placeholder':'Equipment'})
    min_users = IntegerField('Min Partecipant', render_kw={'placeholder':'Min partecipants'})
    weaknesses = TextAreaField('Weaknesses', render_kw={'placeholder':'Weaknesses'})
    picture1 = FileField('Update Event Image', validators=[FileAllowed(['jpeg', 'png', 'jpg'])])
    picture2 = FileField('Update Event Image', validators=[FileAllowed(['jpeg', 'png', 'jpg'])])
    picture3 = FileField('Update Event Image', validators=[FileAllowed(['jpeg', 'png', 'jpg'])])
    submit = SubmitField('Update')

    def validate_date(self, date):
        if date.data<datetime.today().date():
            raise ValidationError('Date should be grater than today')

class JoinEventForm(FlaskForm):
    yourcar = SubmitField('Go')
    someonescar = SubmitField('Go')
    bus = SubmitField('Go')
    yourown = SubmitField('Go')

class UseYourCarForm(FlaskForm):
    time_hour = IntegerField('Time of meeting',validators=[DataRequired()], render_kw={'placeholder':'Hour'})
    time_minute = IntegerField('Time of meeting', validators=[DataRequired()], render_kw={'placeholder': 'Minute'})
    place = StringField('Place of the meeting',validators=[DataRequired()], render_kw={'placeholder':'Place'})
    number_of_seats = IntegerField('Number of seats', validators=[DataRequired()], render_kw={'placeholder':'Number of seats'})
    submit = SubmitField('Ready?')

    def validate_number_of_seats(self, number_of_seats):
        if number_of_seats.data > 7 or number_of_seats.data < 0:
            raise ValidationError('The number of seats must be between 0 and 7')

    def validate_time_hour(self, time_hour):
        if time_hour.data > 23 or time_hour.data < 0:
            raise ValidationError('You have to insert the time in the 24h standard')

    def validate_time_minute(self, time_minute):
        if time_minute.data > 59 or time_minute.data < 0:
            raise ValidationError('You have to insert the time in the 24h standard')
