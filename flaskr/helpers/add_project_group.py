from flaskr.models import deal_group


def add_new_group(group_name):
    group_to_add = deal_group.Deal_group(group_name)
    group_to_add.save_to_db()
