import pytest


def test_core():
    try:
        import zmq
    except ImportError:
        assert(0)

def test_ctypes():
    try:
        from zmq import libzmq
    except ImportError:
        assert(0)

def test_constants():
    try:
        from zmq import constants
    except ImportError:
        assert(0)

def test_context():
    try:
        from zmq import context
    except ImportError:
        assert(0)

def test_device():
    try:
        from zmq import device
    except ImportError:
        assert(0)

def test_error():
    try:
        from zmq import error
    except ImportError:
        assert(0)

def test_message():
    pytest.skip("Not implemented")
    try:
        from zmq import message
    except ImportError:
        assert(0)

def test_socket():
    try:
        from zmq import socket
    except ImportError:
        assert(0)
