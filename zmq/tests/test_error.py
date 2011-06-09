import pytest

from zmq import ZMQError, strerror

def test_strerror():
    pytest.skip("Not implemented")
    e = strerror(5)
    assert isinstance(e, str)

def test_zmqerror():
    pytest.skip("Not implemented")
    e = ZMQError(5)
    assert e.errno == 5
