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


import ctypes

# Load libzmq
try:
    C = ctypes.CDLL('libzmq', use_errno=True)
except OSError:
    import ctypes.util
    location = ctypes.util.find_library('libzmq')
    if location:
        C = ctypes.CDLL(location, use_errno=True)
    if C is None:
        raise ImportError("Unable to find a libzmq")


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


### ZMQ Functions

# int zmq_bind(void *socket, const char *endpoint);
C.zmq_bind.restype = c_int
C.zmq_bind.argtypes = [c_void_p, c_char_p]
C.zmq_bind.errcheck = _check_result

# int zmq_close(void *socket);
C.zmq_close.restype = c_int
C.zmq_close.argtypes = [c_void_p]
C.zmq_close.errcheck = _check_result

# int zmq_connect(void *socket, const char *endpoint);
C.zmq_connect.restype = c_int
C.zmq_connect.argtypes = [c_void_p, c_char_p]
C.zmq_connect.errcheck =_check_result

# int zmq_errno(void)
C.zmq_errno.restype = c_int
C.zmq_errno.argtypes = []

# int zmq_getsockopt(void *socket, int option_name,
#                    void *option_value, size_t *option_len);
C.zmq_getsockopt.restype = c_int
C.zmq_getsockopt.argtypes = [c_void_p, c_int, c_void_p, POINTER(c_size_t)]
C.zmq_getsockopt.errcheck = _check_result

# void *zmq_init (int io_threads);
C.zmq_init.restype = c_void_p
C.zmq_init.argtypes = [c_int]
C.zmq_init.errcheck = _check_result

# int zmq_recv(void *socket, zmq_msg_t *msg, int flags);
C.zmq_recv.restype = c_int
C.zmq_recv.argtypes = [c_void_p, POINTER(zmq_msg_t), c_int]

# int zmq_send(void *socket, zmq_msg_t *msg, int flags);
C.zmq_send.restype = c_int
C.zmq_send.argtypes = [c_void_p, POINTER(zmq_msg_t), c_int]

# int zmq_setsockopt(void *socket, int option_name,
#                    const void *option_value, size_t option_len);
C.zmq_setsockopt.restype = c_int
C.zmq_setsockopt.argtypes = [c_void_p, c_int, c_void_p, c_size_t]
C.zmq_setsockopt.errcheck = _check_result

# void *zmq_socket(void *context, int type);
C.zmq_socket.restype = c_void_p
C.zmq_socket.argtypes = [c_void_p, c_int]
C.zmq_socket.errcheck = _check_result

# const char *zmq_strerror(int errnum);
C.zmq_strerror.restype = c_char_p
C.zmq_strerror.argtypes = [c_int]

# int zmq_term (void *context);
C.zmq_term.restype = c_int
C.zmq_term.argtypes = [c_void_p]
C.zmq_term.errcheck = _check_result

# void zmq_version(int *major, int *minor, int *patch);
C.zmq_version.restype = None
C.zmq_version.argtypes = [POINTER(c_int)]*3

major, minor, patch = c_int(), c_int(), c_int()
C.zmq_version(byref(major), byref(minor), byref(patch))

def zmq_version():
    return tuple(pt.value for pt in (major,minor,patch))

ZMQ_VERSION = int("".join([str(v) for v in zmq_version()]))

C.zmq_msg_init.restype=c_int
C.zmq_msg_init.argtypes=[POINTER(zmq_msg_t)]

C.zmq_msg_init_size.restype = c_int
C.zmq_msg_init_size.argtypes = [POINTER(zmq_msg_t), c_size_t]

C.zmq_msg_init_data.restype = c_int
C.zmq_msg_init_data.argtypes = [POINTER(zmq_msg_t), c_void_p, c_size_t, c_void_p, c_void_p]

C.zmq_msg_close.restype = c_int
C.zmq_msg_close.argtypes = [POINTER(zmq_msg_t)]

C.zmq_msg_move.restype = c_int
C.zmq_msg_move.argtypes = [POINTER(zmq_msg_t), POINTER(zmq_msg_t)]

C.zmq_msg_data.restype = c_void_p
C.zmq_msg_data.argtypes = [POINTER(zmq_msg_t)]

C.zmq_msg_copy.restype = c_int
C.zmq_msg_copy.argtypes = [POINTER(zmq_msg_t), POINTER(zmq_msg_t)]

C.zmq_msg_size.restype = c_size_t,
C.zmq_msg_size.argtypes = [POINTER(zmq_msg_t)]
