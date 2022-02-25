from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User, Business, Private
from flask_login import current_user
from flask_wtf import FlaskForm #a validator about what file we can validate

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=5, max=50)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=5, max=20)])
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)]) #no empty + condictions
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    telephone = IntegerField('Telephone Number', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('SignUp')
    #creo una funzione per questa classe

    def validate_username(self, username):
        #guardo se è nel db
        user = Private.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already taken')

    def validate_email(self, email):
        #guardo se è nel db --> cerco l'user attraverso la mail questa volta
        user = Private.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already taken')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me') #boolean --> cookie
    submit = SubmitField('Login')

class UpdateAccountBusinessForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpeg','png','jpg'])])
    vat_number = IntegerField('Vat Number', validators=[DataRequired()])  # rimettere i nullable
    telephone = IntegerField('Telephone', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Update')
    def validate_name(self, name):
        if name.data != current_user.name:
          business = Business.query.filter_by(name = name.data).first()
          if business:
             raise ValidationError('This username is already taken')

    def validate_email(self, email):
        if email.data != current_user.email:
          business = Business.query.filter_by(email=email.data).first()
          user = Private.query.filter_by(email=email.data).first()
          if business or user:
             raise ValidationError('This email is already taken')

class UpdateAccountForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=5, max=20)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=5, max=20)])
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
    telephone = IntegerField('Telephone Number', validators=[DataRequired()])#no empty + condictions
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpeg','png','jpg'])])
    submit = SubmitField('Update')
    #creo una funzione per questa classe
    #username and email sono gli stessi, perche devono rimanere validi

    def validate_username(self, username):
        if username.data != current_user.username:
          user = Private.query.filter_by(username=username.data).first()
          if user:
             raise ValidationError('This username is already taken')

    def validate_email(self, email):
        if email.data != current_user.email:
          business = Business.query.filter_by(email=email.data).first()
          user = Private.query.filter_by(email=email.data).first()
          if user or business:
             raise ValidationError('This email is already taken')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset') #button per fare il submit
    def validate_email(self, email):
        #guardo se è nel db --> cerco l'user attraverso la mail questa volta
        user = User.query.filter_by(email=email.data).first()
        if user is None:
             raise ValidationError('there is not an account')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset password')
####################BUSINESS############

class RegistrationBusinessForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)]) #no empty + condictions
    email = StringField('Email', validators=[DataRequired(), Email()])
    vat_number = IntegerField('VAT Number', validators=[DataRequired()])
    telephone = IntegerField('Telephone Number', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('SignUp')
    #creo una funzione per questa classe

    def validate_username(self, username):
        #guardo se è nel db
        user = Business.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already taken')

    def validate_email(self, email):
        #guardo se è nel db --> cerco l'user attraverso la mail questa volta
        user = Business.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already taken')