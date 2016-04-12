# -*- coding: utf-8 -*-

from flask import (
    Blueprint,
    redirect,
    url_for,
    flash,
    request,
    render_template
)
from flask.ext.login import (
    login_user,
    logout_user,
    login_required,
    current_user
)
from flask_mail import Message
from forms import LoginForm, RegistrationForm
from models import User
from app import db, mail

auth = Blueprint('auth', __name__)


# admin = Blueprint('admin', __name__, url_prefix='/admin')
# https://github.com/apiguy/flask-classy


# Views:
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html', form=RegistrationForm())

    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        user = User(form.username.data, form.email.data)
        form.populate_obj(user)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        msg = Message(
            'Successful registration!',
            sender=('Blog Tceh Cource', 'flask.mail@yandex.ru'),
            recipients=[form.email.data]
        )
        msg.body = 'Welcome to our blog!'
        mail.send(msg)
        flash('Successful registration! Please login.')

        return redirect(url_for('auth.login'))

    else:
        return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', form=LoginForm())

    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = form.user
        login_user(user, remember=True)
        flash('Logged in successfully.')

        return redirect(url_for('blog.home'))

    else:
        flash('Logged in unsuccessfully')
        return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('blog.home'))
