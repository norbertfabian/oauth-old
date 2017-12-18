# -*- coding: utf-8 -*-
from oauth import app, db, models

__all__ = ['dbGetApplicationId', 'dbGetApplication', 'dbGetUserApplications', 'dbGetClientApplications']

def dbGetApplicationId(application):
    '''
    Get id of application by variable
    '''
    if isinstance(application, int):
        return application
    if isinstance(application, models.Application):
        return application.id
    if isinstance(application, str) or isinstance(application, unicode):
        application = models.Application.query.filter_by(token=application).one_or_none()
        if application is not None:
            return application.id
    return None


def dbGetApplication(application):
    '''
    '''
    if isinstance(application, models.Application):
        return application
    if isinstance(application, int):
        return models.Application.query.filter_by(id=application).one_or_none()
    if isinstance(application, str) or isinstance(application, unicode):
        return models.Application.query.filter_by(token=application).one_or_none()

    return None


def dbGetUserApplications(user):
    pass


def dbGetClientApplications(client):
    pass



