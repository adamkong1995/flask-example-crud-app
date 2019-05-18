from flask_login import LoginManager
from flask import redirect, url_for, g

from flaskr.models.investmentManager import InvestmentManager


login_manager = LoginManager()


# Middleware for loading user using request cookie
@login_manager.user_loader
def load_user(dn):
    user = InvestmentManager.find_by_dn(dn)
    if not user:
        return None

    g.user = user
    return user


# Redirect to login page when user is not logged in
@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('auth.login'))
