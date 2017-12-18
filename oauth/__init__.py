# -*- coding: utf-8 -*-

import os
import sys
import logging
from logging.handlers import SMTPHandler

from flask import Flask, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, static_path='/static')
app.config.from_object('oauth.config')

if os.environ.get('OAUTH_SETTINGS'):
    app.config.from_envvar('OAUTH_SETTINGS')

db = SQLAlchemy(app)

from oauth import models
from oauth import lib

if not app.debug:
    ADMINS = ['euro@profires.cz']
    mail_handler = SMTPHandler('mail.profires.cz',
                               'pool1@profires.cz',
                               ADMINS, 'oAuth application failed')
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

from oauth import rest
from oauth import html
from oauth import soap

from oauth.command import manager
