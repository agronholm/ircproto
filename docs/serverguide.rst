Server implementor's guide
==========================

Creating a real-world IRC server using ircproto is somewhat more complicated than writing a client.

As with other sans-io protocols, you feed incoming data to ircproto and it vends events in return.
For a server, all your :class:`~ircproto.connection.IRCServerConnection` instances will need a
shared :class:`~ircproto.states.IRCServerState` instance. This server state will track the states
of connected clients, connected servers and open channels. Feeding incoming data to an IRC
connection on a server will usually generate outgoing data for multiple connections.
The I/O implementation is responsible for keeping a lookup table that allows it to target the
outgoing data to the proper network sockets.

Implementor's responsibilities
------------------------------

The logic in the connection class will handle most complications of the protocol.
That leaves just a handful of things for I/O implementors to keep in mind:

* Reply to every command event coming from connected peers (except ``PONG``).
  Some commands may require multiple replies.
  Refer to :rfc:`2812` regarding which replies are appropriate for each command.
* Regularly send PING messages to clients and drop their connections when they fail to respond in
  time
* Connect/disconnect other servers when an IRC operator requests it
* Disconnect clients when they are killed

Running the examples
--------------------

The ``examples`` directory in the project source tree contains example code for several popular
I/O frameworks to get you started. Just run any of the server scripts and it will start a server
listening on the default IRC port (6667).
