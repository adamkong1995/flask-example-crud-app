import os
from flaskr import key

# Environment
ENV = key.ENV

# Application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Database configuration
SQLALCHEMY_DATABASE_URI = key.SQLALCHEMY_DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Cookies configuration
SECRET_KEY = key.SECRET_KEY
SESSION_COOKIE_NAME = key.SESSION_COOKIE_NAME
REMEMBER_COOKIE_DURATION = 2629746 # 1 month

# LDAP configuration
LDAP_HOST = key.LDAP_HOST
LDAP_BASE_DN = key.LDAP_BASE_DN
LDAP_USER_LOGIN_ATTR = key.LDAP_USER_LOGIN_ATTR
LDAP_BIND_USER_DN = key.LDAP_BIND_USER_DN
LDAP_BIND_USER_PASSWORD = key.LDAP_BIND_USER_PASSWORD
