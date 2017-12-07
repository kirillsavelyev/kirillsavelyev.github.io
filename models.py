# -*- coding: utf-8 -*-

__author__ = 'kirillsavelyev'

import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# Models for creating database tables


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(100), unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    password = db.Column(db.String(10))
    vacation_days = db.Column(db.Integer, default=28)
    in_staff = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, username, email, first_name, last_name):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
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


# class Vacation(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     user = db.relationship(
#         'User', backref=db.backref('posts', lazy='dynamic'))
#     n_days = db.Column(db.Integer)
#
#     def __init__(self, user=None, n_days='', csrf_token=None):
#         self.user = user
#         self.n_days = n_days


class Bid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(
        'User', backref=db.backref('comments', lazy='dynamic'))
    bid_date = db.Column(db.Date, default=datetime.date.today())
    vac_date = db.Column(db.Date)
    vac_days = db.Column(db.Integer)
    is_visible = db.Column(db.Boolean, default=True)

    def __init__(self, user, vac_date, vac_days, csrf_token=None):
        self.user = user
        self.vac_date = vac_date
        self.vac_days = vac_days

