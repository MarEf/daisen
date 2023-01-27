
from ..models import User, Member
from flask import render_template, flash, redirect, url_for, request
from .forms import SignupFormEng, SignupFormFi, EditMemberForm, BatchEditForm, SortForm
from wtforms import BooleanField
from . import main
from flask_login import login_required
from datetime import datetime
from sqlalchemy import or_

# Poista valmiista ohjelmistosta
from .forms import EmailTest

from .. import db, email


@main.route('/')
def index():
    return render_template("index.html", current_time=datetime.utcnow())

@main.route('/members', methods=['GET', 'POST'])
@login_required
def members():
    class Edit(BatchEditForm):
        pass

    page = request.args.get('page', 1, type=int)
    pagination = Member.query.order_by(Member.status, Member.applicationDate.desc()).paginate(page=page, per_page=20, error_out=False)
    members = pagination.items

    # Luodaan hallinnointilomake dynaamisesti
    for member in members:
        setattr(Edit, "member_"+str(member.id), BooleanField(None))
    
    batchEdit = Edit()

    sortForm = SortForm()

    if sortForm.validate_on_submit() and sortForm.keyword.data:
        keyword = '%'+sortForm.keyword.data+'%'
        page = request.args.get('page', 1, type=int)
        pagination = Member.query.filter(or_(Member.name.like(keyword), Member.email.like(keyword))).order_by(Member.status, Member.applicationDate.desc()).paginate(page=page, per_page=20, error_out=False)
        members = pagination.items

    elif batchEdit.is_submitted() and batchEdit.actions.data:
        message = ""
        
        if (batchEdit.actions.data == "delete"):
            message = message+"Valitut jäsenhakemukset on poistettu järjestelmästä pysyvästi: <br><br>"
            for member in members:
                if (batchEdit['member_'+str(member.id)].data == True):
                    message = message+member.email+"<br>"
                    db.session.delete(member)
        elif (batchEdit.actions.data == "accept"):
            message = message+"Valitut jäsenhakemukset on hyväksytty:<br><br>"
            for member in members:
                if (batchEdit['member_'+str(member.id)].data == True):
                    member.status = True
                    message = message+member.email+"<br>"
        
        flash(message)
        db.session.commit()

        return redirect("/members")
    return render_template("members.html", members=members, pagination=pagination, batchEdit=batchEdit, sortForm=sortForm, current_time=datetime.utcnow())

@main.route('/members/<int:id>', methods=['GET', 'POST'])
@login_required
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
        return redirect(url_for("main.members"))

    return render_template("member.html", form=form, member=[member], current_time=datetime.utcnow())

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
    return render_template('signup.html', form=form, lang='fi', current_time=datetime.utcnow())


#Testireittejä. REMOVE IN PROD

@main.route('/kirjautumistesti')
@login_required
def secret():
    return "Kirjaudu sisään!"

@main.route("/email_test", methods=["GET", "POST"])
def email_test():
    form = EmailTest()
    if form.validate_on_submit():
        email.send_email(form.email.data, "Testiviesti", "mail")
        flash('Viesti lähetetty')
        return redirect('/email_test')
    return render_template("email_test.html", form=form, current_time=datetime.utcnow())