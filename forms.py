# -*- coding: utf-8 -*-

from models import User, Post
from wtforms_alchemy import ModelForm
from flask.ext.wtf import Form
from wtforms import \
    StringField,\
    PasswordField,\
    TextAreaField,\
    IntegerField,\
    validators
from wtforms.validators import Email, DataRequired, EqualTo

# https://wtforms-alchemy.readthedocs.org/en/latest/introduction.html
# http://wtforms-alchemy.readthedocs.org/en/latest/configuration.html#modelform-meta-parameters


class PostForm(Form):
    title = StringField(
        label=u'Title',
        )
    text = TextAreaField(
        label=u'Text',
    )


class CommentForm(Form):
    text = TextAreaField(
        label=u'Your comment',
    )


class BackwardForm(Form):
    title = StringField(
        label=u'Title',
        validators=[validators.length(min=3, max=100)])
    text = TextAreaField(
        label=u'Your message',
        validators=[validators.length(min=3, max=3000)]
    )


class LoginForm(Form):
    username = StringField()
    password = PasswordField()

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, *args, **kwargs):
        rv = super(LoginForm, self).validate()
        if not rv:
            return False

        user = User.query.filter_by(
            username=self.username.data).first()
        if user is None:
            self.username.errors.append('Unknown username')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        self.user = user
        return True


class RegistrationForm(Form):
    username = StringField(
        # label=u'User'
    )
    email = StringField(
        # label=u'Email',
        validators=[
            DataRequired(),
            Email()]
    )
    password = PasswordField(
        # label=u'Password',
        validators=[EqualTo('confirm_password', message='Passwords must match')]
    )
    confirm_password = PasswordField(
        # label=u'Confirm Password',
        validators=[DataRequired()]
    )
