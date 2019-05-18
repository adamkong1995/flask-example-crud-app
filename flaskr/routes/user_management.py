from flask import Blueprint, request, render_template, g, redirect
from flask_login import login_required

from flaskr.services.flask_sqlalchemy import db
from flaskr.models.investmentManager import InvestmentManager
import pandas as pd


user = Blueprint('user', __name__)


@user.route('/user_management', methods=['GET', 'POST'])
@login_required
def user_management():
    if request.method == 'GET':
        users = pd.read_sql(db.session.query(InvestmentManager).statement, db.session.bind)
        users = users.sort_values(by=['im_id'])
        return render_template('/data_admin/user_management.html', users=users, username=g.user.display_name)
    if request.method == 'POST':
        json = request.get_json()

        user = InvestmentManager.find_by_id(json['id'])
        user.name = json['short_name']
        user.isActive = json['isActive']
        user.save_to_db()
        return redirect('/user_management')
