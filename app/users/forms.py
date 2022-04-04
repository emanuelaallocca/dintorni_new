from idlelib.configdialog import is_int

from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User, Business, Private
from flask_login import current_user
from flask_wtf import FlaskForm #a validator about what file we can validate

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=5, max=50)], render_kw={'placeholder':'Name'})
    surname = StringField('Surname', validators=[DataRequired(), Length(min=5, max=20)], render_kw={'placeholder':'Surname'})
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)], render_kw={'placeholder':'Username'}) #no empty + condictions
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'placeholder':'Email'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder':'Password'})
    telephone = IntegerField('Telephone Number', validators=[DataRequired()], render_kw={'placeholder':'Telephone'})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')], render_kw={'placeholder':'Confirm password'})
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
        business = Business.query.filter_by(email=email.data).first()
        if user or business:
            raise ValidationError('This email is already taken')


    def validate_telephone(self, telephone):
        s = str(telephone.data)
        u = Private.query.filter_by(telephone=telephone.data).first()
        b = Business.query.filter_by(telephone=telephone.data).first()
        if len(s)!=10:
            raise ValidationError('Your telephone number must have 10 numbers')
        elif u or b :
            raise ValidationError('Control the input: we already have an account with this telephone number')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'placeholder':'Email'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder':'Password'})
    remember = BooleanField('Remember Me') #boolean --> cookie
    submit = SubmitField('Login')

class UpdateAccountBusinessForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=5, max=20)], render_kw={'placeholder':'Name'})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'placeholder':'Email'})
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpeg','png','jpg'])])
    vat_number = IntegerField('Vat Number', validators=[DataRequired()], render_kw={'placeholder':'Vat number'})  # rimettere i nullable
    telephone = IntegerField('Telephone', validators=[DataRequired()], render_kw={'placeholder':'Telephone'})
    city = StringField('City', validators=[DataRequired()], render_kw={'placeholder':'City'})
    address = StringField('Address', validators=[DataRequired()], render_kw={'placeholder':'Address'})
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

    def validate_vat_number(self, vat_number):
        if vat_number.data != current_user.vat_number:
            s = str(vat_number.data)
            if len(s) != 11:
                raise ValidationError('You must insert a correct VAT NUMBER')

    def validate_address(self, address):
        if address.data != current_user.address:
            s = address.data.lower()
            s = address.data.strip()
            s = s.split()
            info = len(s)
            if (s[0] != 'corso' and s[0] != 'piazza' and s[0] != 'via' and s[0] != 'viale'):
                raise ValidationError('You must insert a correct address')
            if is_int(s[info - 1]) != True:
                raise ValidationError('You must insert a correct address')

    def validate_telephone(self, telephone):
        if telephone.data != current_user.telephone:
            s = str(telephone.data)
            u = Private.query.filter_by(telephone=telephone.data).first()
            b = Business.query.filter_by(telephone=telephone.data).first()
            if len(s) != 10:
                raise ValidationError('Your telephone number must have 10 numbers')
            elif u or b:
                raise ValidationError('Control the input: we already have an account with this telephone number')

class UpdateAccountForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=5, max=20)], render_kw={'placeholder':'Name'})
    surname = StringField('Surname', validators=[DataRequired(), Length(min=5, max=20)], render_kw={'placeholder':'Surname'})
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)], render_kw={'placeholder':'Username'})
    telephone = IntegerField('Telephone Number', validators=[DataRequired()], render_kw={'placeholder':'Telephone'})#no empty + condictions
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'placeholder':'Email'})
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

    def validate_telephone(self, telephone):
        if telephone.data != current_user.telephone:
            s = str(telephone.data)
            u = Private.query.filter_by(telephone=telephone.data).first()
            b = Business.query.filter_by(telephone=telephone.data).first()
            if len(s) != 10:
                raise ValidationError('Your telephone number must have 10 numbers')
            elif u or b:
                raise ValidationError('Control the input: we already have an account with this telephone number')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'placeholder':'Email'})
    submit = SubmitField('Request Password Reset') #button per fare il submit
    def validate_email(self, email):
        #guardo se è nel db --> cerco l'user attraverso la mail questa volta
        user = User.query.filter_by(email=email.data).first()
        if user is None:
             raise ValidationError('there is not an account')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder':'Password'})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')], render_kw={'placeholder':'Confirm password'})
    submit = SubmitField('Reset password')

class RegistrationBusinessForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)], render_kw={'placeholder':'Name'}) #no empty + condictions
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'placeholder':'Email'})
    vat_number = IntegerField('VAT Number', validators=[DataRequired()], render_kw={'placeholder':'Vat number'})
    telephone = IntegerField('Telephone Number', validators=[DataRequired()], render_kw={'placeholder':'Telephone'})
    city = StringField('City', validators=[DataRequired()], render_kw={'placeholder':'City'})
    address = StringField('Address', validators=[DataRequired()], render_kw={'placeholder':'Address'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder':'Password'})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')], render_kw={'placeholder':'Confirm password'})
    #term_conditions = BooleanField('Terms and conditions', validators=[DataRequired()])
    submit = SubmitField('SignUp')
    #creo una funzione per questa classe

    def validate_name(self, name):
        business = Business.query.filter_by(name=name.data).first()
        if business:
            raise ValidationError('This username is already taken')

    def validate_email(self, email):
        business = Business.query.filter_by(email=email.data).first()
        user = Private.query.filter_by(email=email.data).first()
        if business or user:
            raise ValidationError('This email is already taken')

    def validate_vat_number(self, vat_number):
        s = str(vat_number.data)
        if len(s)!=11:
            raise ValidationError('You must insert a correct VAT NUMBER')

    def validate_address(self, address):
        s = address.data.lower()
        s = address.data.strip()
        s = s.split()
        info = len(s)
        if (s[0]!='corso' and s[0]!='piazza' and s[0]!='via' and s[0]!='viale'):
            raise ValidationError('You must insert a correct address')
        if is_int(s[info-1])!=True:
            raise ValidationError('You must insert a correct address')

    def validate_telephone(self, telephone):
        s = str(telephone.data)
        u = Private.query.filter_by(telephone=telephone.data).first()
        b = Business.query.filter_by(telephone=telephone.data).first()
        if len(s)!=10:
            raise ValidationError('Your telephone number must have 10 numbers')
        elif u or b :
            raise ValidationError('Control the input: we already have an account with this telephone number')

    #def validate_terms(self, term_conditions):
        #if term_conditions.data!=True:
            #raise ValidationError('You have to accept terms and conditions')
