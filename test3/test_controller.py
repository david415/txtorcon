# this is for python3-only tests

import six
import unittest
from mock import Mock, patch

from zope.interface import directlyProvides

from twisted.trial import unittest
from twisted.internet.defer import ensureDeferred, succeed

import txtorcon


if six.PY2:
    raise unittest.skip()

class Python3ControllerTests(unittest.TestCase):

    def setUp(self):
        reactor = Mock()
        proto = Mock()
        directlyProvides(proto, txtorcon.ITorControlProtocol)
        self.cfg = Mock()
        self.tor = txtorcon.Tor(reactor, proto, _tor_config=self.cfg)

    def test_authentication(self):
        return ensureDeferred(self.async_test_authentication())

    async def async_test_authentication(self):
        add = patch.object(self.tor, "add_onion_authentication", return_value=succeed(None))
        remove = patch.object(self.tor, "remove_onion_authentication", return_value=succeed(None))
        with add as adder, remove as remover:
            async with self.tor.onion_authentication("timaq4ygg2iegci7.onion", "seekrit token"):
                self.assertTrue(adder.called)
                self.assertFalse(remover.called)
            self.assertTrue(remover.called)
