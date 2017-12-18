# -*- coding: utf-8 -*-

from flask_restful import Resource, Api, marshal, fields
from flask import abort
from oauth import app
from oauth import lib

api = Api(app)

__all__ = []


from oauth.rest import token
from oauth.rest import application
from oauth.rest import user
from oauth.rest import client
from oauth.rest import contact
