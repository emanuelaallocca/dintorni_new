from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()], render_kw={'placeholder':'Insert a title'})
    content = TextAreaField('Content', validators=[DataRequired()], render_kw={'placeholder':'Insert your review'})
    submit = SubmitField('Post')

