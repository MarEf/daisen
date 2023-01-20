import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from flask import Flask, render_template, flash, redirect, url_for

from flask_migrate import Migrate, upgrade

from app import create_app, db
from app.models import User, Member

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


from app.main.forms import SignupFormEng, SignupFormFi

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

@app.route('/join', methods=['GET', 'POST'])
def join():
    form = SignupFormEng()
    if form.validate_on_submit():
        member = Member(name=form.name.data, city=form.city.data, email=form.email.data, hyy=form.hyy.data, studentNumber=form.studentNumber.data, nickname=form.nickname.data, discovered=form.discovered.data)
        db.session.add(member)
        db.session.commit()
        flash('Welcome to YAMA!')
        return redirect('/join')
    return render_template('signup.html', form=form, lang='en')

@app.route('/liity', methods=['GET', 'POST'])
def liity():
    form = SignupFormFi()
    if form.validate_on_submit():
        member = Member(name=form.name.data, city=form.city.data, email=form.email.data, hyy=form.hyy.data, studentNumber=form.studentNumber.data, nickname=form.nickname.data, discovered=form.discovered.data)
        db.session.add(member)
        db.session.commit()
        flash('Tervetuloa YAMAan!')
        return redirect('/join')
    return render_template('signup.html', form=form, lang='fi')