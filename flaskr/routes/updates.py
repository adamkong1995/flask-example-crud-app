from flask import Blueprint, render_template, request, Response, jsonify, redirect, g
from flask_login import login_required
import pandas as pd

from flaskr.services.flask_sqlalchemy import db
from flaskr.services.flask_principal import user

from flaskr.models.deals import Deal
from flaskr.models.deal_group import Deal_group
from flaskr.models.investmentManager import InvestmentManager
from flaskr.models.relationship import Asso_deal_to_im
from flaskr.models.project_update import Project_update


updates = Blueprint('updates', __name__)


@updates.route("/project_update", methods=["GET", "POST"])
@login_required
@user.require(http_exception=403)
def project_update_page():
    if request.method == "GET":
        deal_id = request.args.get('deal_id')

        projects = pd.read_sql(db.session.query(Deal).statement, db.session.bind)
        projects = projects.sort_values(by='name')
        return render_template("/deal_record/update/update_selector.html", 
                                projects=projects, 
                                deal_id=deal_id, 
                                username=g.user.display_name)
    else:
        deal_id = request.form['submitButton']

        deal = pd.read_sql(db.session.query(Deal).statement, db.session.bind)
        projects = deal.sort_values(by='name')
        group = pd.read_sql(db.session.query(Deal_group).statement, db.session.bind)

        # get project's investment manager
        asso_deal_im = pd.read_sql(db.session.query(Asso_deal_to_im).statement, db.session.bind)
        im = pd.read_sql(db.session.query(InvestmentManager).statement, db.session.bind)
        asso_deal_im = asso_deal_im.merge(im, on="im_id", how="left")
        asso_deal_im = asso_deal_im.query('deal_id == @deal_id')
        im_name = ""
        for name in asso_deal_im['name']:
            if isinstance(name, str):
                im_name = im_name + " " + name

        deal = deal.merge(group, on="group_id", how="left")
        deal = deal.query("deal_id == @deal_id")

        updates = pd.read_sql(db.session.query(Project_update).statement, db.session.bind)
        updates = updates.query("deal_id == @ deal_id")
        updates = updates[['date_created', 'update_id', 'update_content', 'isSent']]
        updates = updates.sort_values(by='date_created', ascending=True)
        updates['date_created'] = updates['date_created'].apply(lambda x: x.strftime('%Y-%m-%d'))
        return jsonify(deal_id=deal_id, 
                        group=deal['group_name'].iloc[0], 
                        im_name=im_name, 
                        description=deal['description'].iloc[0], 
                        deal=deal['name'].iloc[0], 
                        update=updates.to_json(orient="records"))


@updates.route('/project_update_add', methods=["POST"])
@login_required
@user.require(http_exception=403)
def project_update_add():
    update = Project_update(request.form['deal_id'], request.form['update_content'], "N")
    update.save_to_db()
    return redirect("/project_update")


@updates.route('/project_update_edit', methods=["POST"])
@login_required
@user.require(http_exception=403)
def project_update_edit():
    update_to_edit = Project_update.find_by_id(request.form['update_id'])
    update_to_edit.update_content = request.form['update_content']
    update_to_edit.isSent = request.form['isSend']
    update_to_edit.save_to_db()
    return redirect("/project_update")


@updates.route('/project_update_delete', methods=['POST'])
@login_required
@user.require(http_exception=403)
def project_update_delete():
    update_to_delete = Project_update.find_by_id(request.form['update_id'])
    update_to_delete.delete_from_db()
    return redirect("/project_update")
