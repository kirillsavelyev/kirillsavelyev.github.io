# -*- coding: utf-8 -*-

import datetime
from flask_sqlalchemy import SQLAlchemy
# from app import db
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(10))

    def __init__(self, username, email):
        self.username = username
        self.email = email
        # self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

    def __str__(self):
        return repr(self)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    # TODO: Поискать методы отобажения названий полей в фоме ввода


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(
        'User', backref=db.backref('posts', lazy='dynamic'))
    title = db.Column(db.String(150), unique=True)
    text = db.Column(db.String(3500))
    date = db.Column(db.Date, default=datetime.date.today())
    is_visible = db.Column(db.Boolean, default=True)

    def __init__(self, user=None, title='', text='',
                 date=None, is_visible=None):
        self.user = user
        self.title = title
        self.text = text
        self.date = date
        self.is_visible = is_visible


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(
        'User', backref=db.backref('comments', lazy='dynamic'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship(
        'Post', backref=db.backref('comments', lazy='dynamic'))
    text = db.Column(db.String(1000))
    date = db.Column(db.Date, default=datetime.date.today())
    is_visible = db.Column(db.Boolean, default=True)

    def __init__(self, user=None, post=None, text='',
                 date=None, is_visible=None):
        self.user = user
        self.post = post
        self.text = text
        self.date = date
        self.is_visible = is_visible
