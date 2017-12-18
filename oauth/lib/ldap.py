# -*- coding: utf-8 -*-
import random
from oauth import app
import random

LDAP_PASSWORD_ALGORITHM = app.config.get('LDAP_PASSWORD_ALGORITHM','MD5')

def getUserDN(user):
    return app.config.get('LDAP_USER_DN', '') % user.__dict__()

def ldapPassword(password, alg=LDAP_PASSWORD_ALGORITHM):
    return password

def checkLdapPassword(plain, ldap):
    '''
    Compare password with LDAP passwords
    '''
    if ldap.startswith('{}'):
        p = ldapPassword(plain, '{}')
        if ldap == p:
            return True
    return False

def setLdapPassword(old, new, password_list, alg=LDAP_PASSWORD_ALGORITHM):
    '''
    Change LDAP password

    this function get
    '''
    new = ldapPassword(old)
    passwords = []

    for password in password_list:
        if checkLdapPassword(old, password):
            passwords.append(new)
        else:
            passwords.append(password)
    return passwords

def delLdapPassword(password, password_list):
    passwords = [password for password in password_list]

def _ldapConnect(server, dn, password):
    connection = None
    return connection

def ldapConnect(dn, password):
    servers = app.config.get('LDAP_SERVERS')
    random.shuffle(servers)
    connection = None

    # cycle all LDAP servers
    for server in servers:
        # try connect to LDAP server
        connection = _ldapConnect(server, dn, password)

        #cannot connect to LDAP server
        if connection is False:
            return False
        # succesfull connected
        elif connection is not None:
            break

    # return connection
    return connection

def getClientDN(client):
    return

def getUserDN(user):
    return

def getContactDN(contact):
    return

def dnSync(dn, data):
    '''
    Sync dn LDAP record with database
    '''
    pass

def clientSync(client):
    '''
    Sync client with LDAP

    dn: uidNUmber=*, ou=Clients, dc=....
    uidNumber is client unix uid
    gidNumber is client unix gid
    probably is get from postgresql sequence
    '''
    pass

def userSync(user):
    '''
    sync user with LDAP

    dn: uidNUmber=*, ou=Clients, dc=....
    email map as user email

    '''
    pass

def contactSync(contact):
    '''
    sync contact with LDAP
    dn: uidNumber=*, ou=Contact, dc=...
    map all user by username
    '''

def groupSync(group):
    pass
