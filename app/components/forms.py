from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[Email(message="Email incorrect format")])
    password = StringField("Password: ", validators=[DataRequired(), Length(min=4, max=100)])
    remember = BooleanField("Remember", default=False)
    submit = SubmitField("Login")

class RegistrForm(FlaskForm):
    email = StringField("Email: ", validators=[Email(message="Email incorrect format")])
    password = StringField("Password: ", validators=[DataRequired(), Length(min=4, max=100)])
    submit = SubmitField("Register")