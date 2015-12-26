from mainapp import db
import string
import random
from passlib.hash import sha256_crypt
import datetime
from utils import get_time

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    comments = db.relationship('Comment', backref='user', lazy='dynamic')

    created_at = db.Column(db.DateTime, default=get_time)

    def hash_password(self, password):
        self.password_hash = sha256_crypt.encrypt(password)

    def verify_password(self, password):
        return sha256_crypt.verify(password, self.password_hash)

    def __repr__(self):
        return '<User %r>' % (self.username)

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)

    text = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    created_at = db.Column(db.DateTime, default=get_time)

    def object(self):
        return {
            'userId': self.user_id,
            'commentId': self.id,
            'text': self.text
        }

    def __repr__(self):
        return '<Comment %r>' % (self.native_text)
