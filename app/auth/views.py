from flask import render_template, redirect, request, url_for, flash, current_app
from . import auth
from ..models import User
from .. import db
from .forms import LoginForm, NewUserForm, EditUserForm, ChangePasswordForm, ForgottenPasswordForm, ResetPasswordForm, DeleteUserForm
from datetime import datetime
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_
from .. import db, email

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
        return redirect(url_for("auth.new_user"))
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
            return redirect(url_for('main.index'))
        else:
            flash("Salasanan vaihto ei onnistunut. Tarkista, että vanha salasana on kirjoitettu oikein ja yritä uudelleen.")

    return render_template("auth/change_password.html", form=form, current_time=datetime.utcnow())

@auth.route('/forgotten_password', methods=["GET", "POST"])
def forgotten_password():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = ForgottenPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None:
            # Generoidaan palautuslinkki
            token = user.generate_reset_token()

            # Lähetetään sähköposti
            email.send_email(form.email.data, "Salasanan palautus", "forgot_password", user=user, token=token)
            
        # Vahvistusviesti annetaan aina, slloinkin kun käyttäjää ei ole, ettei  mahdollinen hyökkääjä voi lähteä
        # suodattamaan järjestelmässä olevia sähköpostiosoitteita palautuslomakkeen avulla.
        flash("Salasanan palautuslinkki on lähetetty antamaasi sähköpostiosoitteeseen. Seuraa sen sisältämiä ohjeita.")
        return redirect(url_for("auth.forgotten_password"))
    return render_template("auth/forgotten_password.html", form=form, current_time=datetime.utcnow())

@auth.route('/reset_password/<token>', methods=["GET", "POST"])
def reset_password(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))

    form = ResetPasswordForm()
    
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash("Salasanasi on vaihdettu onnistuneesti. Voit nyt kirjautua sisään uudella salasanalla.")
            return redirect(url_for('auth.login'))
        else:
            flash("Käyttämäsi salasanan palautuslinkki on joko virheellinen tai vanhentunut. Pyydä uutta linkkiä ja yritä uudelleen.")
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form, current_time=datetime.utcnow())

@auth.route('/delete_user/<id>', methods=["GET", "POST"])
@login_required
def delete_user(id):
    if User.query.count() == 1:
        flash("Et voi poistaa järjestelmän ainoaa käyttäjätiliä.")
        return redirect(url_for('auth.users'))
    
    form = DeleteUserForm()
    user = User.query.get(id)

    if user is not None:
        if form.validate_on_submit():
            username = user.username
            db.session.delete(user)
            db.session.commit()
            flash("Käyttäjätili "+username+" on poistettu järjestelmästä.")
            return redirect(url_for('auth.users'))
    else:
        flash("En tiedä, miten onnistuit tässä, mutta käyttäjää, jota yrität poistaa ei ole olemassa.")
        return redirect(url_for('auth.users'))

    return render_template('auth/delete_user.html', form=form, user=user, current_time=datetime.utcnow())