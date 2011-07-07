from ctypes import get_errno

from zmqpy import libzmq

class ZMQException(Exception):
    pass

class ZMQError(ZMQException):
    def __init__(self, errno=None):
        if errno is None:
            errno = get_errno()
        self.strerror = libzmq.C.zmq_strerror(errno)
        self.errno = errno

    def __str__(self):
        return self.strerror

class ZMQNotDone(ZMQException):
    pass

def strerror(errnum):
    rc = libzmq.C.zmq_strerror(errnum)
    if str is bytes:
        return rc
    else:
        return rc.decode()
