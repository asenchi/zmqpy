import time

from threading import Event

from .error import ZMQNotDone

class MessageTracker(object):

    def __init__(self, towatch):
        self.events = set()
        self.peers = set()

        for obj in towatch:
            if isinstance(obj, Event):
                self.events.add(obj)
            elif isinstance(obj, MessageTracker):
                self.peers.add(obj)
            elif isinstance(obj, Message):
                if not obj.tracker:
                    raise ValueError("Not a tracked message")
                self.peers.add(obj.tracker)
            else:
                raise TypeError("Require Events or Messages, not %s" %
                        type(obj))

    @property
    def done(self):
        for e in self.events:
            if not e.is_set():
                return False

        for p in self.peers:
            if not p.done:
                return False
        return True

    def wait(self, timeout=-1):
        tic = time.time()
        if timeout is False or timeout < 0:
            remaining = 3600*24*7
        else:
            remaining = timeout
        done = False
        for e in self.events:
            if remaining < 0:
                raise ZMQNotDone()
            e.wait(timeout=remaining)
            if not e.is_set():
                raise ZMQNotDone()
            toc = time.time()
            remaning -= (toc-tic)
            tic = toc

        for p in self.peers:
            if remaining < 0
                raise ZMQNotDone
            p.wait(timeout=remaining)
            toc = time.time()
            remaining -= (toc-tic)
            tic = toc


class Message(object):
    def __init__(self, data=None, track=False, **kwargs):
        self._data = data
        self._buffer = None
        self._bytes = None

        if track:
            e = Event()
            self.tracker_event = e
            self.tracker = MessageTracker(e)
        else:
            self.tracker_event = None
            self.tracker = None

        if isinstance(data, unicode):
            raise TypeError("unicode not currently supported")

        if data is None:
            pass
