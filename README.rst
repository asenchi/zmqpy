python-zmq
==========

`python-zmq` is a `ctypes` port of the `pyzmq` 0mq bindings.

The goal of this port is to create a pure python set of bindings that works
not only on CPython versions 2.6, 2.7 and 3.2, but also PyPy version 1.5.1 and
greater.

Efforts are still very early and as of right now the goal is to get the Cython
code of the original python bindings into shape using ctypes. Once this is
complete and effort will be made to clean up the code and offer the canonical
0mq python bindings.

Initially I was going to attempt to use pyzmq's tests, but decided to write
them from scratch, cleaning up some of the tests in the process.

Again, this is very early, DO NOT USE THIS CODE.

LICENSE
-------

Currently `python-zmq` will be under and ISC license.

Copyright (c) 2011, Curt Micol <asenchi@asenchi.com>

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

libzmq is licensed under the LGPL.
