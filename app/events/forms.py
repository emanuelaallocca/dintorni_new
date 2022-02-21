import wtforms
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateField, IntegerField, FloatField, ValidationError
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


class JoinEventForm(FlaskForm):
    car = SubmitField('Car')
    bus = SubmitField('Bus')
    yourown = SubmitField('Your own')