from flask import Blueprint, request, render_template, redirect, url_for, current_app
from flask_login import login_user, logout_user, login_required
from flask_principal import Principal, Identity, AnonymousIdentity, identity_changed

from flaskr.services.flask_ldap3_login import ldap_manager
from flaskr.services.flask_login import login_manager
from flaskr.services.flask_principal import principal_manager
from flaskr.models.investmentManager import InvestmentManager


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        # Use if you setup a ldap server
        #res = ldap_manager.authenticate(request.form.get('username'), request.form.get('password'))
        # Check if verified
        #if res.status.name == 'fail':
        #    return render_template('login.html', message='Login Failed. Please try again.')
        #user_info = dict(res.user_info)

        # If you dont have ldap server, you can use it as demo auth function
        if request.form.get('username') == 'webadmin':
            user_info = {}
            user_info['dn'] = 'CN=WebAdminTeam'
            user_info['memberOf'] = ['CN=WebAdminTeam']
            user_info['displayName'] = 'Web Admin'
            user_info['mail'] = 'webadmin@test.com'
        elif request.form.get('username') == 'user':
            user_info = {}
            user_info['dn'] = 'CN=NormalUser'
            user_info['memberOf'] = ['CN=NormalUser']
            user_info['displayName'] = 'Tom'
            user_info['mail'] = 'normalUser@test.com'
        else:
            return render_template('login.html', message='Login Failed. Please try again.')

        user = InvestmentManager.find_by_dn(user_info['dn'])
        if not user:
            user = InvestmentManager(user_info['displayName'], user_info['dn'])
            user.save_to_db()

        # Update user info on every login
        user = update_user_info(user, user_info)

        login_user(user, remember=True)
        identity_changed.send(current_app._get_current_object(), identity=Identity(user.member_of))

        return redirect(url_for('project_add.add'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    # Clean the role in flask principal
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
    return redirect(url_for('auth.login'))


def update_user_info(user, user_info):
    user.display_name = user_info['displayName']
    user.email = user_info['mail']
    if 'memberOf' in user_info:
        user.member_of = '|'.join(user_info['memberOf'])
    user.save_to_db()

    return user
