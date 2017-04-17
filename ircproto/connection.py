from __future__ import unicode_literals

import codecs

from ircproto.events import decode_event, commands, Reply, Ping
from ircproto.exceptions import ProtocolError
from ircproto.replies import reply_templates


class BaseIRCConnection(object):
    """Base class for IRC connection state machines."""

    __slots__ = ('output_codec', 'input_codec', 'fallback_codec', '_input_buffer',
                 '_output_buffer', '_closed')

    sender = None  # type: str

    def __init__(self, output_encoding='utf-8', input_encoding='utf-8',
                 fallback_encoding='iso-8859-1'):
        self.output_codec = output_encoding
        self.input_codec = input_encoding
        self.fallback_codec = fallback_encoding
        self._input_buffer = bytearray()
        self._output_buffer = bytearray()
        self._closed = False

    def feed_data(self, data):
        """
        Feed data to the internal buffer of the connection.

        If there is enough data to generate one or more events, they will be added to the list
        returned from this call.

        Sometimes this call generates outgoing data so it is important to call
        :meth:`.data_to_send` afterwards and write those bytes to the output.

        :param bytes data: incoming data
        :raise ircproto.ProtocolError: if the protocol is violated
        :return: the list of generated events
        :rtype: list

        """
        self._input_buffer.extend(data)
        events = []
        while True:
            event = decode_event(self._input_buffer, self.input_codec, self.fallback_codec)
            if event is None:
                return events
            else:
                self.handle_event(event)
                events.append(event)

    def data_to_send(self):
        """
        Return any data that is due to be sent to the other end.

        :rtype: bytes

        """
        data = bytes(self._output_buffer)
        del self._output_buffer[:]
        return data

    def handle_event(self, event):
        # Automatically respond to pings
        if isinstance(event, Ping):
            self.send_command('PONG', event.server1, event.server2)

    def send_command(self, command, *params):
        """
        Send a command to the peer.

        This method looks up the appropriate command event class and instantiates it using
        ``params``. Then the event is encoded and added to the output buffer.

        :param str command: name of the command (``NICK``, ``PRIVMSG`` etc.)
        :param str params: arguments for the constructor of the command class

        """
        if isinstance(command, bytes):
            command = command.decode('ascii')

        try:
            command_cls = commands[command]
        except KeyError:
            raise ProtocolError('no such command: %s' % command)

        event = command_cls(None, *params)
        self._send_event(event)

    def _send_event(self, event):
        """
        Send an event to the peer.

        :param ircproto.events.Event event: the event to send

        """
        if self._closed:
            raise ProtocolError('the connection has been closed')

        encoded_event = event.encode()
        self._output_buffer.extend(codecs.encode(encoded_event, encoding=self.output_codec))


class IRCClientConnection(BaseIRCConnection):
    """An IRC client's connection to a server."""

    __slots__ = ('nickname', 'realname')

    def __init__(self):
        super(IRCClientConnection, self).__init__()
        self.nickname = self.realname = None


class IRCServerConnection(BaseIRCConnection):
    """A server side connection to either an IRC client or another IRC server."""

    __slots__ = ('host', '_server_state')

    def __init__(self, host, server_state):
        super(IRCServerConnection, self).__init__()
        self.host = host
        self._server_state = server_state

    def send_reply(self, code, **templatevars):
        """
        Send a reply for a command.

        This method creates a :class:`~ircproto.events.Reply`, encodes it and adds the result to
        the ouput buffer.

        :param int code: reply code
        :param templatevars: variables required for the reply message template

        """
        # Format the reply message
        message = reply_templates[code].format(**templatevars)
        event = Reply(self.sender, code, message)
        self._send_event(event)

    @property
    def sender(self):
        return self._server_state.host
