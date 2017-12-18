# -*- coding: utf-8 -*-

from flask_restful import Resource, reqparse, Api, marshal, fields
from flask import abort,url_for, request, render_template, Response
from oauth import app, models, lib
from oauth.decorator import *
import datetime
api = Api(app)

class ClientList(Resource):
    '''
    show user avaible client account
    '''
    pass

class ClientApplication(Resource):
    '''
    Manage application
    '''
    pass

class ClientApplicationList(Resource):
    '''
    List of application
    '''
    pass

class ClientDomain(Resource):
    pass

class ClientDomainList(Resource):
    pass

class ClientDomainEmail(Resource):
    pass

class ClientUser(Resource):
    '''
    Show
    '''
    pass
