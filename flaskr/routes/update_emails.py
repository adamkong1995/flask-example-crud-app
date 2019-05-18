from flask import Blueprint, request, jsonify
from flask_login import login_required

from flaskr.helpers import load_update_content, send_update_email, update_status


update_emails = Blueprint('update_emails', __name__)


@update_emails.route('/update_email_get', methods=['POST'])
@login_required
def update_email_get():
    updatesNotSent = load_update_content.load_modal()
    emailList = load_update_content.get_email_list()

    return jsonify(updates=updatesNotSent, emails=emailList)


@update_emails.route('/update_email_send', methods=['POST'])
@login_required
def update_email_send():
    json = request.get_json()
    tosendIds = json['id']
    tosends = load_update_content.load_email(tosendIds)

    try:
        send_update_email.send(json['to'], json['cc'], tosends)
        update_status.update_isSend_status(tosends)
        return jsonify(status="done")
    except:
        return jsonify(status="error")
