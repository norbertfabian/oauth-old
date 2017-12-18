# -*- coding: utf-8 -*-
from flask import render_template, current_app, _app_ctx_stack as stack
from flask.ext.mail import Mail, Message
from psycopg2 import IntegrityError
from oauth import app, db, models
from oauth.lib import query
from sqlalchemy.exc import IntegrityError

mail = Mail(app)

__all__ = [
            'registerUser', 'registerDevice', 'deviceAddApplication', 'sentRegistratinoEmail', 'sentRegistratinoEmail',
            'validate','getValidation', 'getUserToken', 'authenticate', 'getValidToken', 'removeToken',
            'removeApplication', 'removeUser', 'removeClient', 'removeToken', 'sendValidation', 'sendValidationEmail',
        ]

class Auth(object):
    def __init__(self, app=None):
        self.app = app

    def isOAthAdmin(user):
        '''
        Check, if user can do oauth staff
        '''
        ctx = stack.top()
        return False

def registerUser(username, email, password):
    '''
    Create new User
    '''
    contact = query.dbAddContact(email=email, first_name=username, last_name=username)
    user = query.dbAddUser(username, email, password, contact)
    validation = query.dbAddValidation(user)
    application_user = query.dbAddApplicationUser(app.config['APPLICATION_ID'], user, contact, email=email)
    query.dbSetApplicationUserContact(app.config['APPLICATION_ID'], user, contact)
    sentRegistratinoEmail(user, application_user, validation)
    return user

def registerDevice():
    '''
    Create new Device
    '''
    user = None
    while True:
        try:
            username = models.getRandom(50)
            password = models.getRandom(64)
            contact = None
            user = query.dbAddUser(username, password, is_device=True)
            break
        except IntegrityError as e:
            continue

    return user

def deviceAddApplication(device, application, is_admin=False):
    query.dbAddApplicationUser(application, device, is_admin=is_admin)
    token = models.Token(application, device)
    db.session.add(token)
    db.session.commit()
    return token


def sentRegistratinoEmail(user, application_user, validation):
    msg = Message("Registration oAuth",
                  sender=app.config['DEFAULT_MAIL_SENDER'],
                  recipients=[application_user.email])
    params = {'user': user, 'secret': validation.secret, 'email': application_user.email}
    msg.body = render_template('email/registration.txt', **params)
    msg.html = render_template('email/registration.html', **params)
    mail.send(msg)


def authenticate(username, password):
    return query.dbAuthenticate(username, password)

def validate(user, secret):

    user = query.dbGetUserId(user)
    if user is None:
        return None, None

    validation = query.dbValidate(user, secret)
    if validation:
        token = query.dbGetUserToken(user, app.config['APPLICATION_ID'])
        return user, token

    return None, None

def sendValidation(user, duration=None):
    if user.validation_type == 1:
        return sendValidationEmail(user, duration)
    elif user.validation_type == 2:
        return sendValidationSMS(user, duration)
    if user.validation_type == 3:
        validation = getValidation(user, duration)
        return app.logger.info("SECRET: %s", validation.secret)

def sendValidationEmail(user, duration=None):
    validation = getValidation(user, duration)
    msg = Message("Validation",
                  sender=app.config['DEFAULT_MAIL_SENDER'],
                  recipients=[user.email])
    params = {'user': user, 'email': user.email, 'secret': validation.secret}
    msg.body = render_template('email/validation.txt', **params)
    msg.html = render_template('email/validation.html', **params)
    mail.send(msg)
    return validation

def sendValidationEmail(user, duration=None):
    validation = getValidation(user, duration)
    sms = {}
    return validation

def getValidation(user, duration=None):
    user = query.dbGetUser(user)
    if user is None:
        return None
    return query.dbAddValidation(user)

def getUserToken(user, application=app.config['APPLICATION_ID']):
    return query.dbGetUserToken(user, application)


def getValidToken(token):
    return query.dbGetValidToken(token)

def removeToken(token):
    return query.dbRemoveToken(token)

def removeApplication(application):
    pass

def removeUser(user):
    pass

def removeClient(client):
    pass
