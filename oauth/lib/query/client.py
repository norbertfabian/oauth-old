# -*- coding: utf-8 -*-
from oauth import app, db, models
from oauth.lib.query.user import dbGetUserId

__all__ = ['registerClient', 'registerApplication', 'getClient', 'getClientUsers', 'getClientDomains', 'getClientApplications', 'getAllUserContacts']

def registerClient(display, user):
    user_id = dbGetUserId(user)
    db.session.begin_nested()
    client = models.Client(display, user.contact)
    db.session.add(client)
    db.session.commit()


def registerApplication(client, title, token=None):
    application = models.Application(client, title)
    return application

def getClient(client):
    pass


def getClientUsers(client):
    '''
    get all client user
    '''
    pass

def getClientDomains(client):
    '''
    Get all user domains
    '''
    pass


def getClientApplications(client):
    '''
    Get all user applications
    '''
    pass


def getAllUserContacts(client):
    '''
    Get all user contacts
    '''

    # traverse thourht applications
    pass

