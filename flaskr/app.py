from flask import Flask, render_template, request
from flask_migrate import Migrate
from flask_principal import identity_loaded, RoleNeed

from flaskr.services.flask_sqlalchemy import db
from flaskr.services.flask_ldap3_login import ldap_manager
from flaskr.services.flask_login import login_manager
from flaskr.services.flask_principal import principal_manager
from flaskr.routes import project_add, project_edit, ajax_group, updates, update_emails, reports, auth, user_management, factiva_keywords


app = Flask(__name__)
app.config.from_pyfile('config.py')

migrate = Migrate(app, db)
login_manager.init_app(app)
ldap_manager.init_app(app)
principal_manager.init_app(app)

# Assign permission role to current user based on AD server's DN
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    needs = []
    role = str(identity.id)

    if 'NormalUser' in role:
        needs.append(RoleNeed('user'))

    if 'WebAdminTeam' in role:
        needs.append(RoleNeed('user'))
        needs.append(RoleNeed('super_user'))

    for n in needs:
        identity.provides.add(n)


@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(403)
def page_not_found(e):
    return render_template('permission_denied.html', referer=request.url)


app.register_blueprint(auth.auth)
app.register_blueprint(project_add.project_add)
app.register_blueprint(project_edit.project_edit)
app.register_blueprint(ajax_group.ajax_group)
app.register_blueprint(updates.updates)
app.register_blueprint(update_emails.update_emails)
app.register_blueprint(reports.reports)
app.register_blueprint(user_management.user)
app.register_blueprint(factiva_keywords.keywords)


db.init_app(app)
db.create_all(app=app)
