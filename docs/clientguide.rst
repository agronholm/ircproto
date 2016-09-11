Client implementor's guide
==========================

Creating a real-world IRC client using ircproto is quite straightforward.
As with other sans-io protocols, you feed incoming data to ircproto and it vends events in return.
To invoke actions on the connection, call
:meth:`~ircproto.connection.IRCClientConnection.send_command` with the appropriate arguments for
each command. The server's replies will then be available as :class:`~ircproto.events.Reply`
events.

To get pending outgoing data, use the :meth:`~ircproto.IRCClientConnection.data_to_send` method.
For a reference on the available commands and their arguments, see :rfc:`2812`.

Implementing DCC protocols
--------------------------

TODO

Running the examples
--------------------

The ``examples`` directory in the project source tree contains example code for several popular
I/O frameworks to get you started. Just run any of the client scripts and it will connect to the
specified server, join the specified channel, send a message there and then disconnect.
