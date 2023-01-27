from flask import render_template, redirect, request, url_for, flash
from . import auth
from ..models import User
from .. import db
from .forms import LoginForm, NewUserForm, EditUserForm, ChangePasswordForm
from datetime import datetime
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_
import jwt

@auth.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter(or_(User.email==form.handle.data, User.username==form.handle.data)).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash("Väärä käyttäjätunnus tai salasana. Yritä uudelleen.")

    return render_template('auth/login.html', form=form, current_time=datetime.utcnow())

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Sinut on kirjattu ulos")
    return redirect(url_for('main.index'))

@auth.route('/new_user', methods=["GET", "POST"])
def new_user():
    form = NewUserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Uusi käyttäjätili luotu.")
    return render_template('auth/new_user.html', form=form, current_time=datetime.utcnow())


@auth.route('/users')
@login_required
def users():
    page = request.args.get('page', 1, type=int)
    pagination = User.query.paginate(page=page, per_page=20, error_out=False)
    users = pagination.items
    return render_template("users.html", pagination=pagination, users=users, current_time=datetime.utcnow())

@auth.route('/users/<id>', methods=["GET", "POST"])
@login_required
def user(id):
    user = User.query.get_or_404(id)
    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        db.session.add(user)
        db.session.commit()
        flash("Käyttäjätiedot päivitetty onnistuneesti.")
        return redirect(url_for("auth.users"))

    return render_template("user.html", id=id, form=form, current_time=datetime.utcnow())

@auth.route('/change_password', methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash("Salasanasi on päivitetty")
            return redirect('main.index')

    return render_template("auth/change_password.html", form=form, current_time=datetime.utcnow())

@auth.route('/delete_user')
@login_required
def delete_user():
    pass