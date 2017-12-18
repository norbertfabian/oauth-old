# -*- coding: utf-8 -*-
from oauth import app, db, models

__all__ = [
                'dbAddContact', 'dbAddApplicationContact', 'dbHideApplicationContact', 'dbGetContactByIC', 'dbGetContactByDIC', 'dbGetApplicationContact', 'dbSetApplicationUserContact', 'dbGetApplicationContactList',
                'search', 'serachUser', 'searchApplication', 'searchClient'
        ]

def dbAddContact(**kwargs):
    '''
    Create contact information
    '''
    tmp = models.Contact(**kwargs)
    hash = tmp.getHash()
    contact = models.Contact.query.filter_by(hash=hash).one_or_none()
    if contact is None:
        tmp.hash = hash
        db.session.add(tmp)
        db.session.commit()
        contact = tmp
    return contact

def dbAddApplicationContact(id_application, id_contact):
    if isinstance(id_contact, models.Contact):
        id_contact = id_contact.id

    application_contact = models.ApplicationContact.query.filter_by(id_application=id_application, id_contact=id_contact).one_or_none()
    if application_contact is None:
        db.session.add(models.ApplicationContact(id_application, id_contact))
        db.session.commit()

def dbHideApplicationContact(id_application, id_contact):
    if isinstance(id_contact, models.Contact):
        id_contact = id_contact.id

    if isinstance(id_application, models.Application):
        id_application = id_application.id

    models.ApplicationContact.query.filter(
        models.ApplicationContact.id_application==id_application,
        models.ApplicationContact.id_contact==id_contact
    ).update({'deleted': True})
    return True


def dbSetApplicationUserContact(id_application, id_user, id_contact):
    '''
    Set user contact
    '''
    if isinstance(id_user, models.User):
        id_user = id_user.id

    if isinstance(id_application, models.Application):
        id_application = id_application.id

    if isinstance(id_contact, models.Contact):
        id_contact = id_contact.id

    elif isinstance(id_contact, int):
        id_contact = id_contact

    if id_user is None or id_application is None or id_contact is None:
        return None

    application_user = models.ApplicationUser.query.filter_by(id_application=id_application, id_user=id_user).one()
    application_user_contact = models.ApplicationUserContact.query.filter_by(id_application=id_application, id_user=id_user, id_contact=id_contact).one_or_none()
    dbAddApplicationContact(id_application, id_contact)

    application_user.id_contact = id_contact

    if application_user_contact is None:
        application_user_contact = models.ApplicationUserContact(id_application, id_user, id_contact)
    else:
        application_user_contact.id_contact = id_contact

    db.session.add(application_user)
    db.session.add(application_user_contact)
    db.session.commit()
    return application_user

def dbGetContactByIC(ic):
    return models.Contact.query.filter_by(ic=ic).order_by(models.Contact.id.desc()).limit(1).one_or_none()

def dbGetContactByDIC(dic):
    return models.Contact.query.filter_by(dic=dic).order_by(models.Contact.id.desc()).limit(1).one_or_none()

def search(*args, **kwargs):
    pass

def serachUser(user, *args, **kwargs):
    pass

def dbGetApplicationContact(id_application, id_contact):
    if isinstance(id_application, models.Application):
        id_application = id_application.id

    if isinstance(id_contact, models.Contact):
        id_contact = id_contact.id

    return models.Contact.query.join(
                                    models.ApplicationContact
                                ).filter(
                                    models.ApplicationContact.id_application==id_application,
                                    models.ApplicationContact.id_contact==id_contact
                                ).limit(1).one_or_none()

def dbGetApplicationContactList(id_application):
    if isinstance(id_application, models.Application):
        id_application = id_application.id

    return models.Contact.query.join(
                                    models.ApplicationContact
                                ).filter(
                                    models.ApplicationContact.id_application==id_application,
                                    models.ApplicationContact.deleted==False
                                ).all()

def searchApplication(application, *args, **kwargs):
    pass

def searchClient(client, *args, **kwargs):
    pass


