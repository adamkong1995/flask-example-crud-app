from flask import Blueprint, render_template, request, Response, g
from flask_login import login_required
import pandas as pd
import numpy as np


from flaskr.helpers.get_deals_report import Get_deals_report


reports = Blueprint('reports', __name__)


@reports.route('/report_selector', methods=['GET', 'POST'])
@login_required
def report_selector():
    if request.method == "GET":
        return render_template("/deal_record/report/report_selector.html", username=g.user.display_name)
    else:
        reportType = request.form.get('reportType')

        if reportType == "web_deals_report":
            deal_report = Get_deals_report()    
            json = deal_report.to_json(orient="records")
            # Escape special character
            json = json.replace("\\n", "\\\\n'")
            return render_template("/deal_record/report/deals_report.html", report=json, username=g.user.display_name)

        elif reportType == "csv_deals_report":
            deal_report = Get_deals_report()
            deal_report = deal_report.drop(['group_id', 'asso_id', 'im_id'], axis=1)

            return Response(deal_report.to_csv(index=False),
                            mimetype="text/csv",
                            headers={
                                "Content-disposition":
                                "attachment; filename=deals_report.csv"
                            })
