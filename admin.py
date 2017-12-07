# -*- coding: utf-8 -*-

__author__ = 'kirillsavelyev'

from flask import (
    Blueprint,
    request,
    render_template
)
from flask_login import login_required, current_user
from models import Bid
from app import db

admin = Blueprint('admin', __name__)


@admin.route('/statistics', methods=['GET', 'POST'])
@login_required
def statistics():
    if current_user.is_admin:
        # request all years from db
        years_t = db.session.query(
            db.func.strftime('%Y', Bid.vac_date)
        ).distinct().all()

        # need transformation to list, because db returns tuple
        years = []
        for year in years_t:
            years.append(year[0])

        years.sort()

        if request.method == 'GET':
            return render_template('statistics.html', years=years)

        elif request.method == 'POST':
            year = request.form['year']

            # request vacation dates and days per year
            bids = db.session.query(
                db.func.strftime('%m', Bid.vac_date),
                db.func.sum(Bid.vac_days)
            ).filter_by(
                is_visible=True
            ).filter(
                db.func.strftime('%Y', Bid.vac_date).like(year)
            ).group_by(
                db.func.strftime('%Y', Bid.vac_date),
                db.func.strftime('%m', Bid.vac_date)
            ).all()

            # Sum of vacation days for each month
            vac_days_month = [0]*12

            for m, d in bids:
                vac_days_month[int(m)-1] = d

            # Total sum of vacation days in year
            vac_days_year = sum(vac_days_month)

            legend = 'Monthly Vacations'
            labels = ["January", "February", "March",
                      "April", "May", "June",
                      "July", "August", "September",
                      "October", "November", "December"]

            return render_template('statistics.html',
                                   values=vac_days_month,
                                   labels=labels,
                                   legend=legend,
                                   vac_days_year=vac_days_year,
                                   years=years)
