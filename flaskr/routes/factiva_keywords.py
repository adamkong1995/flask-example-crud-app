from flask import Blueprint, render_template, g, request, jsonify
from flask_login import login_required
import pandas as pd

from flaskr.services.flask_sqlalchemy import db
from flaskr.services.flask_principal import user

from flaskr.models.factiva_keywords import factiva_keywords
from flaskr.models.investmentManager import InvestmentManager


keywords = Blueprint('keywords', __name__)


@keywords.route('/edit_keywords', methods=['GET'])
@login_required
def edit_keywords():
    ims = InvestmentManager.get_all_active()
    new_keywords = factiva_keywords.get_all_from_db()
    return render_template('/deal_record/news/keywords.html', 
                            ims=ims, 
                            current_user=g.user.im_id, 
                            username=g.user.display_name)


@keywords.route('/add_keywords', methods=['POST'])
@login_required
def add_keywords():
    data = request.get_json()
    keywords = factiva_keywords(data['keywords'], data['im'])
    keywords.save_to_db()
    return "done"


@keywords.route('/load_keywords', methods=['POST'])
@login_required
def load_keywords():
    data = request.get_json()
    im = data['im']

    keywords = pd.read_sql(db.session.query(factiva_keywords).statement, db.session.bind)
    keywords = keywords.query('im_id == @im')

    return jsonify(keywords.to_json(orient="records"))


@keywords.route('/delete_keywords', methods=['POST'])
@login_required
def delete_keywords():
    data = request.get_json()
    keywords = factiva_keywords.find_by_id(data['id'])
    keywords.delete_from_db()
    return "hi"
