from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateField, IntegerField, FloatField
from wtforms.validators import DataRequired


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

class JoinEventForm(FlaskForm):
    car = SubmitField('Car')
    bus = SubmitField('Bus')
    yourown = SubmitField('Your own')