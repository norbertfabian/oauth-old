# -*- coding: utf-8 -*-
import json
import datetime

from flask_restful import Resource, reqparse, Api, marshal, fields
from flask import abort,url_for, request, render_template, make_response, Response

from oauth import app, models, lib
from oauth.decorator import *
api = Api(app)

user_parser = reqparse.RequestParser()
user_parser.add_argument('app', type=int)
user_parser.add_argument('user', type=str)

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'is_device': fields.Boolean,
    'is_staff': fields.Boolean,
    'is_admin': fields.Boolean,
    }

def user2dict(user):
    return {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'phone': user.phone,
                'is_device': user.is_device,
                'is_staff': user.is_staff or user.is_superadmin,
                'is_admin': user.is_admin or user.is_superadmin,
                'is_superadmin': user.is_superadmin,
                'id_contact': user.id_contact,
            }

class ApplicationUser(Resource):
    @require_applicationtoken
    @require_usertoken
    def get(self):
        if g.user.is_staff:
            return [user2dict(row) for row in lib.dbGetApplicationUserList(g.application.id)]

    @require_applicationtoken
    @require_usertoken
    def post(self):
        pass

class ApplicationUserArg(Resource):

    @require_applicationtoken
    @require_usertoken
    def get(self, arg):
        if isinstance(arg, unicode):
            if arg.isdigit():
                id = int(arg)
                if id == g.user.id:
                    # object is alredy cached
                    return user2dict(g.user)
                return require_staff(self.retrieve)(int(arg))

            elif arg == u'current':
                return user2dict(g.user)

        resp = make_response(json.dumps({'message': 'User %s not found' % arg}), 404)
        return resp


    def retrieve(self, id):
        query = lib.dbGetApplicationUser(g.application.id, id)
        if not query:
            resp = make_response(json.dumps({'message': 'User %d not found' % id}), 404)
            return resp

        response = user2dict(query)

        return response

#class RegisterDevice(Resource):
    #'''
    #'''
    #def post(self):
        #device = lib.registerDevice()
        #return {'device': device.username}

#api.add_resource(RegisterDevice, '/api/rest/register_device/', endpoint='rest.user.register-device')
api.add_resource(ApplicationUser, '/api/rest/user/', endpoint='rest.user.user-list')
api.add_resource(ApplicationUserArg, '/api/rest/user/<arg>/', endpoint='rest.user.user')

#class UserDetail(Resource):
    #'''
    #Core user attributes
    #'''
    #@require_usertoken
    #def get(self):
        #return False

    #@require_usertoken
    #def post(self):
        #return False

#class UserContact(Resource):
    #'''
    #Base contact for user
    #'''
    #@require_usertoken
    #def get(self):
        #return False

    #@require_usertoken
    #def post(self):
        #return False


#class UserApplicationContact(Resource):
    #'''
    #Manage contact in application
    #'''
    #@require_usertoken
    #def get(self):
        #return False

    #@require_usertoken
    #def get(self):
        #return False


#class UserApplication(Resource):
    #'''
    #Show application detail
    #'''
    #@require_usertoken
    #def get(self):
        #return False

#class UserApplicationList(Resource):
    #'''
    #Show list of all enabled application
    #'''
    #pass

#class UserEmail(Resource):
    #'''
    #Show all email valid for user account
    #'''
    #pass

#class UserClient(Resource):
    #'''
    #Posibility to create client account
    #'''
    #pass

#api.add_resource(UserSomething, '/api/rest/application/user/', endpoint='rest.application.user')
