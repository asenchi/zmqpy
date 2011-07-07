# Copyright (c) 2011, Curt Micol <asenchi@asenchi.com>
# 
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
# 
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


# TODO THIS NEEDS A LOT OF WORK AND SHOULD NOT BE CONSIDERED WORKING

from ctypes import c_int32, c_int64, c_size_t, sizeof, byref

import libzmq

from .constants import ENOTSUP, EINVAL
from .errors import ZMQError

__all__ = ['Socket']

# TODO
def _recv_message(handle, flags=0, track=False):
    msg = Message(track=track)
    rc = zmq_recvmsg(handle, byref(msg.zmq_msg), flags)
    if rc < 0:
        raise ZMQError()
    return msg

def _recv_copy(handle, flags=0):
    # TODO implement
    pass

class Socket(object):

    def __init__(self, context, socket_type):
        self.context = context
        self.socket_type = socket_type
        self.handle = libzmq.C.zmq_socket(context.handle, socket_type)
        if self.handle is None:
            raise ZMQError()
        self.closed = False

    def close(self):
        """Destroy a 0mq socket object."""
        if self.handle is not None and not self.closed:
            rc = libzmq.C.zmq_close(self.handle)
            if rc != 0:
                raise ZMQError()
            self.handle = None
            self.closed = True
        return rc

    def _verify_open(self):
        if self.closed:
            raise ZMQError(ENOTSUP)

    def bind(self, addr):
        if isinstance(addr, unicode):
            addr = addr.encode('utf-8')
        if not isinstance(addr, bytes):
            raise TypeError('expected str, got: %r' % addr)
        rc = libzmq.C.zmq_bind(self.handle, addr)
        if rc != 0:
            raise ZMQError()

    def connect(self, addr):
        if isinstance(addr, unicode):
            addr = addr.encode('utf-8')
        if not isinstance(addr, bytes):
            raise TypeError('expected str, got: %r' % addr)
        rc = libzmq.C.zmq_connect(self.handle, addr)
        if rc != 0:
            raise ZMQError()

    def rcvmore(self):
        more = self.getsockopt(RCVMORE)
        return bool(more)

    def setsockopt(self, option, value, **kwargs):
        self._verify_open()

        # TODO Need to implement unicode here. The way it works in pyzmq is odd
        # to me, so I need to dig into it.
        encoding = getattr(kwargs, 'encoding', None)
        if encoding:
            raise TypeError('unicode not currently supported.')

        if option in sockopts_bytes:
            if not isinstance(value, bytes):
                raise TypeError('expected str, got: %r' % value)
            rc = libzmq.C.zmq_setsockopt(self.handle, option, byref(value),
                    c_size_t(sizeof(value)))
        elif option in sockopts_int64:
            if not isinstance(value, int):
                raise TypeError('expected str, got: %r' % value)
            value_int64 = c_int64(value)
            rc = libzmq.C.zmq_setsockopt(self.handle, option, byref(value_int64),
                    c_size_t(sizeof(value)))
        elif option in sockopts_int32:
            if not isinstance(value, int):
                raise TypeError('expected str, got: %r' % value)
            rc = libzmq.C.zmq_setsockopt(self.handle, option, byref(value),
                    c_size_t(sizeof(value)))
        else:
            raise ZMQError()

        if rc != 0:
            raise ZMQError()

    def getsockopt(self, option):
        self._verify_open()

        if option in sockopts_bytes:
            if not vlen:
                vlen = c_size_t(sizeof(value))
            rc = libzmq.C.zmq_getsockopt(self.handle, option, byref(value), byref(vlen))
        elif option in sockopts_int64:
            value = c_int64(value)
            if not vlen:
                vlen = c_size_t(sizeof(value))
            rc = libzmq.C.zmq_getsockopt(self.handle, option, byref(value), byref(vlen))
        elif option in sockopts_int32:
            value = c_int32(value)
            if not vlen:
                vlen = c_size_t(sizeof(value))
            rc = libzmq.C.zmq_getsockopt(self.handle, option, byref(value), byref(vlen))
        else:
            raise ZMQError(EINVAL)

        if rc != 0:
            raise ZMQError()

    def send(self, data, flags=0, copy=True, track=False):
        self._verify_open()

        if isinstance(data, unicode):
            raise TypeError("unicode not currently supported")

        if copy:
            if isinstance(data, Message):
                data = data.buffer
            return _send_copy(self.handle, data, flags)
        else:
            if isinstance(data, Message):
                if track and not data.tracker:
                    raise ValueError('message not tracked')
                msg = data
            else:
                msg = Message(data, track=track)
            return _send_message(self.handle, msg, flags)

    def recv(self, flags=0, copy=True, track=False):
        self._verify_open()

        if copy:
            return _recv_copy(self.handle, flags)
        else:
            return _recv_message(self.handle, flags, track)

    def send_multipart(self, msg_parts, flags=0, copy=True, track=False):
        for msg in msg_parts[:-1]:
            self.send(msg, SNDMORE|flags, copy=copy, track=track)
        return self.send(msg_parts[-1], flags, copy=copy, track=track)

    def recv_multipart(self, flags=0, copy=True, track=False):
        parts = []
        while True:
            part = self.recv(flags, copy=copy, track=track)
            parts.append(part)
            if self.rcvmore():
                continue
            else:
                break
        return parts

# TODO Implement helper methods: json, tnetstrings, pyobj, etc
