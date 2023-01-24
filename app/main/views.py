
from ..models import User, Member
from flask import render_template, flash, redirect, url_for, request
from .forms import SignupFormEng, SignupFormFi, EditMemberForm
from . import main
from flask_login import login_required

from .. import db


@main.route('/')
def index():
    return render_template("index.html")

@main.route('/members')
def members():
    page = request.args.get('page', 1, type=int)
    pagination = Member.query.paginate(page=page, per_page=20, error_out=False)
    members = pagination.items
    return render_template("members.html", members=members, pagination=pagination)

@main.route('/members/<int:id>', methods=['GET', 'POST'])
def member(id):
    # IF USER NOT LOGGED IN, ABORT
    member = Member.query.get_or_404(id)
    form = EditMemberForm(obj=member)

    if form.validate_on_submit():
        member.name = form.name.data
        member.city = form.city.data
        member.email = form.email.data
        member.hyy = form.hyy.data
        member.studentNumber = form.studentNumber.data
        member.nickname = form.nickname.data
        member.discovered = form.discovered.data
        member.status = form.status.data

        db.session.add(member)
        db.session.commit()
        flash("Jäsentiedot päivitetty onnistuneesti:<br><br>"+member.email)
        return redirect(url_for("members"))

    return render_template("member.html", form=form, member=[member])

@main.route('/users')
def users():
    return render_template("users.html")

@main.route('/users/<name>')
def user(name):
    return render_template("user.html", id=id)

@main.route('/join', methods=['GET', 'POST'])
def join():
    form = SignupFormEng()
    if form.validate_on_submit():
        member = Member(name=form.name.data, city=form.city.data, email=form.email.data, hyy=form.hyy.data, studentNumber=form.studentNumber.data, nickname=form.nickname.data, discovered=form.discovered.data)
        db.session.add(member)
        db.session.commit()
        flash('Welcome to YAMA!')
        return redirect('/join')
    return render_template('signup.html', form=form, lang='en')

@main.route('/liity', methods=['GET', 'POST'])
def liity():
    form = SignupFormFi()
    if form.validate_on_submit():
        member = Member(name=form.name.data, city=form.city.data, email=form.email.data, hyy=form.hyy.data, studentNumber=form.studentNumber.data, nickname=form.nickname.data, discovered=form.discovered.data)
        db.session.add(member)
        db.session.commit()
        flash('Tervetuloa YAMAan!')
        return redirect('/join')
    return render_template('signup.html', form=form, lang='fi')

@main.route('/kirjautumistesti')
@login_required
def secret():
    return "Kirjaudu sisään!"