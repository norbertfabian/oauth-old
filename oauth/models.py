# -*- coding: utf-8 -*-

import hashlib
import random
import string
from sqlalchemy.orm import validates
from sqlalchemy.sql import func

from oauth import app, db
import datetime

DB_TOKEN_LEN = app.config.get('DB_TOKEN_LEN', 64)

def getRandom(N=DB_TOKEN_LEN, choice=app.config.get("RANDOM_CHAR", string.printable)):
    return ''.join(random.choice(choice) for _ in range(N))


class ApplicationUser(db.Model):
    __tablename__ = 'application_user'

    id_application = db.Column(db.Integer, db.ForeignKey('application.id_application'), primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'), primary_key=True)
    id_contact = db.Column(db.Integer, db.ForeignKey('contact.id_contact'))

    email = db.Column(db.String(150))
    phone = db.Column(db.String(20))

    is_staff = db.Column(db.Boolean, server_default='false')
    is_admin = db.Column(db.Boolean, server_default='false')

    application = db.relationship('Application', back_populates='users')
    user = db.relationship('User', back_populates='applications')

    def __repr__(self):
        return '<ApplicationUser %s %s>' % (self.application, self.user)

    def __str__(self):
        return self.display

    def __unicode__(self):
        return self.display

    def __init__(self, application, user, contact=None, email=None, phone=None, is_staff=False, is_admin=False):
        if isinstance(application, int):
            self.id_application = application
        elif isinstance(application, Application):
            self.application = application

        if isinstance(user, int):
            self.id_user = user
        elif isinstance(user, User):
            self.user = user

        if isinstance(contact, Contact):
            self.contact = contact
        elif isinstance(contact, int):
            self.id_contact = contact

        self.is_staff = is_staff
        self.is_admin = is_admin
        self.email = email
        self.phone = phone

class ApplicationContact(db.Model):
    __tablename__ = 'application_contact'

    id_application = db.Column(db.Integer, db.ForeignKey('application.id_application'), primary_key=True)
    id_contact = db.Column(db.Integer, db.ForeignKey('contact.id_contact'), primary_key=True)
    deleted = db.Column(db.Boolean, default=False)

    application = db.relationship('Application', back_populates='applicationcontacts')
    contact = db.relationship('Contact', back_populates='applicationcontacts')

    def __repr__(self):
        return '<ApplicationContact %s %s>' % (self.application, self.contact)

    def __init__(self, application=None, contact=None):
        '''
        Inicialize
        '''
        if isinstance(application, int):
            self.id_application = application
        elif isinstance(application, Application):
            self.application = application

        if isinstance(contact, int):
            self.id_contact = contact
        elif isinstance(contact, Contact):
            self.contact = contact

class ApplicationUserContact(db.Model):
    __tablename__ = 'application_user_contact'

    id_application = db.Column(db.Integer, db.ForeignKey('application.id_application'), primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'), primary_key=True)
    id_contact = db.Column(db.Integer, db.ForeignKey('contact.id_contact'), primary_key=True)

    application = db.relationship('Application', back_populates='applicationusercontacts')
    contact = db.relationship('Contact', back_populates='applicationusercontacts')
    user = db.relationship('User', back_populates='contacts')

    def __repr__(self):
        return '<ApplicationUserContact %s %s %s>' % (self.application, self.user, self.contact)

    def __init__(self, application=None, user=None, contact=None):
        '''
        Inicialize
        '''
        if isinstance(application, int):
            self.id_application = application
        elif isinstance(application, Application):
            self.application = application

        if isinstance(user, int):
            self.id_user = user
        elif isinstance(user, User):
            self.user = user

        if isinstance(contact, int):
            self.id_contact = contact
        elif isinstance(contact, Contact):
            self.contact = contact

class UserClient(db.Model):
    '''
    When user client account
    '''
    __tablename__ = 'user_client'
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'), primary_key=True)
    id_client = db.Column(db.Integer, db.ForeignKey('client.id_client'), primary_key=True)
    date = db.Column(db.DateTime, server_default=func.current_timestamp())

    user = db.relationship('User', back_populates='clients')
    client = db.relationship('Client', back_populates='users')

    def __repr__(self):
        return '<UserClient %s %s>' % (self.user, self.client)

    def __init__(self, user, client):
        self.user = user
        self.client = client

class UserDomain(db.Model):
    '''
    UserDomain membership
    '''
    __tablename__ = 'user_domain'
    SEQUENCE = db.Sequence('user_domain_seq')

    id = db.Column(db.Integer, SEQUENCE, server_default=SEQUENCE.next_value(), primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'), index=True)
    id_domain = db.Column(db.Integer, db.ForeignKey('domain.id_domain'), index=True)
    name = db.Column(db.String(50)) # $name@$domain
    accepted = db.Column(db.Boolean, default=True) # user can decline delivery of email

    user = db.relationship('User', back_populates='domains')
    domain = db.relationship('Domain', back_populates='users')

    def __repr__(self):
        return '<UserDomain %s %s>' % (self.user, self.domain)

    def __init__(self, user=None, domain=None, name=None):
        if isinstance(user, int):
            self.id_user = user
        elif isinstance(user, models.User):
            self.user = user

        if isinstance(domain, int):
            self.id_domain = domain
        elif isinstance(domain, models.Domain):
            self.domain = domain

        self.name = name

USER_SEQ = db.Sequence('user_seq')
class User(db.Model):
    __tablename__ = 'user'
    SEQUENCE = USER_SEQ

    id = db.Column('id_user', db.Integer,SEQUENCE, server_default=SEQUENCE.next_value(), primary_key=True)
    id_contact = db.Column(db.Integer, db.ForeignKey("contact.id_contact"), nullable=True)
    is_device = db.Column(db.Boolean, server_default='false')
    is_superadmin = db.Column(db.Boolean, default=False)

    username = db.Column(db.String(50), unique=True, index=True)
    password = db.Column(db.String(64))
    validation_type = db.Column(db.Integer)
    registered = db.Column(db.DateTime, server_default=func.current_timestamp(), nullable=False)

    clients = db.relationship('UserClient', back_populates='user')
    applications = db.relationship('ApplicationUser', back_populates='user')
    contacts =  db.relationship('ApplicationUserContact', back_populates='user')
    domains = db.relationship('UserDomain', back_populates='user')
    contact = db.relationship('Contact', back_populates='contacusers')
    tokens = db.relationship('Token', back_populates='user')
    validations = db.relationship('Validation', back_populates='user')

    def __repr__(self):
        return '<User %s>' % (self.username)

    def __str__(self):
        return self.username

    def __unicode__(self):
        return  self.username

    def __init__(self, username, password, contact=None, is_device=False, is_superadmin=False):
        self.username = username
        self.password = password
        self.is_device = is_device
        self.is_superadmin = is_superadmin

        if isinstance(contact, int):
            self.id_contact = contact
        elif isinstance(contact, Contact):
            self.contact = contact

CLIENT_SEQ = db.Sequence('client_seq')
class Client(db.Model):
    __tablename__ = 'client'
    SEQUENCE = CLIENT_SEQ

    id = db.Column('id_client', db.Integer, SEQUENCE, server_default=SEQUENCE.next_value(), primary_key=True)
    id_contact = db.Column(db.Integer, db.ForeignKey("contact.id_contact"), nullable=True)

    display = db.Column(db.String(50))
    uid = db.Column(db.Integer, nullable=True, unique=True)
    gid = db.Column(db.Integer, nullable=True)

    contact = db.relationship('Contact', back_populates='contacclients')
    applications = db.relationship('Application', back_populates='client')
    users = db.relationship('UserClient', back_populates='client')
    domains = db.relationship('Domain', back_populates='client')

    def __repr__(self):
        return '<Client %s>' % (self.display)

    def __init__(self, display, contact=None, uid=None, gid=None):
        self.display = display
        if isinstance(contact, int):
            self.id_contact = contact
        elif contact is not None:
            self.contact = contact

        # gen from LDAP lib
        self.uid = uid
        self.gid = gid

DOMAIN_SEQ = db.Sequence('domain_seq')
class Domain(db.Model):
    __tablename__ = 'domain'
    SEQUENCE = DOMAIN_SEQ
    id_domain = db.Column(db.Integer, SEQUENCE, server_default=SEQUENCE.next_value(), primary_key=True)
    name = db.Column(db.String(150), unique=True)
    id_client = db.Column(db.Integer, db.ForeignKey('client.id_client'), index=True)
    validated = db.Column(db.Boolean, server_default='false', default=False)

    client = db.relationship('Client', back_populates='domains')
    users = db.relationship('UserDomain', back_populates='domain')

    def __repr__(self):
        return '<Domain %r>' % self.domain

    def __str__(self):
        return  self.domain

    def __init__(self, name, client, validated=False):
        self.name = name
        self.client = client
        self.validated = validated

APPLICATION_SEQ = db.Sequence('application_seq')
class Application(db.Model):
    __tablename__ = 'application'
    SEQUENCE = APPLICATION_SEQ

    id = db.Column('id_application', db.Integer,SEQUENCE, server_default=SEQUENCE.next_value(), primary_key=True)
    oauth = db.Column(db.Boolean, server_default='false')
    id_client = db.Column(db.Integer, db.ForeignKey("client.id_client"))

    title = db.Column(db.String(50), nullable=False)
    token = db.Column(db.String(DB_TOKEN_LEN), default=getRandom, nullable=False, unique=True)
    created = db.Column(db.DateTime, nullable=False, server_default=func.current_timestamp())
    active = db.Column(db.Boolean, server_default='true')
    expiration = db.Column(db.DateTime)
    return_path = db.Column(db.String(200))
    conf = db.Column(db.String())

    # Payment options, experimental
    calc_user = db.Column(db.Boolean, server_default='false')
    payment = db.Column(db.Integer, server_default='0') # amount per period
    period = db.Column(db.Integer, server_default='0') # days of period

    alive = db.Column(db.Integer) # how long token live (second), None is infinity
    restore = db.Column(db.Integer) # how frequently ask application per validity (second), None is infinity

    client = db.relationship('Client', back_populates='applications')
    tokens = db.relationship('Token', back_populates='application')
    users = db.relationship('ApplicationUser', back_populates='application')
    applicationusercontacts = db.relationship('ApplicationUserContact', back_populates='application')
    applicationcontacts = db.relationship('ApplicationContact', back_populates='application')

    def __repr__(self):
        return '<Application %s>' % (self.title)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return  self.title

    def __init__(self, client, title, token=None, oauth=False):
        '''
        Init arguments
        '''
        if isinstance(client, int):
            self.id_client = client
        else:
            self.client = client

        self.title = title
        if token is None:
            token = getRandom(DB_TOKEN_LEN)
        self.token = token
        self.oauth = oauth

TOKEN_SEQ = db.Sequence('token_seq')
class Token(db.Model):
    __tablename__ = 'token'
    SEQUENCE = TOKEN_SEQ

    id = db.Column('id_token', db.Integer, SEQUENCE, server_default=SEQUENCE.next_value(), primary_key=True)
    id_application = db.Column(db.Integer, db.ForeignKey("application.id_application"), index=True)
    id_user = db.Column(db.Integer, db.ForeignKey("user.id_user"), index=True)

    validated = db.Column(db.Boolean())
    token = db.Column(db.String(DB_TOKEN_LEN), default=getRandom, unique=True)

    application = db.relationship('Application', back_populates='tokens')
    user = db.relationship('User', back_populates='tokens')

    created = db.Column(db.DateTime, server_default=func.current_timestamp())
    last_activity = db.Column(db.DateTime, server_default=func.current_timestamp())
    expiration = db.Column(db.DateTime) # last activity + application.alive

    def __repr__(self):
        return '<Token %s %s %s>' % (self.application, self.user, self.token)

    def __str__(self):
        return self.token

    def to_dict(self):
        return {
                    'id': self.id,
                    'id_application': self.id_application,
                    'id_user': self.id_user,
                    'validated': self.validated,
                    'token': self.token,
                    'created': self.created,
                    'last_activity': self.last_activity,
                    'expiration': self.expiration,
        }

    def __init__(self, application, user, expiration=None):
        self.application = application
        self.user = user
        self.expiration = expiration
        if application.oauth:
            self.validated = True

VALIDATION_SEQ = db.Sequence('validation_seq')
class Validation(db.Model):
    __tablename__ = 'validation'
    SEQUENCE = VALIDATION_SEQ

    id = db.Column('id_validation', db.Integer, SEQUENCE, server_default=SEQUENCE.next_value(), primary_key=True)
    id_user = db.Column('id_user', db.Integer, db.ForeignKey("user.id_user"), index=True)

    secret = db.Column(db.String(10), index=True) # secret send by another way
    expiration = db.Column(db.DateTime)
    use = db.Column(db.DateTime)

    user = db.relationship(User, back_populates='validations')

    def __repr__(self):
        return '<Validation %r %r %r>' % (self.user, self.expiration, self.user)

    def __str__(self):
        return self.secret

    def __init__(self, user, expiration=None, secret=None):
        if secret is None:
            secret = getRandom(6)
        self.user = user
        self.expiration = None
        self.secret = secret

CONTACT_SEQ = db.Sequence('contact_seq')
class Contact(db.Model):
    __tablename__ = 'contact'
    SEQUENCE = CONTACT_SEQ

    HASH_FIELDS = ['company', 'first_name', 'last_name', 'www', 'gsm', 'email', 'custom_id', 'ic', 'dic', 'street', 'city', 'zip', 'bank_account', 'bank_code' ,'iban']

    id = db.Column('id_contact', db.Integer, SEQUENCE, server_default=SEQUENCE.next_value(), primary_key=True)
    company = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    www =  db.Column(db.String(100))
    gsm =  db.Column(db.String(20))
    email = db.Column(db.String(100))
    custom_id = db.Column(db.String(20))
    ic = db.Column(db.String(20))
    dic = db.Column(db.String(20))
    street = db.Column(db.String(100))
    city = db.Column(db.String(50))
    zip = db.Column(db.String(10))
    bank_account = db.Column(db.String(50))
    bank_code = db.Column(db.String(50))
    iban = db.Column(db.String(50))
    date = db.Column(db.DateTime(timezone=True), server_default=func.current_timestamp())
    hash = db.Column(db.String(DB_TOKEN_LEN), unique=True)

    contacusers = db.relationship('User', back_populates='contact')
    contacclients = db.relationship('Client', back_populates='contact')

    applicationusercontacts = db.relationship('ApplicationUserContact', back_populates='contact')
    applicationcontacts = db.relationship('ApplicationContact', back_populates='contact')

    def __str__(self):
        if self.company is not None:
            return self.company
        return '%s %s' % (self.first_name, self.last_name)

    def __init__(self, **kwargs):
        self.company = kwargs.get('company', 'My company')
        self.first_name = kwargs.get('first_name', 'MyName')
        self.last_name = kwargs.get('last_name', 'MySurename')
        self.www = kwargs.get('www', 'http://example.com')
        self.email = kwargs.get('email', 'example@example.com')

        for field in Contact.HASH_FIELDS:
            if field in kwargs:
                setattr(self, field, kwargs[field])

    #@validates
    #def validate_email(self, key, address):
        #assert '@' in address
        #return address

    @property
    def to_dict(self):
        return {k:getattr(self, k) for k in Contact.HASH_FIELDS+['id']}

    def getHash(self):
        hash = hashlib.md5()
        for key in Contact.HASH_FIELDS:
            value = getattr(self, key)
            if isinstance(value, str):
                hash.update(value)
            elif isinstance(value, unicode):
                hash.update(value.encode('utf8'))

        return hash.hexdigest()
