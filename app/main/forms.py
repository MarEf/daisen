from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Length, Optional, Regexp

class SignupFormEng(FlaskForm):
    name = StringField('Full name *', validators=[DataRequired(), Length(max=255)])
    city = StringField('Place of residence *', validators=[DataRequired(), Length(max=255)])
    email = StringField('Email *', validators=[DataRequired(), Length(max=254), Email()])
    hyy = BooleanField('HYY member')
    studentNumber = StringField('Student Number', validators=[Length(max=10), Regexp('^[0-9]*$'), Optional()])
    nickname = StringField('Nick (e.g. on IRC or Discord', validators=[Length(max=255), Optional()])
    discovered = TextAreaField('How did you hear about us?', validators=[Length(max=4000), Optional()])
    submit = SubmitField('Join')

class SignupFormFi(FlaskForm):
    name = StringField('Koko nimi *', validators=[DataRequired(), Length(max=255)])
    city = StringField('Asuinkunta *', validators=[DataRequired(), Length(max=255)])
    email = StringField('Sähköposti *', validators=[DataRequired(), Length(max=254), Email()])
    hyy = BooleanField('HYY:n jäsen')
    studentNumber = StringField('Opiskelijanumero', validators=[Length(max=10), Regexp('^[0-9]*$'), Optional()])
    nickname = StringField('Nick (esim. IRC tai Discord', validators=[Length(max=255), Optional()])
    discovered = TextAreaField('Kuinka kuulit meistä?', validators=[Length(max=4000), Optional()])
    submit = SubmitField('Liity')

class EditMemberForm(FlaskForm):
    name = StringField('Koko nimi *', validators=[DataRequired(), Length(max=255)])
    city = StringField('Asuinkunta *', validators=[DataRequired(), Length(max=255)])
    email = StringField('Sähköposti *', validators=[DataRequired(), Length(max=254), Email()])
    hyy = BooleanField('HYY:n jäsen')
    studentNumber = StringField('Opiskelijanumero', validators=[Length(max=10), Regexp('^[0-9]*$'), Optional()])
    nickname = StringField('Nick (esim. IRC tai Discord', validators=[Length(max=255), Optional()])
    discovered = TextAreaField('Kuinka kuulit meistä?', validators=[Length(max=4000), Optional()])
    status = BooleanField('Hyväksy jäsenhakemus')
    submit = SubmitField('Tallenna')
    
class BatchEditForm(FlaskForm):
    actions = SelectField(None, choices=[('accept', 'Hyväksy valitut'),('delete', 'Poista valitut')])
    submit = SubmitField("Suorita toiminto")

class SortForm(FlaskForm):
    keyword = StringField(label='', validators=[Length(max=255)])
    submit = SubmitField("Rajaa jäsenhakemuksia")

# REMOVE IN PROD
class EmailTest(FlaskForm):
    email = StringField("Sähköpostiosoite", validators=[DataRequired(), Length(max=254), Email()])
    submit = SubmitField("Lähetä testiviesti")