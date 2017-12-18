# -*- coding: utf-8 -*-
import datetime
from flask import render_template, after_this_request, g
from sqlalchemy import or_
from oauth import app, lib, models

__all__ = ['emailRegistration']

@app.route('/email/registration/<int:id_user>/<type>', methods=['get'])
def emailRegistration(id_user=None, type='html'):

    @after_this_request
    def contentType(response):
        if type=='txt':
            response.mimetype='text/plain'
        return response

    user = lib.dbGetUser(id_user)
    now = datetime.datetime.now()
    secret = models.Validation.query.filter_by(user=user).filter(
                                                                    or_(models.Validation.expiration>now,models.Validation.expiration==None),
                                                                    models.Validation.use == None
                                                                ).order_by(models.Validation.id).one_or_none()
    if secret is not None:
        secret = secret.secret

    if user is None:
        return u"Uživatel neexistuje"

    email = None
    if user.contact:
        email = user.contact.email

    data = {'subject': 'Registrace', 'user': user, 'email': email, 'secret': secret}

    if type == 'txt':
        return render_template("email/registration.txt", **data)
    if type == 'html':
        return render_template("email/registration.html", **data)

@app.route('/email/validation/<int:id_user>/<type>', methods=['get'])
def emailValidation(id_user=None, type='html'):

    @after_this_request
    def contentType(response):
        if type=='txt':
            response.mimetype='text/plain'
        return response

    user = lib.dbGetUser(id_user)
    now = datetime.datetime.now()
    secret = models.Validation.query.filter_by(user=user).filter(
                                                                    or_(models.Validation.expiration>now,models.Validation.expiration==None),
                                                                    models.Validation.use == None
                                                                ).order_by(models.Validation.id).one_or_none()
    if secret is not None:
        secret = secret.secret

    if user is None:
        return u"Uživatel neexistuje"

    email = None
    if user.contact:
        email = user.contact.email

    data = {'subject': 'Validace', 'user': user, 'email': email, 'secret': secret}

    if type == 'txt':
        return render_template("email/validation.txt", **data)
    if type == 'html':
        return render_template("email/validation.html", **data)
