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

    def setup_hidden_service(self, tor_process_protocol):
        config      = txtorcon.TorConfig(tor_process_protocol.tor_protocol)
        hs_endpoint = txtorcon.TCPHiddenServiceEndpoint(reactor, config, self.publicPort)
        return hs_endpoint

    def updates(self, prog, tag, summary):
        print "%d%%: %s" % (prog, summary)

    def _parseServer(self, reactor, socksPort=None, controlPort=None, publicPort=None):
        assert publicPort is not None
        assert (socksPort and controlPort) is not None

        self.publicPort    = int(publicPort)

        config             = txtorcon.TorConfig()
        config.socksPort   = int(socksPort)
        config.ControlPort = int(controlPort)

        # optional progress output
        #progress_updates   = self.updates
        progress_updates   = None

        d = txtorcon.launch_tor(config, reactor, progress_updates=progress_updates, timeout=60)
        d.addCallback(self.setup_hidden_service)
        return d

    def parseStreamServer(self, reactor, *args, **kwargs):
        return self._parseServer(reactor, *args, **kwargs)



torHiddenServiceEndpointStringParser = TorHiddenServiceEndpointStringParser()
