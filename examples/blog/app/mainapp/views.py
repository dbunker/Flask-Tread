import flask
from mainapp import app
from mainapp import db
from flask import jsonify
from passlib.hash import sha256_crypt

from functools import wraps

import random
import string
import re
import json
import time

from flask import Response, request
import models
from models import User, Comment

from flask_tread import init_tread_app, id_to_hash, hash_to_id
from flask_tread import route, auth_route, create_token
from flask_tread import Optional, MultiType, ignored

init_tread_app(app, app.config['LOGIN_KEY'])

##################
# User

@route('/api/user', command='signup', takes={
    'username': unicode,
    'email': unicode,
    'password': unicode
}, sends={
    'username': unicode,
    'userId': id_to_hash,
    'token': unicode
})
def signup():

    json_data = flask.g.json_data
    username = json_data['username']
    email = json_data['email']
    password = json_data['password']

    if not re.match('^\w{6,}$', username):
        return { 'error': 'invalid username' }

    if not re.match('^\w{6,}$', password):
        return { 'error': 'invalid password' }

    if not re.match('^[\.\w]{1,}[@]\w+[.]\w+$', email):
        return { 'error': 'invalid email' }

    if User.query.filter_by(username = username).first() is not None:
        return { 'error': 'username already exists' }

    if User.query.filter_by(email = email).first() is not None:
        return { 'error': 'email already exists' }

    set_user = User(
        username = username,
        email = email
    )
    set_user.hash_password(password)

    db.session.add(set_user)
    db.session.commit()

    return {
        'username': set_user.username,
        'userId': set_user.id,
        'token': create_token(set_user.id)
    }

@route('/api/user', command='login', takes={
    'usernameEmail': unicode,
    'password': unicode
}, sends={
    'username': unicode,
    'userId': id_to_hash,
    'token': unicode
})
def login():

    json_data = flask.g.json_data
    username_email = json_data['usernameEmail']
    password = json_data['password']

    user = User.query.filter_by(email = username_email).first()

    if user == None:
        user = User.query.filter_by(username = username_email).first()

    if user == None:
        return { 'error': 'could not find user' }, 400

    if not user.verify_password(password):
        return { 'error': 'could not authenticate' }, 400

    return {
        'username': user.username,
        'userId': user.id,
        'token': create_token(user.id)
    }

@auth_route('/api/user', command='checkToken', sends={
    'validToken': bool
})
def check_token():
    return {
        'validToken': True
    }

##################
# Comment

comment_sends = {
    'userId': id_to_hash,
    'commentId': id_to_hash,
    'text': unicode
}

@auth_route('/api/comment', command='create', takes={
    'text': unicode
}, sends=comment_sends)
def create_comment():

    json_data = flask.g.json_data
    user_id = flask.g.user_id

    new_comment = Comment(
        user_id = user_id,
        text = json_data['text']
    )

    db.session.add(new_comment)
    db.session.commit()

    return new_comment.object()

@auth_route('/api/comment/<comment_id>', command='get', params={
    'comment_id': hash_to_id
}, sends=comment_sends)
def get_comment(comment_id):

    comment = Comment.query.get(comment_id)
    return comment.object()

@auth_route('/api/comment', command='get', sends={
    'comments': [ comment_sends ]
})
def all_comments():

    comments = Comment.query.all()
    return {
        'comments': [ comment.object() for comment in comments ]
    }
