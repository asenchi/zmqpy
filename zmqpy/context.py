from zmqpy import libzmq
from zmqpy.constants import EINVAL, ENOTSUP
from zmqpy.errors import ZMQError
from zmqpy.socket import Socket


_instance = None

class Context(object):
    def __init__(self, io_threads=1):
        if not io_threads > 0:
            raise ZMQError(EINVAL)
        self._ctx = libzmq.C.zmq_init(io_threads)

    def __del__(self):
        if not self.closed:
            self.term()

    @property
    def closed(self):
        return self._ctx is None

    def term(self):
        if not self.closed:
            rc = libzmq.C.zmq_term(self._ctx)
            if rc != 0:
                raise ZMQError()
            self._ctx = None
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
