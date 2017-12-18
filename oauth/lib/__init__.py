# -*- coding: utf-8 -*-
from query import *
from auth import *
from validators import *
from ldap import *
from sms import *

from ares_util.ares import call_ares

def getContactByIC(ic):

    contact = dbGetContactByIC(ic)
    if contact is None:
        ares = call_ares(ic)
        if ares:
            data = {
                        'company': ares['legal']['company_name'],
                        'ic': ares['legal']['company_id'],
                        'dic': ares['legal']['company_vat_id'],
                        'street': ares['address']['street'],
                        'city': ares['address']['city'],
                        'zip': ares['address']['zip_code'],
                        'www': None,
                        'email': None,
                        'first_name': None,
                        'last_name': None,
                    }

            if ares['legal']['legal_form'] == '101':
                try:
                    split = ares['legal']['company_name'].split(' ')
                    data['first_name'] = split[0]
                    data['last_name'] = split[1]
                except Exception, e:
                    pass

            contact = dbAddContact(**data)
    return contact


def getContactByDIC(dic):
    return dbGetContactByDIC(dic)
