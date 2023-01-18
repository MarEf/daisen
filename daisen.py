from flask import Flask, render_template
from flask_moment import Moment
from datetime import datetime
from flask_bootstrap import Bootstrap

app = Flask(__name__, template_folder="app/templates", static_folder="app/static")
moment = Moment(app)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template("index.html", current_time=datetime.utcnow())


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