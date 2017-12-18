# -*- coding: utf-8 -*-

from flask.ext.spyne import Spyne
from spyne.protocol.soap import Soap11
from spyne.model.primitive import Unicode, Integer
from spyne.model.complex import Iterable
from oauth import app
from oauth import lib

soap = Spyne(app)

class TestService(soap.Service):
    __service_url_path__ = '/soap/'
    __in_protocol__ = Soap11(validator='lxml')
    __out_protocol__ = Soap11()

    @soap.srpc(Unicode, Integer, _returns=Iterable(Unicode))
    def echo(str, cnt):
        for i in range(cnt):
            yield str
