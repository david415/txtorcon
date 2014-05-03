#!/usr/bin/env python

from zope.interface import implementer
from twisted.plugin import IPlugin
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
from twisted.internet.interfaces import IStreamServerEndpointStringParser
from twisted.internet.endpoints import serverFromString
from twisted.internet.endpoints import TCP4ServerEndpoint

import txtorcon


@implementer(IPlugin, IStreamServerEndpointStringParser)
class TorHiddenServiceEndpointStringParser(object):
    prefix = "onion"

    def _parseServer(self, reactor, socksPort=None, controlPort=None, publicPort=None, dataDir=None):

        assert publicPort is not None

        hs_endpoint = txtorcon.TCPHiddenServiceEndpoint(reactor, public_port=publicPort, data_dir=dataDir, socks_port=socksPort, control_port=controlPort)
        return hs_endpoint

    def parseStreamServer(self, reactor, *args, **kwargs):
        return self._parseServer(reactor, *args, **kwargs)



torHiddenServiceEndpointStringParser = TorHiddenServiceEndpointStringParser()
