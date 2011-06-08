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


from ctypes import *

# Load libzmq
try:
    libzmq = CDLL('libzmq', use_errno=True)
except:
    import ctypes.util
    location = ctypes.util.find_library('libzmq')
    if location:
        libzmq = CDLL(location, use_errno=True)

# Constants
ZMQ_HAUSNUMERO = 156384712
ZMQ_ENOTSUP = (ZMQ_HAUSNUMERO + 1)
ZMQ_EPROTONOSUPPORT = (ZMQ_HAUSNUMERO + 2)
ZMQ_ENOBUFS = (ZMQ_HAUSNUMERO + 3)
ZMQ_ENETDOWN = (ZMQ_HAUSNUMERO + 4)
ZMQ_EADDRINUSE = (ZMQ_HAUSNUMERO + 5)
ZMQ_EADDRNOTAVAIL = (ZMQ_HAUSNUMERO + 6)
ZMQ_ECONNREFUSED = (ZMQ_HAUSNUMERO + 7)
ZMQ_EINPROGRESS = (ZMQ_HAUSNUMERO + 8)
ZMQ_ENOTSOCK = (ZMQ_HAUSNUMERO + 9)

# Native 0MQ error codes
ZMQ_EFSM = (ZMQ_HAUSNUMERO + 51)
ZMQ_ENOCOMPATPROTO = (ZMQ_HAUSNUMERO + 52)
ZMQ_ETERM = (ZMQ_HAUSNUMERO + 53)
ZMQ_EMTHREAD = (ZMQ_HAUSNUMERO + 54)
ZMQ_MAX_VSM_SIZE = 30

# Message types
ZMQ_DELIMITER = 31
ZMQ_VSM = 32

ZMQ_MSG_MORE = 1
ZMQ_MSG_SHARED = 128
ZMQ_MSG_MASK = 129 # Merges all the flags

# Socket types.                                                             */ 
ZMQ_PAIR = 0
ZMQ_PUB = 1
ZMQ_SUB = 2
ZMQ_REQ = 3
ZMQ_REP = 4
ZMQ_DEALER = 5
ZMQ_ROUTER = 6
ZMQ_PULL = 7
ZMQ_PUSH = 8
ZMQ_XPUB = 9
ZMQ_XSUB = 10

# TODO Support versions here
ZMQ_XREQ = ZMQ_DEALER        # Old alias, remove in 3.x
ZMQ_XREP = ZMQ_ROUTER        # Old alias, remove in 3.x
ZMQ_UPSTREAM = ZMQ_PULL      # Old alias, remove in 3.x
ZMQ_DOWNSTREAM = ZMQ_PUSH    # Old alias, remove in 3.x

# Socket options
ZMQ_HWM = 1
ZMQ_SWAP = 3
ZMQ_AFFINITY = 4
ZMQ_IDENTITY = 5
ZMQ_SUBSCRIBE = 6
ZMQ_UNSUBSCRIBE = 7
ZMQ_RATE = 8
ZMQ_RECOVERY_IVL = 9
ZMQ_MCAST_LOOP = 10
ZMQ_SNDBUF = 11
ZMQ_RCVBUF = 12
ZMQ_RCVMORE = 13
ZMQ_FD = 14
ZMQ_EVENTS = 15
ZMQ_TYPE = 16
ZMQ_LINGER = 17
ZMQ_RECONNECT_IVL = 18
ZMQ_BACKLOG = 19
ZMQ_RECOVERY_IVL_MSEC = 20   # opt. recovery time, reconcile in 3.x
ZMQ_RECONNECT_IVL_MAX = 21
ZMQ_MAXMSGSIZE = 22
ZMQ_SNDHWM = 23
ZMQ_RCVHWM = 24

# Send/recv options
ZMQ_NOBLOCK = 1
ZMQ_DONTWAIT = 1
ZMQ_SNDMORE = 2

ZMQ_POLLIN = 1
ZMQ_POLLOUT = 2
ZMQ_POLLERR = 4

# Devices
ZMQ_STREAMER = 1
ZMQ_FORWARDER = 2
ZMQ_QUEUE = 3

# Helpers
def _zmq_func(shlib, func, **kwargs):
    fn = getattr(shlib, func)
    fn.restype = kwargs.pop('restype', None)
    fn.argtypes = kwargs.pop('argtypes', None)
    if fn.errcheck is not None:
        fn.errcheck = kwargs.pop('errcheck', None)
    return fn

def _check_result(rc, func, args):
    if rc is None:
        raise ZMQError(get_errno())
    if rc != 0:
        raise ZMQError(get_errno())
    return rc


class zmq_msg_t(Structure):
    _fields_ = [
            ('content', c_void_p),
            ('flags', c_ubyte),
            ('vsm_size', c_ubyte),
            ('vsm_data', c_ubyte*ZMQ_MAX_VSM_SIZE)
            ]

# ZMQ Functions
# int zmq_bind(void *socket, const char *endpoint);
zmq_bind = _zmq_func(libzmq, 'zmq_bind',
                     restype=c_int,
                     argtypes=[c_void_p, c_char_p],
                     errcheck=_check_result)

# int zmq_close(void *socket);
zmq_close = _zmq_func(libzmq, 'zmq_close',
                      restype=c_int,
                      argtypes=[c_void_p],
                      errcheck=_check_result)

# int zmq_connect(void *socket, const char *endpoint);
zmq_connect = _zmq_func(libzmq, 'zmq_connect',
                        restype=c_int,
                        argtypes=[c_void_p, c_char_p],
                        errcheck=_check_result)

# int zmq_errno(void)
zmq_errno = _zmq_func(libzmq, 'zmq_errno',
                      restype=c_int,
                      argtypes=[])

# int zmq_getsockopt(void *socket, int option_name,
#                    void *option_value, size_t *option_len);
zmq_getsockopt = _zmq_func(libzmq, 'zmq_getsockopt',
                           restype=c_int,
                           argtypes=[c_void_p, c_int,
                                     c_void_p, POINTER(c_size_t)],
                           errcheck=_check_result)

# void *zmq_init (int io_threads);
zmq_init = _zmq_func(libzmq, 'zmq_init',
                     restype=c_void_p,
                     argtypes=[c_int],
                     errcheck=_check_result)

# int zmq_recv(void *socket, zmq_msg_t *msg, int flags);
zmq_recv = _zmq_func(libzmq, 'zmq_recv',
                     restypes=c_int,
                     argtypes=[c_void_p, POINTER(zmq_msg_t), c_int])

# int zmq_send(void *socket, zmq_msg_t *msg, int flags);
zmq_send = _zmq_func(libzmq, 'zmq_send',
                     restypes=c_int,
                     argtypes=[c_void_p, POINTER(zmq_msg_t), c_int])

# int zmq_setsockopt(void *socket, int option_name,
#                    const void *option_value, size_t option_len);
zmq_setsockopt = _zmq_func(libzmq, 'zmq_setsockopt',
                           restype=c_int,
                           argtypes=[c_void_p, c_int, c_void_p, c_size_t],
                           errcheck=_check_result)

# void *zmq_socket(void *context, int type);
zmq_socket = _zmq_func(libzmq, 'zmq_socket',
                       restype=c_void_p,
                       argtypes=[c_void_p, c_int],
                       errcheck=_check_result)

# const char *zmq_strerror(int errnum);
zmq_strerror = _zmq_func(libzmq, 'zmq_errno',
                         restype=c_char_p,
                         argtypes=[c_int])

# int zmq_term (void *context);
zmq_term = _zmq_func(libzmq, 'zmq_term',
                     restype=c_int,
                     argtypes=[c_void_p],
                     errcheck=_check_result)

# void zmq_version(int *major, int *minor, int *patch);
__zmq_version = _zmq_func(libzmq, 'zmq_version',
                          restype=None,
                          argtypes=[POINTER(c_int)]*3)

major, minor, patch = c_int(), c_int(), c_int()
__zmq_version(byref(major), byref(minor), byref(patch))

def zmq_version():
    return tuple(pt.value for pt in (major,minor,patch))

ZMQ_VERSION = int("".join([str(v) for v in zmq_version()]))

zmq_msg_init = _zmq_func(libzmq, 'zmq_msg_init',
                         restype=c_int,
                         argtypes=[POINTER(zmq_msg_t)])

zmq_msg_init_size = _zmq_func(libzmq, 'zmq_msg_init_size',
                         restype=c_int,
                         argtypes=[POINTER(zmq_msg_t), c_size_t])

zmq_msg_init_data = _zmq_func(libzmq, 'zmq_msg_init_data',
                         restype=c_int,
                         argtypes=[POINTER(zmq_msg_t), c_void_p, c_size_t,
                                   c_void_p, c_void_p])

zmq_msg_close = _zmq_func(libzmq, 'zmq_msg_close',
                          restype=c_int,
                          argtypes=[POINTER(zmq_msg_t)])

zmq_msg_move = _zmq_func(libzmq, 'zmq_msg_move',
                         restypes=c_int,
                         argtypes = [POINTER(zmq_msg_t), POINTER(zmq_msg_t)])

zmq_msg_data = _zmq_func(libzmq, 'zmq_msg_data',
                         estype=c_void_p,
                         argtypes = [POINTER(zmq_msg_t)])

zmq_msg_copy = _zmq_func(libzmq, 'zmq_msg_copy',
                         restype=c_int,
                         argtypes = [POINTER(zmq_msg_t), POINTER(zmq_msg_t)])

zmq_msg_size = _zmq_func(libzmq, 'zmq_msg_size',
                         restype = c_size_t,
                         argtypes = [POINTER(zmq_msg_t)])
