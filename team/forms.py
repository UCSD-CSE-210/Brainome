from flask_wtf import Form
from wtforms import ValidationError
from wtforms.fields import (BooleanField, PasswordField, StringField,
                            SubmitField)
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, EqualTo, InputRequired, Length
from .user import Role, User

class LoginForm(Form):
    email = EmailField(
        'Email', validators=[InputRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')

class ChangeUserEmailForm(Form):
    email = EmailField(
        'New email', validators=[InputRequired(), Length(1, 64), Email()])
    submit = SubmitField('Update email')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')