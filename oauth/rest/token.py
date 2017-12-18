# -*- coding: utf-8 -*-

import json
import datetime

from flask_restful import Resource, reqparse, Api, marshal, fields
from flask import abort,url_for, request, render_template, make_response, Response

from oauth import app, models, lib
from oauth.decorator import *
api = Api(app)

class ApplicationToken(Resource):
    @require_applicationtoken
    @require_usertoken
    def get(self):
        return 'token_list'

class ApplicationTokenArg(Resource):
    @require_applicationtoken
    @require_usertoken
    def get(self, arg):
            if arg == u'current':
                t = g.token
                return {
                            'id': t.id,
                            'id_application': t.id_application,
                            'id_user': t.id_user,
                            'token': t.token,
                            'validated': t.validated,
                            'last_activity': t.last_activity.isoformat() if t.last_activity else None,
                            'expiration': t.expiration.isoformat() if t.expiration else None,
                            'username': t.username,
                            'title': t.title,
                            'is_device': t.is_device,
                            'is_staff': t.is_staff or t.is_admin or t.is_superadmin,
                            'is_admin': t.is_admin or t.is_superadmin,
                            'alive': t.alive,
                    }

api.add_resource(ApplicationToken, '/api/rest/token/', endpoint='rest.application.token')
api.add_resource(ApplicationTokenArg, '/api/rest/token/<arg>/', endpoint='rest.application.token-arg')
