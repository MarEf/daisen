from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Daisen - Jäsenhakemusten hallintajärjestelmä</h1>'


@app.route('/member')
def members():
    return '<h1>Tälle sivulle tulee sivutettu näkymä kaikista jäsenhakemuksista</h1>'

@app.route('/member/<id>')
def member(id):
    return '<h1>Tälle sivulle tulee yksittäisen hakemuksen tiedot muokkauslomakkeella</h1>'

@app.route('/user')
def users():
    return '<h1>Tänne tulee näkymä kaikista käyttäjistä</h1>'

@app.route('/user/<name>')
def user(name):
    return '<h1>Tänne tulee yksittäisen käyttäjän tietojen muokkaussivu</h1>'