import datetime

from flask_restful import Resource, reqparse, Api, marshal, fields, inputs
from flask import g, abort,url_for, request, render_template, Response
from oauth import app
from oauth import models, lib
from oauth.decorator import *

api = Api(app)

__all__ = []


add_device_parser = reqparse.RequestParser()
add_device_parser.add_argument('is_admin', default=False, type=bool, help='If is creating basic device')

class AddDevice(Resource):
    @require_applicationtoken
    @require_usertoken
    @require_admin
    def post(self):
        args = add_device_parser.parse_args()
        device = lib.registerDevice()
        t = lib.deviceAddApplication(device, g.application, is_admin=args['is_admin'])
        return  {
                            'id': t.id,
                            'id_application': t.id_application,
                            'id_user': t.id_user,
                            'token': t.token,
                            'is_admin': args['is_admin'],
                    }


api.add_resource(AddDevice, '/api/rest/application/add_device/', endpoint='rest.application.add-device')

