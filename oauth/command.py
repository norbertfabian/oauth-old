# -*- coding: utf-8 -*-
import imp
import os.path
from flask.ext.script import Shell, Manager
from flask.ext.migrate import Migrate,MigrateCommand

from oauth import app, db
import models, lib
from test import *

manager = Manager(app)

@manager.command
def create():
    db.create_all()
    contact = lib.dbAddContact()

    client = models.Client('Admin', contact); db.session.add(client)
    user = models.User('admin', 'admin', contact=contact); db.session.add(user)
    application = models.Application(client, 'OAuth', app.config.get('SECRET_KEY'), oauth=True); application.id = app.config['APPLICATION_ID']; db.session.add(application)

    db.session.add(models.ApplicationUser(application, user, email=app.config['ADMIN_EMAIL'], is_staff=True, is_admin=True))
    db.session.add(models.UserClient(user, client))
    db.session.add(models.Domain("test.cz", client))
    db.session.commit()

@manager.option('-u', '--username', dest='username', required=True)
@manager.option('-p', '--password', dest='password', required=True)
def register_user(username, password):
    user = lib.registerUser(username, password)
    print user.username

@manager.command
def create_contact(**kwargs):
    contact = lib.createContact(**kwargs)
    return contact.id


def _make_context():
    return dict(app=app, db=db, models=models, lib=lib)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
manager.add_command("shell", Shell(banner=app.config.get("SHELL_BANNER"), make_context=_make_context))
