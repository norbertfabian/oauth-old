from flask_restful import Resource, reqparse, Api, marshal, fields
from flask import g, abort,url_for, request, render_template, Response
from oauth import app, models, lib
from oauth.decorator import *
import datetime

api = Api(app)

__all__ = []

contact_fields = {
    'id': fields.Integer,
    'company': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'www': fields.String,
    'gsm': fields.String,
    'email': fields.String,
    'ic': fields.String,
    'dic': fields.String,
    'custom_id': fields.String,
    'street': fields.String,
    'city': fields.String,
    'zip': fields.String,
    'bank_account': fields.String,
    'bank_code': fields.String,
    'iban': fields.String,
    'date': fields.DateTime(dt_format='iso8601'),
}

contact_fields_parser = reqparse.RequestParser()
contact_fields_parser.add_argument('id')
contact_fields_parser.add_argument('company')
contact_fields_parser.add_argument('first_name')
contact_fields_parser.add_argument('last_name')
contact_fields_parser.add_argument('www')
contact_fields_parser.add_argument('gsm')
contact_fields_parser.add_argument('email')
contact_fields_parser.add_argument('ic')
contact_fields_parser.add_argument('dic')
contact_fields_parser.add_argument('custom_id')
contact_fields_parser.add_argument('street')
contact_fields_parser.add_argument('city')
contact_fields_parser.add_argument('zip')
contact_fields_parser.add_argument('bank_account')
contact_fields_parser.add_argument('bank_code')
contact_fields_parser.add_argument('iban')

class RestContactByIC(Resource):

    def get(self, ic):
        contact = lib.getContactByIC(ic)
        if contact is None or not isinstance(contact.id, int):
            return {'ic': 'Resource does not exists'}, 404

        return marshal(contact.__dict__, contact_fields)

class RestContactByDIC(Resource):

    def get(self, dic):
        return {'sdsd': 'sdfas'}

class ApplicationContact(Resource):

    @require_applicationtoken
    @require_usertoken
    def get(self):
        return [row.to_dict for row in lib.dbGetApplicationContactList(g.application.id)]

    @require_applicationtoken
    @require_usertoken
    def post(self):
        contact = contact_fields_parser.parse_args()
        contact = lib.dbAddContact(**contact)
        lib.dbAddApplicationContact(g.application.id, contact.id)
        return {k:getattr(contact, k) for k in models.Contact.HASH_FIELDS+['id']}

class ApplicationContactArg(Resource):

    @require_applicationtoken
    def get(self, arg):
        contact = lib.dbGetApplicationContact(g.application.id, arg)
        if contact is not None:
            return {k:getattr(contact, k) for k in models.Contact.HASH_FIELDS+['id']}

    @require_applicationtoken
    @require_usertoken
    def post(self, arg):
        lib.dbHideApplicationContact(g.application.id, arg)
        new = contact_fields_parser.parse_args()
        contact = lib.dbAddContact(**new)
        lib.dbAddApplicationContact(g.application.id, contact.id)

        return {k:getattr(contact, k) for k in models.Contact.HASH_FIELDS+['id']}


api.add_resource(ApplicationContact, '/api/rest/applicationcontact/', endpoint='rest.application.contact')
api.add_resource(ApplicationContactArg, '/api/rest/applicationcontact/<arg>/', endpoint='rest.application.contact-arg')
api.add_resource(RestContactByIC, '/api/rest/contact/ic/<ic>/')
api.add_resource(RestContactByDIC, '/api/rest/contact/dic/<dic>/')
