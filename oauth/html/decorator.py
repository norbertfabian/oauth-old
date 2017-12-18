# -*- coding: utf-8 -*-

from flask import request, g
from oauth import app, lib

def login_required(f):
    def wrap(neco):
        return f(neco)
    return wrap()
