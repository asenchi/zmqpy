VERSION = (0, 1, 0, "a", 1) # following PEP 386
DEV_N = 0

def get_version():
    version = "%s.%s" % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = "%s.%s" % (version, VERSION[2])
    if VERSION[3] != "f":
        version = "%s%s%s" % (version, VERSION[3], VERSION[4])
        if DEV_N:
            version = "%s.dev%s" % (version, DEV_N)
    return version

__version__ = get_version()

from zmq.libzmq import *

from zmq.constants import *
from zmq.context import *
from zmq.socket import *
