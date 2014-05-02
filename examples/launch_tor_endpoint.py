#!/usr/bin/env python

##
## Here we set up a Twisted Web server and then launch a slave tor
## with a configured hidden service directed at the Web server we set
## up. This uses TCPHiddenServiceEndpoint, which gives you slightly
## less control over how things are set up, but may be easier. See
## also the :ref:`launch_tor.py` example.
##


from twisted.internet import reactor
from twisted.web import server, resource
from twisted.internet.endpoints import serverFromString

import txtorcon


class Simple(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        return "<html>Hello, world! I'm a hidden service!</html>"

site = server.Site(Simple())

def setup_failed(arg):
    print "SETUP FAILED", arg
    reactor.stop()


def setup_complete(port):
    print "I have set up a hidden service, advertised at:"
    print "http://%s:%d" % (port.onion_uri, port.onion_port)
    print "locally listening on", port.getHost()

def received_endpoint(endpoint):
    print "endpoint %s" % (endpoint,)
    endpoint.listen(site).addCallback(setup_complete).addErrback(setup_failed)

# set a couple options to avoid conflict with the defaults if a Tor is
# already running

hs_endpoint_deferred = serverFromString(reactor, "onion:socksPort=0:controlPort=9089:publicPort=80")

print "hs_endpoint_deferred %s" % (hs_endpoint_deferred,)

hs_endpoint_deferred.addCallback(received_endpoint)


reactor.run()
