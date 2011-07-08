import contextlib
import py

import zmqpy

from .base import BaseZMQTests


class TestContext(BaseZMQTests):

    def test_object_deletion(self, context):
        assert not context.closed
        try:
            del context
        except NameError:
            pass

    def test_closed_property(self, context):
        assert not context.closed
        context.term()
        assert context.closed

    def test_init_failure(self):
        with py.test.raises(zmqpy.ZMQError):
            ctx = zmqpy.Context(0)

    def test_global_context(self, context):
        c1 = context.instance()
        c2 = zmqpy.Context.instance(2)
        assert c1 == c2
        c2.term()
        c3 = zmqpy.Context.instance()
        c4 = zmqpy.Context.instance()
        assert c3 != c2
        assert c3 == c4

    def test_socket_close(self, context):
        py.test.skip("Not yet implemented")

    def test_mass_socket_creation(self, context):
        py.test.skip("Not yet implemented")

    def test_termination(self, context):
        py.test.skip("Not yet implemented")
