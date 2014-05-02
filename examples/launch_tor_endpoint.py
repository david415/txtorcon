#!/usr/bin/env python

##
## Here we set up a Twisted Web server and then launch a slave tor
## with a configured hidden service directed at the Web server we set
## up. This uses serverFromString to translate the "onion" endpoint descriptor
## into a TCPHiddenServiceEndpoint object...
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

def setup_complete(port):
    print "I have set up a hidden service, advertised at:"
    print "http://%s:%d" % (port.onion_uri, port.onion_port)
    print "locally listening on", port.getHost()

def received_endpoint(endpoint):
    print "endpoint %s" % (endpoint,)
    if endpoint is None:
        return
    else:
        endpoint.listen(site).addCallback(setup_complete).addErrback(setup_failed)



# set a couple options to avoid conflict with the defaults if a Tor is
# already running
hs_endpoint_deferred = serverFromString(reactor, "onion:socksPort=0:controlPort=9089:publicPort=80")
hs_endpoint_deferred.addCallback(received_endpoint)
hs_endpoint_deferred.addErrback(setup_failed)

reactor.run()
