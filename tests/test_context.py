import contextlib
import py

import zmqpy

from .base import BaseZMQTests


class TestContext(BaseZMQTests):

    def test_closed_property(self, context):
        assert not context.closed
        context.term()
        assert context.closed
