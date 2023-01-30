from flask import current_app, request, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from . import db
import jwt

class Member(db.Model):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(254), index=True, unique=True, nullable=False)
    hyy = db.Column(db.Boolean, default=False)
    studentNumber = db.Column(db.String(10), nullable=True) # Outo pseudopakollinen arvo, jota ei voi tarkistaa backendissä...
    nickname = db.Column(db.String(255), nullable = True)
    discovered = db.Column(db.Text, nullable = True)
    applicationDate = db.Column(db.DateTime, default=datetime.now())
    status = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Jäsen %r>' % self.name

    def set_status(self, new_status: bool):
        self.status = new_status

from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    email = db.Column(db.String(254), unique=True, index=True)
    password_hash = db.Column(db.String(255))

    def __repr__(self):
        return '<Admin %r>' %self.username

    @property
    def password(self):
        return AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_reset_token(self):
        token = jwt.encode({
                "reset": self.id,
                "exp": datetime.utcnow()+timedelta(minutes=20)
            },
            current_app.config['SECRET_KEY'],
            algorithm="HS256"
            )
        return token

    def reset_password(token, new_password):
        try:
            data = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                leeway=timedelta(seconds=10),
                algorithms=["HS256"]
                )
        except:
            return False
        user = User.query.get(data.get("reset"))
        if user is None:
            return False
        
        user.password = new_password
        db.session.add(user)
        return True

from . import login_manager

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))