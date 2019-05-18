import pandas as pd

from flaskr.services.flask_sqlalchemy import db

from flaskr.models.deals import Deal
from flaskr.models.investmentManager import InvestmentManager
from flaskr.models.relationship import Asso_deal_to_im
from flaskr.models.project_update import Project_update


def load_modal():
    deal = pd.read_sql(db.session.query(Deal.deal_id, Deal.name).statement, db.session.bind)
    deal_im = pd.read_sql(db.session.query(Asso_deal_to_im.deal_id, Asso_deal_to_im.im_id).statement, db.session.bind)
    im = pd.read_sql(db.session.query(InvestmentManager.im_id, InvestmentManager.email).statement, db.session.bind)

    updates = pd.read_sql(db.session.query(Project_update).statement, db.session.bind)
    updates = updates.query('isSent != "Y"')
    updates = updates.merge(deal, on='deal_id', how='left')

    updatesNotSent = updates[['update_id', 'name', 'update_content']]
    return updatesNotSent.to_json(orient="records")


def get_email_list():
    deal = pd.read_sql(db.session.query(Deal.deal_id, Deal.name).statement, db.session.bind)

    deal_im = pd.read_sql(db.session.query(Asso_deal_to_im.deal_id, Asso_deal_to_im.im_id).statement, db.session.bind)

    im = pd.read_sql(db.session.query(InvestmentManager.im_id, InvestmentManager.email).statement, db.session.bind)

    updates = pd.read_sql(db.session.query(Project_update).statement, db.session.bind)
    updates = updates.query('isSent != "Y"')
    updates = updates.merge(deal, on='deal_id', how='left')

    emailList = updates.merge(deal_im, on='deal_id', how='left')
    emailList = emailList.merge(im, on='im_id', how='left')
    emailList = emailList[['email']].drop_duplicates()

    return emailList.to_json(orient="records")


def load_email(tosendIds):
    tosends = pd.read_sql(db.session.query(Project_update).statement, db.session.bind)
    tosends = tosends[tosends.update_id.isin(tosendIds)]
    deal = pd.read_sql("""SELECT d.deal_id, d.name, d."encounteredDate", d."dealSize", c.country, s.strategy, g.group_name
                            FROM deal d 
                            LEFT JOIN country c ON d.country_id = c.country_id
                            LEFT JOIN strategy s ON d.stgy_id = s.stgy_id
                            LEFT JOIN deal_group g ON d.group_id = g.group_id
                        """, db.session.bind)
    deal['encounteredDate'] = deal['encounteredDate'].dt.strftime('%Y-%m-%d')

    tosends = tosends.merge(deal, on='deal_id', how='left')
    return tosends.to_json(orient="records")
