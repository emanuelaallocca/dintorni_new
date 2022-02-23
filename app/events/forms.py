import wtforms
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, DateField, IntegerField, FloatField, ValidationError, \
    FileField
from wtforms.validators import DataRequired, Regexp, ValidationError
from datetime import date


class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    location = TextAreaField('Location', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    price = FloatField('Price',validators=[DataRequired()])
    equipment = TextAreaField('Equipment Required', validators=[DataRequired()])
    min_users= IntegerField ('Min Partecipant', validators=[DataRequired()])
    weaknesses = TextAreaField('Weaknesses', validators=[DataRequired()])
    submit = SubmitField('Event')
    def correct_date(self):
        if date.year<date.today().year:
            raise EventForm.ValidationError('date should be grater than today')

class ModifyEventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    location = TextAreaField('Location', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    equipment = TextAreaField('Equipment Required', validators=[DataRequired()])
    min_users = IntegerField('Min Partecipant', validators=[DataRequired()])
    weaknesses = TextAreaField('Weaknesses', validators=[DataRequired()])
    picture = FileField('Update Event Image', validators=[FileAllowed(['jpeg', 'png', 'jpg'])])
    submit = SubmitField('Update')

class JoinEventForm(FlaskForm):
    car = SubmitField('Car')
    bus = SubmitField('Bus')
    yourown = SubmitField('Your own')