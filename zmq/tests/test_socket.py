import pytest
import unittest

import zmq

class TestSocket(unittest.TestCase):

    def setup_class(self):
        self.ctx = zmq.Context()
        self.pub_socket = self.ctx.socket(zmq.PUB)
        self.sub_socket = self.ctx.socket(zmq.SUB)

    def test_create(self):
        assert isinstance(self.pub_socket, zmq.Socket)

    def test_bind(self):
        pytest.skip("Not implemented")

    def test_connect(self):
        pytest.skip("Not implemented")

    def test_close(self):
        ctx = zmq.Context()
        s = ctx.socket(zmq.PUB)
        s.close()
        assert s.closed

    def test_non_support_address(self):
        pytest.skip("Not implemented")

    def test_sockopts_unicode(self):
        pytest.skip("Not implemented")

    def test_sockopts_int32(self):
        pytest.skip("Not implemented")

    def test_sockopts_int64(self):
        pytest.skip("Not implemented")

    def test_send_unicode(self):
        pytest.skip("Not implemented")

    def test_message_tracker(self):
        pytest.skip("Not implemented")
