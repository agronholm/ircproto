from __future__ import print_function, unicode_literals

from argparse import ArgumentParser

from ircproto.connection import IRCClientConnection
from ircproto.constants import RPL_MYINFO
from ircproto.events import Reply, Error, Join

try:
    from asyncio import get_event_loop, Protocol
except ImportError:
    from trollius import get_event_loop, Protocol


class MessageSendProtocol(Protocol):
    def __init__(self, nickname, channel, message):
        self.nickname = nickname
        self.channel = channel
        self.message = message
        self.conn = IRCClientConnection()
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        self.conn.send_command('NICK', self.nickname)
        self.conn.send_command('USER', 'ircproto', '0', 'ircproto example client')
        self.send_outgoing_data()

    def connection_lost(self, exc):
        get_event_loop().stop()

    def data_received(self, data):
        close_connection = False
        for event in self.conn.feed_data(data):
            print('<<< ' + event.encode().rstrip())
            if isinstance(event, Reply):
                if event.is_error:
                    self.transport.abort()
                    return
                elif event.code == RPL_MYINFO:
                    self.conn.send_command('JOIN', self.channel)
            elif isinstance(event, Join):
                self.conn.send_command('PRIVMSG', self.channel, self.message)
                self.conn.send_command('QUIT')
                close_connection = True
            elif isinstance(event, Error):
                self.transport.abort()
                return

        self.send_outgoing_data()
        if close_connection:
            self.transport.close()

    def send_outgoing_data(self):
        # This is more complicated than it should because we want to print all outgoing data here.
        # Normally, self.transport.write(self.conn.data_to_send()) would suffice.
        output = self.conn.data_to_send()
        if output:
            print('>>> ' + output.decode('utf-8').replace('\r\n', '\r\n>>> ').rstrip('> \r\n'))
            self.transport.write(output)

parser = ArgumentParser(description='A sample IRC client')
parser.add_argument('host', help='address of irc server (foo.bar.baz or foo.bar.baz:port)')
parser.add_argument('nickname', help='nickname to register as')
parser.add_argument('channel', help='channel to join once registered')
parser.add_argument('message', help='message to send once joined')
args = parser.parse_args()
host, _, port = args.host.partition(':')

loop = get_event_loop()
protocol = MessageSendProtocol(args.nickname, args.channel, args.message)
loop.run_until_complete(loop.create_connection(lambda: protocol, host, int(port or 6667)))
loop.run_forever()
