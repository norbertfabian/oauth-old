# -*- coding: utf-8 -*-
from oauth import app, db, models
from oauth.lib.ldap import ldapPassword
from oauth.lib.query.contact import dbAddContact
from sqlalchemy.exc import IntegrityError

def dbAddUser(username, password, contact=None, is_device=False, is_superadmin=False):
    '''
    Register new user
    '''
    #if contact is None:
        #contact = dbAddContact()

    try:
        password = ldapPassword(password)
        user = models.User(username, password, contact=contact, is_device=is_device, is_superadmin=is_superadmin)
        db.session.add(user)
        db.session.commit()
    except IntegrityError, e:
        raise

    return user

def dbSetUserContact(user, contact):
    user.contact = contact
    db.session.add(user)
    # add user
    if models.UserContact.query.filter_by(user=user, contact=contact).one_or_none() is None:
        db.session.add(models.UserContact(user, contact))
    db.session.commit()
    return contact

def dbGetUser(user):
    if isinstance(user, models.User):
        return user

    if isinstance(user, int):
        return models.User.query.filter_by(id=user).one_or_none()

    if isinstance(user, str) or isinstance(user, unicode):
        return models.User.query.filter_by(username=user).one_or_none()
    return None

def dbGetUserId(user):
    '''
    Get just user ID
    '''
    if isinstance(user, int):
        return user
    elif isinstance(user, models.User):
        return user.id
    elif isinstance(user, str) or isinstance(user, unicode):
        user = models.User.query.filter_by(username=user).one_or_none()
        if user is not None:
            return user.id
    return None


class ApplicationUser(object):
    FIELDS = (
        models.User.id,
        models.User.username,
        models.User.id_contact,
        models.User.is_device,
        models.User.is_superadmin,
        models.ApplicationUser.email,
        models.ApplicationUser.phone,
        models.ApplicationUser.is_staff,
        models.ApplicationUser.is_admin,
    )

    @staticmethod
    def load(obj):
        if obj is not None:
            return ApplicationUser(obj)
        return None

    def __init__(self, obj):
        for key in obj.keys():
            setattr(self, key, getattr(obj, key))

        if self.is_admin:
            self.is_staff = True
        elif self.is_superadmin:
            self.is_staff = True
            self.is_admin = True

def dbGetApplicationUser(id_application, id_user):
    id_user = dbGetUserId(id_user)
    if isinstance(id_application, models.Application):
        id_application = id_application.id

    return ApplicationUser.load(db.session.query(*ApplicationUser.FIELDS).join(
                                                models.ApplicationUser.user
                                            ).filter(
                                                models.ApplicationUser.id_application==id_application,
                                                models.ApplicationUser.id_user==id_user
                                            ).one_or_none())

def dbAddApplicationUser(id_application, id_user, contact=None, email=None, phone=None, is_staff=None, is_admin=None):
    '''
    Add user to application

    if user is already in application, change values if is different
    '''
    if isinstance(id_application, models.Application):
        id_application = id_application.id

    if isinstance(id_user, models.User):
        id_user = id_user.id

    application_user = models.ApplicationUser.query.filter_by(id_application=id_application, id_user=id_user).one_or_none()
    if application_user is None:
        application_user = models.ApplicationUser(
                                                    id_application,
                                                    id_user,
                                                    contact=contact,
                                                    email=email,
                                                    phone=phone,
                                                    is_staff=is_staff not in [False, None],
                                                    is_admin=is_admin not in [False, None]
                                                )
        db.session.add(application_user)
        db.session.commit()

    changed = False
    if email is not None and application_user.email != email:
        changed = True
        application_user.email = email

    if phone is not None and application_user.phone != phone:
        changed = True
        application_user.phone = phone

    if is_staff is not None and application_user.is_staff != is_staff:
        changed = True
        application_user.is_staff = is_staff

    if is_admin is not None and application_user.is_admin != is_admin:
        changed = True
        application_user.is_admin = is_admin

    if changed:
        db.session.add(application_user)

    return application_user

def dbDelApplicationUser(id_application, id_user):
    '''
    Remove user from application
    '''
    models.ApplicationUser.query.filter(id_application=id_application, id_user=id_user).delete(synchronize_session=False)
    models.ApplicationUserContact.query.filter(id_application=id_application, id_user=id_user).delete(synchronize_session=False)
    db.session.commit()

def dbGetApplicationUserList(id_application, device=False):
    '''
    device = True, False, None
    return all active application user
    '''
    if isinstance(id_application, models.Application):
        id_application = Application

    filter_args = [
                    models.ApplicationUser.id_application==id_application,
                    models.ApplicationUser.id_user==models.User.id,
                  ]

    if device is True:
        filter_args.append(models.User.is_device==True)
    elif device is False:
        filter_args.append(models.User.is_device==False)

    return ApplicationUser.load(db.session.query(*ApplicationUser.FIELDS).join(
                                                models.ApplicationUser.user
                                            ).filter(
                                                *filter_args
                                            ).all())
