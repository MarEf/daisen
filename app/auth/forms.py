from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class LoginForm(FlaskForm):
    handle = StringField('Sähköpostiosoite tai käyttäjätunnus', validators=[DataRequired(), Length(1,255)])
    password = PasswordField('Salasana', validators=[DataRequired()], id='password')
    show_password = BooleanField('Näytä salasana', id='password_toggle')
    remember_me = BooleanField("Pidä minut kirjautuneena sisään")
    submit = SubmitField("Kirjaudu sisään")

class NewUserForm(FlaskForm):
    username = StringField("Käyttäjätunnus", validators=[DataRequired(), Length(max=255)])
    email = StringField("Sähköpostiosoite", validators=[DataRequired(), Length(max=254), Email()])
    password = PasswordField("Salasana (Vähintään 16 merkkiä)", validators=[DataRequired(), Length(min=16), EqualTo("password2", message="Salasanat eivät ole samat")], id="password")
    password2 = PasswordField("Kirjoita salasana uudelleen", validators=[DataRequired(), Length(min=16)], id="confirm_password")
    show_password = BooleanField("Näytä salasanat", id="password_toggle")
    submit = SubmitField("Luo uusi käyttäjätunnus")

class EditUserForm(FlaskForm):
    username = StringField("Käyttäjätunnus", validators=[DataRequired(), Length(max=255)])
    email = StringField("Sähköpostiosoite", validators=[DataRequired(), Length(max=254), Email()])
    submit = SubmitField("Muokkaa käyttäjätietoja")

class DeleteUserForm(FlaskForm):
    confirm = BooleanField("Olen varma, että haluan poistaa tämän käyttäjätilin ja ymmärrän, ettei sitä voi palauttaa jälkikäteen.", validators=[DataRequired()])
    submit = SubmitField("Poista valittu käyttäjätili")

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Vanha salasana", validators=[DataRequired(), Length(min=16)], id="old_password")
    password = PasswordField("Uusi salasana (Vähintään 16 merkkiä)", validators=[Length(min=16), EqualTo("password2", message="Salasanat eivät ole samat")], id="new_password")
    password2 = PasswordField("Kirjoita uusi salasana uudelleen", validators=[DataRequired(), Length(min=16)], id="confirm_password")
    show_password = BooleanField("Näytä salasanat", id="password_toggle")
    submit = SubmitField("Vaihda salasanaa")

class ForgottenPasswordForm(FlaskForm):
    email = StringField("Sähköpostiosoite, johon salasanan vaihtolinkki lähetetään", validators=[DataRequired(), Length(max=254), Email()])
    submit = SubmitField("Lähetä sähköposti")

class ResetPasswordForm(FlaskForm):
    password = PasswordField("Uusi salasana", validators=[DataRequired(), Length(min=16), EqualTo("password2")], id="password")
    password2 = PasswordField("Kirjoita uusi salasana uudelleen", validators=[DataRequired(), Length(min=16)], id="confirm_password")
    show_password = BooleanField("Näytä salasanat", id="password_toggle")
    submit = SubmitField("Vaihda salasana")