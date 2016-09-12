.. image:: https://travis-ci.org/agronholm/ircproto.svg?branch=master
  :target: https://travis-ci.org/agronholm/ircproto
  :alt: Build Status
.. image:: https://coveralls.io/repos/github/agronholm/ircproto/badge.svg?branch=master
  :target: https://coveralls.io/github/agronholm/ircproto?branch=master
  :alt: Code Coverage

The IRC_ (Internet Relay Chat) protocol is the oldest distributed chat protocol still in widespread
use. This library implements both client and server sides of the IRC protocol as a pure
state-machine which only takes in bytes and returns a list of parsed events. This leaves users free
to use any I/O approach they see fit (asyncio_, curio_, Twisted_, etc.).

Sample code is provided for implementing both clients and servers using a variety of I/O
frameworks.

.. _IRC: https://tools.ietf.org/html/rfc2812
.. _asyncio: https://docs.python.org/3/library/asyncio.html
.. _curio: https://github.com/dabeaz/curio
.. _Twisted: https://twistedmatrix.com/

Project links
-------------

* `Documentation <http://ircproto.readthedocs.org/en/latest/>`_
* `Source code <https://github.com/agronholm/ircproto>`_
* `Issue tracker <https://github.com/agronholm/ircproto/issues>`_
