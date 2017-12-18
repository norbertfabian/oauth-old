# -*- coding: utf-8 -*-

import os
import string
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'databse connect string'
SECRET_KEY = 'flask secret key'


ADMINS = frozenset(['martin@miksanik.net'])
ADMIN_EMAIL = 'euro@profires.cz'
#RETURN_PATH = "http://oauth.cz/private/"
RETURN_PATH = "/api/html/logged/#"

SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}


DB_TOKEN_LEN = 64
RANDOM_CHAR = string.ascii_letters + string.digits
SHELL_BANNER = "OAuth"

TEST_APP_TOKEN = SECRET_KEY
APPLICATION_ID = 0
REDIRECT_GET_ARG = 'next'
APPLICATION_GET_ARG = 'app'
RETURN_PATH_COOKIE = 'RETURN_PATH'

APPLICATION_TOKEN_COOKIE = 'OAUTH_APP'
USER_TOKEN_COOKIE = 'OAUTH_USER'
APPLICATION_HEADER_FIELD = 'X_OAUTH_APP'
USER_HEADER_FIELD = 'X_OAUTH_USER'

DEFAULT_MAIL_SENDER = 'bot@oauth.cz'
MAIL_SERVER = 'proxy.profires.cz'
MAIL_PORT = 465

LDAP_BASE = 'dc=neco,dc=neco'
LDAP_PASSWORD_ALGORITHM= 'MD5'
LDAP_SERVERS = [
                    {'server': '', 'port': '', 'ssl': ''},
                ]
LDAP_USER_DN = 'uid=%%s, ou=People,%s' % LDAP_BASE
LDAP_CLIENT_DN = 'uidNumber=%%(id)d, ou=Clients,%s' % LDAP_BASE
LDAP_CONTACT_DN = 'uidNumber=%%(id)d, ou=Contacts,%s' % LDAP_BASE
LDAP_APPLICATION_DN = 'gidNumber=%%(id)d, ou=Application, %s' % LDAP_BASE

LDAP_CONTACT_MAP = {}
LDAP_USER_MAP = {}
LDAP_CLIENT_MAP = {}

