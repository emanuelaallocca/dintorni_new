import wtforms
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, DateField, IntegerField, FloatField, ValidationError, \
    FileField
from wtforms.validators import DataRequired, Regexp, ValidationError
from datetime import date, datetime


class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()], render_kw={'placeholder':'Insert a title'})
    date = DateField('Date', validators=[DataRequired()], render_kw={'placeholder':'Insert the event date'})
    location = TextAreaField('Location', validators=[DataRequired()], render_kw={'placeholder':'Insert the event location'})
    content = TextAreaField('Content', validators=[DataRequired()], render_kw={'placeholder':'Insert the event description'})
    price = FloatField('Price',validators=[DataRequired()], render_kw={'placeholder':'Insert the event price'})
    equipment = TextAreaField('Equipment Required', validators=[DataRequired()], render_kw={'placeholder':'Insert the equipment needed'})
    min_users= IntegerField ('Min Partecipant', validators=[DataRequired()], render_kw={'placeholder':'Insert the minimum amount of partecipants'})
    weaknesses = TextAreaField('Weaknesses', validators=[DataRequired()], render_kw={'placeholder':'Insert the event problematics'})
    submit = SubmitField('Event')

    def validate_date(self, date):
        if date.data<datetime.today().date():
            raise ValidationError('Date should be grater than today')


class ModifyEventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()], render_kw={'placeholder':'Insert a new title'})
    date = DateField('Date', validators=[DataRequired()], render_kw={'placeholder':'Insert the new event date'})
    location = TextAreaField('Location', validators=[DataRequired()], render_kw={'placeholder':'Insert the new event location'})
    content = TextAreaField('Content', validators=[DataRequired()], render_kw={'placeholder':'Insert the new event description'})
    price = FloatField('Price', validators=[DataRequired()], render_kw={'placeholder':'Insert the new event price'})
    equipment = TextAreaField('Equipment Required', validators=[DataRequired()], render_kw={'placeholder':'Insert the new equipment needed'})
    min_users = IntegerField('Min Partecipant', validators=[DataRequired()], render_kw={'placeholder':'Insert the new minimum amount of partecipants'})
    weaknesses = TextAreaField('Weaknesses', validators=[DataRequired()], render_kw={'placeholder':'Insert the event problematics'})
    picture = FileField('Update Event Image', validators=[FileAllowed(['jpeg', 'png', 'jpg'])])
    submit = SubmitField('Update')

    def validate_date(self, date):
        if date.data<datetime.today().date():
            raise ValidationError('Date should be grater than today')

class JoinEventForm(FlaskForm):
    car = SubmitField('Car')
    bus = SubmitField('Bus')
    yourown = SubmitField('Your own')