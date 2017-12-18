# -*- coding: utf-8 -*-
from oauth import app, db, models

def getDomain(domain):
    '''
    Get domain by ID or NAME
    '''
    pass

def registerDomain(client, name):
    '''
    register new client domain
    '''
    pass

def hasDomain(domain, user=None, id_user=None, client=None, id_client=None):
    '''
    Check, if client own domain
    '''
    if user is None and id_user is None and client is None and id_client is None:
        raise Exception("You must specivy owner")



def delDomain(domain):
    '''
    Remove client domain
    '''
    pass


def addDomain(client, name):
    pass
