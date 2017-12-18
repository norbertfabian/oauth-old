# -*- coding: utf-8 -*-
import json
from functools import wraps
from flask import g, request, make_response
from oauth import app
from oauth.lib import getValidToken, dbGetApplication, dbGetApplicationUser

def require_usertoken(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        g.token = None
        token = request.cookies.get(app.config['USER_TOKEN_COOKIE'])
        token = request.headers.get(app.config['USER_HEADER_FIELD'], token)
        token = getValidToken(token)

        if token is None or token.id_application !=  g.application.id:
            resp = make_response(json.dumps({'message': 'User token is not valid'}), 403)
            if g.application:
                resp.headers['X-APPLICATION-ID'] = g.application.id
            return resp

        g.token = token
        g.user = dbGetApplicationUser(g.application.id, token.id_user)
        return f(*args, **kwargs)
    return decorated_function

def require_applicationtoken(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        g.application = None
        application = request.cookies.get(app.config['APPLICATION_TOKEN_COOKIE'], app.config['SECRET_KEY'])
        application = request.headers.get(app.config['APPLICATION_HEADER_FIELD'], application)
        application = dbGetApplication(application)

        if application is None:
            resp = make_response(json.dumps({'message': 'Application token is not valid'}), 403)
            return resp

        g.application = application
        return f(*args, **kwargs)
    return decorated_function

def require_staff(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user.is_staff:
            return f(*args, **kwargs)

        resp = make_response(json.dumps({'message': 'Insufficient permissions, you must be a staff or admin'}), 403)
        return resp
    return decorated_function

def require_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user.is_admin:
            return f(*args, **kwargs)

        resp = make_response(json.dumps({'message': 'Insufficient permissions you must be an admin'}), 403)
        return resp
    return decorated_function

def require_superadmin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user.is_superadmin:
            return f(*args, **kwargs)

        resp = make_response(json.dumps({'message': 'Insufficient permissions you must be an superadmin'}), 403)
        return resp
    return decorated_function

