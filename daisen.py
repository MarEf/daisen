import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from flask import Flask, render_template

from flask_migrate import Migrate, upgrade

from app import create_app, db
from app.models import User, Member

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.cli.command()
def deploy():
    upgrade()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/members')
def members():
    return '<h1>Tälle sivulle tulee sivutettu näkymä kaikista jäsenhakemuksista</h1>'

@app.route('/members/<id>')
def member(id):
    return '<h1>Tälle sivulle tulee yksittäisen hakemuksen tiedot muokkauslomakkeella</h1>'

@app.route('/users')
def users():
    return '<h1>Tänne tulee näkymä kaikista käyttäjistä</h1>'

@app.route('/users/<name>')
def user(name):
    return '<h1>Tänne tulee yksittäisen käyttäjän tietojen muokkaussivu</h1>'