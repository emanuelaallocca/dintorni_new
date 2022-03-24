import wtforms
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, DateField, IntegerField, FloatField, ValidationError, \
    FileField
from wtforms.validators import DataRequired, Regexp, ValidationError
from datetime import date, datetime


class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()], render_kw={'placeholder':'Title'})
    date = DateField('Date', validators=[DataRequired()], render_kw={'placeholder':'Date'})
    location = TextAreaField('Location', validators=[DataRequired()], render_kw={'placeholder':'Location'})
    content = TextAreaField('Content', validators=[DataRequired()], render_kw={'placeholder':'Description'})
    price = FloatField('Price',validators=[DataRequired()], render_kw={'placeholder':'Price'})
    equipment = TextAreaField('Equipment Required', validators=[DataRequired()], render_kw={'placeholder':'Equipment needed'})
    min_users= IntegerField ('Min Partecipant', validators=[DataRequired()], render_kw={'placeholder':'Min partecipants'})
    weaknesses = TextAreaField('Weaknesses', validators=[DataRequired()], render_kw={'placeholder':'Weaknesses'})
    submit = SubmitField('Event')

    def validate_date(self, date):
        if date.data<datetime.today().date():
            raise ValidationError('Date should be grater than today')


class ModifyEventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()], render_kw={'placeholder':'New title'})
    date = DateField('Date', validators=[DataRequired()], render_kw={'placeholder':'New date'})
    location = TextAreaField('Location', validators=[DataRequired()], render_kw={'placeholder':'New location'})
    content = TextAreaField('Content', validators=[DataRequired()], render_kw={'placeholder':'New description'})
    price = FloatField('Price', validators=[DataRequired()], render_kw={'placeholder':'New price'})
    equipment = TextAreaField('Equipment Required', validators=[DataRequired()], render_kw={'placeholder':'Equipment'})
    min_users = IntegerField('Min Partecipant', validators=[DataRequired()], render_kw={'placeholder':'Min partecipants'})
    weaknesses = TextAreaField('Weaknesses', validators=[DataRequired()], render_kw={'placeholder':'Weaknesses'})
    picture = FileField('Update Event Image', validators=[FileAllowed(['jpeg', 'png', 'jpg'])])
    submit = SubmitField('Update')

    def validate_date(self, date):
        if date.data<datetime.today().date():
            raise ValidationError('Date should be grater than today')

class JoinEventForm(FlaskForm):
    car = SubmitField('Car')
    bus = SubmitField('Bus')
    yourown = SubmitField('Your own')