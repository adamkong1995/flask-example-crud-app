from flask import Blueprint, request, render_template, redirect, request, jsonify, g
from flask_login import login_required
import pandas as pd

from flaskr.services.flask_sqlalchemy import db
from flaskr.services.flask_principal import user

from flaskr.models.deal_group import Deal_group
from flaskr.models.investmentManager import InvestmentManager
from flaskr.models.deals import Deal
from flaskr.models.relationship import Asso_deal_to_im
from flaskr.models.project_update import Project_update

from flaskr.helpers.add_project_group import add_new_group


project_edit = Blueprint('project_edit', __name__)


@project_edit.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    if request.method == "GET":
        managers = InvestmentManager.get_all_from_db()

        return render_template("/deal_record/edit/edit_table.html", 
                                managers=managers, 
                                selected_im=g.user.im_id, 
                                username=g.user.display_name)
    else:
        im_id = request.form['im_id']

        deal = pd.read_sql(db.session.query(Deal).statement, db.session.bind)
        asso_deal_im = pd.read_sql(db.session.query(Asso_deal_to_im).statement, db.session.bind)
        im = pd.read_sql(db.session.query(InvestmentManager).statement, db.session.bind)
        groupList = pd.read_sql(db.session.query(Deal_group).statement, db.session.bind)
        updates = pd.read_sql(db.session.query(Project_update).statement, db.session.bind)

        updates = updates.sort_values('date_modified', ascending=False).drop_duplicates(['deal_id'])
        updates = updates[['date_modified', 'deal_id']]
        updates = updates.rename(columns={'date_modified':'latest_update'})

        deal = deal.merge(asso_deal_im[['deal_id', 'im_id']], on="deal_id", how="left")
        deal = deal.merge(im[['im_id', 'name']], on="im_id", how="left")
        deal = deal.query("im_id == @im_id")
        deal = deal.merge(updates, on="deal_id", how="left")
        deal = deal.merge(groupList[['group_id', 'group_name']], on='group_id', how='left')

        deal['status'] = deal['status'].str.capitalize()
        deal['dealSize'] = deal['dealSize'].div(1000000)
        deal['startDate'] = deal['startDate'].dt.strftime('%Y-%m-%d')
        deal['exitDate'] = deal['exitDate'].dt.strftime('%Y-%m-%d')
        deal['startDate'] = deal['startDate'].replace("NaT", "TBC")
        deal['exitDate'] = deal['exitDate'].replace("NaT", "TBC")
        deal = deal.sort_values(by="date_modified", ascending=False)

        return jsonify(deal=deal.to_json(orient="records"))


@project_edit.route("/edit_record", methods=["GET", "POST"])
@login_required
@user.require(http_exception=403)
def edit_record():
    if request.method == "GET":
        deal_id = request.args.get('deal_id')
        deal = pd.read_sql(db.session.query(Deal).statement, db.session.bind)
        deal = deal.query('deal_id == ' + deal_id)
        deal['dealSize'] = deal['dealSize'] / 1000000

        # Replace Nat with None in time columns
        deal.startDate = deal.startDate.astype(object).where(deal.startDate.notnull(), None)
        deal.exitDate = deal.exitDate.astype(object).where(deal.exitDate.notnull(), None)

        managers = InvestmentManager.get_all_from_db()
        groupList = pd.read_sql(db.session.query(Deal_group).statement, db.session.bind)
        deal = deal.merge(groupList[['group_id', 'group_name']], on='group_id', how='left')

        participants = pd.read_sql(db.session.query(Asso_deal_to_im).statement, db.session.bind)
        participants = participants.query('deal_id == @deal_id')

        return render_template('/deal_record/edit/edit_project.html', 
                                deal=deal, 
                                managers=managers, 
                                participants=participants['im_id'].tolist(), 
                                username=g.user.display_name)
    else:
        deal_to_edit = Deal.find_by_id(request.form['submitButton'])

        # Create a group if not exist in db
        if request.form.get('group_id') == '-1':
            add_new_group(request.form.get('group'))

        group_id = Deal_group.find_by_group_name(request.form.get('group'))
        group_id = group_id.group_id

        deal_to_edit.group_id = group_id
        deal_to_edit.name = request.form.get('name')
        deal_to_edit.description = request.form.get('description')

        deal_to_edit.dealSize = float(request.form.get('dealsize'))*1000000
        deal_to_edit.status = request.form.get('status')

        if request.form.get('startDate') != "None":
            if request.form.get('startDate'):
                deal_to_edit.startDate = request.form.get('startDate')
            else:
                deal_to_edit.startDate = None

        if request.form.get('exitDate') != "None":
            if request.form.get('exitDate'):
                deal_to_edit.exitDate = request.form.get('exitDate')
            else:
                deal_to_edit.exitDate = None

        deal_to_edit.investmentManager = []
        pic = Asso_deal_to_im('main')
        pic.investmentManager = InvestmentManager.find_by_id(request.form.get('manager1'))
        deal_to_edit.investmentManager.append(pic)
        deal_to_edit.save_to_db()

        return redirect('/edit')


@project_edit.route('/project_delete', methods=["POST"])
@login_required
@user.require(http_exception=403)
def project_delete():
    deal_id = request.form['deal_id']

    # Remove all update before remove an investment
    while Project_update.find_by_deal_id(deal_id):
        update_to_delete = Project_update.find_by_deal_id(deal_id)
        update_to_delete.delete_from_db()
    deal_to_delete = Deal.find_by_id(deal_id)
    deal_to_delete.delete_from_db()
    return redirect('/edit')
