from flask import Blueprint, request, render_template, redirect, request, g
from flask_login import login_required
import pandas as pd

from flaskr.services.flask_sqlalchemy import db
from flaskr.services.flask_principal import user

from flaskr.models.deals import Deal
from flaskr.models.investmentManager import InvestmentManager
from flaskr.models.deal_group import Deal_group
from flaskr.models.relationship import Asso_deal_to_im

from flaskr.helpers.add_project_group import add_new_group


project_add = Blueprint('project_add', __name__)


@project_add.route("/", methods=['GET'])
@login_required
def add():
    managers = InvestmentManager.get_all_active()
    groups = Deal_group.get_all_from_db()

    return render_template('/deal_record/add/add.html', 
                            managers=managers, 
                            groups=groups, 
                            username=g.user.display_name, 
                            current_user=g.user.im_id)


@project_add.route("/add_project", methods=['POST'])
@login_required
@user.require(http_exception=403)
def add_project():
    dealSize = float(request.form.get('dealsize')) * 1000000

    if request.form.get('startDate'):
        startDate = request.form.get('startDate')
    else:
        startDate = None

    if request.form.get('exitDate'):
        exitDate = request.form.get('exitDate')
    else:
        exitDate = None

    # Add investment group if it is not exist in database
    if request.form.get('group_id') == '-1':
        add_new_group(request.form.get('group'))

    group_id = Deal_group.find_by_group_name(request.form.get('group'))
    group_id = group_id.group_id

    deal = Deal(group_id, request.form.get('name'), request.form.get('description'), dealSize, request.form.get('status'), startDate, exitDate)

    pic = Asso_deal_to_im('main')
    pic.investmentManager = InvestmentManager.find_by_id(request.form.get('manager1'))
    deal.investmentManager.append(pic)

    deal.save_to_db()
    return redirect("/")
