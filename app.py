# -*- coding: utf-8 -*-

__author__ = 'kirillsavelyev'

import os
import config

from flask import Flask, redirect, url_for, Blueprint
from flask_login.login_manager import LoginManager
from flask_mail import Mail
from models import db

login_manager = LoginManager()
mail = Mail()

base_dir = os.path.dirname(__file__)

bower_blueprint = Blueprint(
        'bower', __name__, static_url_path='',
        static_folder=os.path.join(base_dir, 'static')
    )


def create_app():
    from views import home
    from auth import auth
    from admin import admin

    app = Flask(__name__, template_folder='templates')
    app.config.from_object(config)

    app.register_blueprint(auth)
    app.register_blueprint(home)
    app.register_blueprint(admin)
    app.register_blueprint(bower_blueprint)

    login_manager.init_app(app)

    mail.init_app(app)
    db.init_app(app)

    # Dynamic context:
    with app.app_context():
        db.create_all()

    return app


@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('auth.login'))


if __name__ == '__main__':
    app = create_app()
    app.run()

