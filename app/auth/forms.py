from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class LoginForm(FlaskForm):
    email = StringField('Sähköpostiosoite', validators=[DataRequired(), Length(1,254), Email])
    password = PasswordField('Salasana', validators=[DataRequired()], id='password')
    show_password = BooleanField('Näytä salasana', id='password_toggle')
    remember_me = BooleanField("Pidä minut kirjautuneena sisään")
    submit = SubmitField("Kirjaudu sisään")