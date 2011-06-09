
from ctypes import get_errno

from .libzmq import zmq_strerror

__all__ = ['ZMQException', 'ZMQError', 'ZMQNotDone', 'strerror']

class ZMQException(Exception):
    pass

class ZMQError(ZMQException):
    def __init__(self, errno=None):
        if errno is None:
            errno = get_errno()
        self.strerror = zmq_strerror(errno)
        self.errno = errno

    def __str__(self):
        return self.strerror

class ZMQNotDone(ZMQException):
    pass

def strerror(errnum):
    rc = zmq_strerror(errnum)
    if str is bytes:
        return rc
    else:
        return rc.decode()
