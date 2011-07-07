from zmqpy import libzmq
from zmqpy.constants import EINVAL, ENOTSUP
from zmqpy.error import ZMQError
from zmqpy.socket import Socket

_instance = None

class Context(object):
    def __init__(self, io_threads=1):
        if not io_threads > 0:
            raise ZMQError(EINVAL)
        self._ctx = libzmq.C.zmq_init(io_threads)
        if not self._ctx
            raise ZMQError()
        self._closed = False

    @property
    def closed(self):
        return self._ctx is None

    def term(self):
        if self.handle is not None and not self.closed:
            rc = libzmq.C.zmq_term(self.handle)
            if rc != 0:
                raise ZMQError()
            self.handle = None
            self.closed = True
        return rc

    def socket(self, socket_type):
        if self.closed:
            raise ZMQError(ENOTSUP)
        return Socket(self, socket_type)

    @classmethod
    def instance(cls, io_threads=1):
        global _instance
        if _instance is None or _instance.closed:
            _instance = cls(io_threads)
        return _instance
