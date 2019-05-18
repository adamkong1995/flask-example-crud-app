import pandas as pd
from flaskr.services.flask_sqlalchemy import db

from flaskr.models.deals import Deal
from flaskr.models.deal_group import Deal_group
from flaskr.models.investmentManager import InvestmentManager
from flaskr.models.relationship import Asso_deal_to_im
from flaskr.models.project_update import Project_update


pd.set_option('display.float_format', lambda x: '%.2f' % x)
pd.options.display.max_colwidth = 256


def Get_deals_report():
    deal = pd.read_sql(db.session.query(Deal).statement, db.session.bind)
    groups = pd.read_sql(db.session.query(Deal_group.group_id, Deal_group.group_name).statement, db.session.bind)
    asso_deal_im = pd.read_sql(db.session.query(Asso_deal_to_im.asso_id, Asso_deal_to_im.deal_id, Asso_deal_to_im.im_id).statement, db.session.bind)
    ims = pd.read_sql(db.session.query(InvestmentManager.im_id, InvestmentManager.name).statement, db.session.bind)
    updates = pd.read_sql(db.session.query(Project_update.date_modified, Project_update.deal_id, Project_update.update_content).statement, db.session.bind)

    # keep the latest update for each project
    latest_updates = updates.sort_values('date_modified', ascending=False).drop_duplicates(['deal_id'])

    report = deal.merge(groups, on="group_id", how="left") \
                 .merge(asso_deal_im, on="deal_id", how="left") \
                 .merge(ims, on="im_id", how="left") \
                 .merge(latest_updates, on="deal_id", how="left")

    report = report.rename(columns={'date_modified_x': 'date_modified', 'name_x': 'project_name', 'name_y': 'pic', 'date_modified_y': 'date_updated'})

    # formatting
    report['date_created'] = report['date_created'].dt.strftime('%Y-%m-%d')
    report['date_modified'] = report['date_modified'].dt.strftime('%Y-%m-%d')
    report['dealSize'] = report['dealSize'].div(1000000)
    report['startDate'] = report['startDate'].dt.strftime('%Y-%m-%d').replace("NaT", "TBC")
    report['exitDate'] = report['exitDate'].dt.strftime('%Y-%m-%d').replace("NaT", "TBC")

    return report
