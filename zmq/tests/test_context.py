import sys
import pytest

import zmq

class TestContext:

    def test_initialize(self):
        self.c1 = zmq.Context()
        assert isinstance(self.c1, zmq.Context)
        del self.c1
        self.c2 = zmq.Context()
        assert isinstance(self.c2, zmq.Context)
        del self.c2

    def test_term(self):
        self.context = zmq.Context()
        self.context.term()
        assert self.context.closed

    def test_instance(self):
        c1 = zmq.Context.instance()
        c2 = zmq.Context.instance(io_threads=2)
        assert c1 == c2
        c2.term()
        c3 = zmq.Context.instance()
        c4 = zmq.Context.instance()
        assert c2.closed
        assert c3 != c2
        assert c3 == c4

    def test_failure(self):
        pytest.skip("Not Implemented")

    def test_context_socket(self):
        pytest.skip("Not Implemented")
