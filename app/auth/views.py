from flask import render_template
from . import auth
from ..models import User
from .forms import LoginForm

@auth.route('/login')
def login():
    form = LoginForm()

    return render_template('auth/login.html', form=form)