# -*- coding: utf-8 -*-

__author__ = 'kirillsavelyev'

import datetime

from flask import (
    Blueprint,
    redirect,
    url_for,
    flash,
    request,
    render_template
)
from flask_login import login_required, current_user
from flask_mail import Message
from forms import BidForm, BackwardForm
from models import User, Bid
from app import db, mail

home = Blueprint('home', __name__)
# https://github.com/apiguy/flask-classy


@home.route('/', methods=['GET', 'POST'])
def personal_area():
    if current_user.is_authenticated:
        vacation_days = current_user.vacation_days

        bids = Bid.query.filter_by(
            user_id=current_user.id, is_visible=True).all()

        bids.sort(key=lambda item: item.vac_date)

        return render_template(
            'index.html', vac_days=vacation_days, bids=bids)
    else:
        return redirect(url_for('auth.login'))


@home.route('/view_bid', methods=['POST'])
@login_required
def view_bid():
    if request.method == 'POST':
        bid_id = request.form['id']
        bid = Bid.query.filter_by(id=bid_id).first()

        return render_template('bid.html', bid=bid)


@home.route('/new_bid', methods=['GET', 'POST'])
@login_required
def new_bid():
    if request.method == 'POST':
        user = User.query.filter_by(username=current_user.username).first()
        form = BidForm(request.form)
        if form.validate():
            form.user = user
            bid = Bid(user=user, **form.data)

            User.query.filter_by(
                id=user.id
            ).update({'vacation_days': user.vacation_days - form.vac_days.data})

            db.session.add(bid)
            db.session.commit()
            vac_date = \
                Bid.query.filter_by(vac_date=bid.vac_date).first().vac_date
            flash('Vacation "{}" created!'.format(vac_date))
            return redirect(url_for('home.personal_area'))
        else:
            return render_template('new_bid.html', form=form)

    form = BidForm()

    return render_template('new_bid.html', form=form)


@home.route('/edit_bid', methods=['GET', 'POST'])
@login_required
def edit_bid():
    # if request.method == 'POST':
    #     user = User.query.filter_by(username=current_user.username).first()
    #     form = BidForm(request.form)
    #     if form.validate():
    #         form.user = user
    #         bid = Bid(user=user, **form.data)
    #         db.session.add(bid)
    #         db.session.commit()
    #         vac_date = Bid.query.\
    #             filter_by(vac_date=bid.vac_date).first().vac_date
    #         flash('Bid "{}" edited!'.format(vac_date))
    #         return redirect(url_for('home.personal_area'))
    #
    # form = BidForm()
    #
    # return render_template('new_bid.html', form=form)
    pass


@home.route('/delete_bid', methods=['POST'])
@login_required
def delete_bid():
    if request.method == 'POST':
        bid_id = request.form['id']
        bid = Bid.query.filter_by(id=bid_id).first()
        min_days = bid.vac_date.day - datetime.date.today().day
        # TODO: Create check vac_date that is earlier than bid_date
        if min_days > 3:
            bid.is_visible = False

            User.query.filter_by(
                id=current_user.id
            ).update(
                {'vacation_days': current_user.vacation_days + bid.vac_days})

            db.session.commit()
            flash('Bid {} deleted!'.format(bid.vac_date))
            return redirect(url_for('home.personal_area'))
        else:
            flash('You are late! Go to the Vacation!', 'error')
            return redirect(url_for('home.personal_area'))


@home.route('/user_profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    if request.method == 'GET':
        return render_template('user_profile.html', form=BackwardForm())

    if request.method == 'POST':
        form = BackwardForm(request.form)
        if form.validate_on_submit():
            msg = Message(
                form.title.data,
                sender=[current_user.username, 'flask.mail@yandex.ru'],
                recipients=['flask.mail@yandex.ru']
            )
            msg.body = form.text.data
            mail.send(msg)

            flash('Message will be send!')

        return redirect(url_for('home.user_profile'))


# @home.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404
