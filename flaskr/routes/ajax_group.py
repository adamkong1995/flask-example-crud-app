from flask import Blueprint, jsonify
from flask_login import login_required
import pandas as pd

from flaskr.services.flask_sqlalchemy import db
from flaskr.models.deal_group import Deal_group


ajax_group = Blueprint('ajax_group', __name__)


@ajax_group.route('/ajax_search_group', methods=['POST'])
@login_required
def ajax_search_group():
    group_list = pd.read_sql(db.session.query(Deal_group).statement, db.session.bind)
    group_list = group_list['group_name']
    return jsonify(group=group_list.to_json(orient="records"))


@ajax_group.route('/ajax_search_group_id', methods=['POST'])
@login_required
def ajax_search_group_id():
    group_name = request.form['input_text']
    group_id = Deal_group.find_by_group_name(group_name)
    group_id = group_id.group_id
    return jsonify(group=group_id)
