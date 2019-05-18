from flaskr.models import project_update
import json


def update_isSend_status(jsonData):
    ids = json.loads(jsonData)
    for item in ids:
        to_update = project_update.Project_update.find_by_id(item['update_id'])
        to_update.isSent = "Y"
        to_update.save_to_db()
