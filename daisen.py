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
    return render_template("members.html")

@app.route('/members/<id>')
def member(id):
    return render_template("member.html", id=id)

@app.route('/users')
def users():
    return render_template("users.html")

@app.route('/users/<name>')
def user(name):
    return render_template("user.html", id=id)