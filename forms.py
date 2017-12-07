# -*- coding: utf-8 -*-

__author__ = 'kirillsavelyev'


from models import User
from flask_login import current_user
from wtforms_alchemy import ModelForm
from flask_wtf import FlaskForm
from wtforms import \
    StringField,\
    PasswordField,\
    TextAreaField,\
    DateField,\
    IntegerField,\
    validators
from wtforms.validators import \
    Email, \
    DataRequired, \
    EqualTo, \
    NumberRange

# https://wtforms-alchemy.readthedocs.org/en/latest/introduction.html
# http://wtforms-alchemy.readthedocs.org/en/latest/configuration.html#modelform-meta-parameters


class BidForm(FlaskForm):
    vac_date = DateField(
        label='Vacation start date',
        render_kw={"placeholder": 'yyyy-mm-dd'},
        validators=[DataRequired()]
    )
    vac_days = IntegerField(
        label='Number of days',
        render_kw={"placeholder": '2-20'},
        validators=[DataRequired(),
                    # NumberRange(min=2,
                    #             max=20,
                    #             message='Range from 2 to 20')
                    ]
    )

    def validate(self):
        vd = User.query.filter_by(id=current_user.id).first().vacation_days
        vac_days_avail = vd - self.vac_days.data

        if vac_days_avail < 0:
            self.vac_days.errors = list(self.vac_days.errors)
            self.vac_days.errors.append(
                'You have only {} days of vacation'.format(vd))

            return False

        return True


class BackwardForm(FlaskForm):
    title = StringField(
        label=u'Title',
        validators=[validators.length(min=3, max=100)])
    text = TextAreaField(
        label=u'Your message',
        validators=[validators.length(min=3, max=3000)]
    )


class LoginForm(FlaskForm):
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


class RegistrationForm(FlaskForm):
    username = StringField(
        # label=u'User'
        validators=[DataRequired()]
    )
    first_name = StringField(
        # label=u'First Name'
    )
    last_name = StringField(
        # label=u'Last Name'
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
