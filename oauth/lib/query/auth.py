# -*- coding: utf-8 -*-
import datetime
from sqlalchemy import or_, update
from oauth import app, db
from oauth import models

from oauth.lib.query.user import dbGetUserId, dbGetUser, dbAddApplicationUser
from oauth.lib.query.application import dbGetApplication
from oauth.lib.ldap import ldapPassword

__all__ = ['dbAuthenticate', 'dbValidate', 'dbAddValidation', 'dbGetValidToken', 'dbGetUserToken', 'dbRemoveToken']

def dbAuthenticate(username, password):
    '''
    Authenticate user by database

    fallback password validation
    '''
    return models.User.query.filter_by(username=username, password=ldapPassword(password)).one_or_none()

def dbValidate(user, secret):
    '''
    Validate user by validation table
    '''
    id_user = dbGetUserId(user)
    if id_user is None:
        return
    validation = models.Validation.query.filter_by(id_user=id_user, secret=secret, use=None).filter(db.or_(models.Validation.expiration >= datetime.datetime.now(), models.Validation.expiration==None)).one_or_none()
    if validation is not None:
        validation.use = datetime.datetime.now()
        db.session.add(validation)
        db.session.commit()
    return validation

def dbAddValidation(user, secret=None, expiration=None):
    user = dbGetUser(user)
    if isinstance(user, models.User):
        validation = models.Validation(user, secret, expiration)
        db.session.add(validation)
        db.session.commit()
        return validation
    return None

def dbGetValidToken(token):
    '''
    Get user by valid token
    '''
    if token is None:
        return None

    now = datetime.datetime.now()
    token = db.session.query(
                                models.Token.id,
                                models.Token.id_application,
                                models.Token.id_user,
                                models.Token.validated,
                                models.Token.last_activity,
                                models.Token.expiration,
                                models.Token.token,
                                models.User.username,
                                models.User.is_superadmin,
                                models.User.is_device,
                                models.ApplicationUser.is_staff,
                                models.ApplicationUser.is_admin,
                                models.Application.alive,
                                models.Application.title,
                            ).filter(
                                models.Token.token==token,
                                or_(models.Token.expiration>=now, models.Token.expiration==None),
                                models.ApplicationUser.id_user==models.Token.id_user,
                                models.ApplicationUser.id_application==models.Token.id_application,
                                models.Token.id_user==models.User.id,
                                models.Application.id==models.Token.id_application,
                            ).one_or_none()

    if token is not None:
        last_activity = now
        expiration = None
        if token.expiration is not None:
            expiration = now + datetime.timedelta(0, token.application.alive)

        update(models.Token).values(
                                        last_activity=last_activity,
                                        expiration=expiration,
                                        ).where(models.Token.id==token.id)
        db.session.commit()
        db.session.flush()
    return token

def dbGetUserToken(user, application, create=True):
    '''
    Get user token for application,
    '''
    user = dbGetUser(user)
    if user is None:
        return None

    application = dbGetApplication(application)
    if application is None:
        return None

    expiration = None
    if application.alive:
        expiration = datetime.datetime.now() + datetime.timedelta(0, application.alive)

    token = models.Token(application, user, expiration)

    dbAddApplicationUser(application, user, user.contact.email if user.contact is not None else None)

    db.session.add(token)
    db.session.commit()
    return token

def dbRemoveToken(token):
    if isinstance(token, models.Token):
        db.session.delete(token)

    elif isinstance(token, int):
        db.session.query(models.Token).filter_by(id=token).delete()

    elif isinstance(token, str) or isinstance(token, unicode):
        db.session.query(models.Token).filter_by(token=token).delete()
    else:
        return False
    db.session.commit()
    return True
