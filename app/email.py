from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail
import os

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    print(os.environ.get('MAIL_USERNAME'))
    app = current_app._get_current_object()
    msg = Message("Test email", sender="   daisen@test.com", recipients=[to])
    msg.subject = subject
    msg.body = render_template("mail/"+template+'.txt', **kwargs)
    msg.html = render_template("mail/"+template+'.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr