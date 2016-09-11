from argparse import ArgumentParser

import curio

from ircproto.connection import IRCClientConnection
from ircproto.constants import RPL_MYINFO
from ircproto.events import Reply, Error, Join


async def send_message_to_channel(host, port, nickname, channel, message):
    async def send_outgoing_data():
        # This is more complicated than it should because we want to print all outgoing data here.
        # Normally, await sock.sendall(conn.data_to_send()) would suffice.
        output = conn.data_to_send()
        if output:
            print('>>> ' + output.decode('utf-8').replace('\r\n', '\r\n>>> ').rstrip('> \r\n'))
            await sock.sendall(output)

    sock = await curio.open_connection(host, port)
    async with sock:
        conn = IRCClientConnection()
        conn.send_command('NICK', nickname)
        conn.send_command('USER', 'ircproto', '0', 'ircproto example client')
        await send_outgoing_data()
        while True:
            data = await sock.recv(10000)
            for event in conn.feed_data(data):
                print('<<< ' + event.encode().rstrip())
                if isinstance(event, Reply):
                    if event.is_error:
                        return
                    elif event.code == RPL_MYINFO:
                        conn.send_command('JOIN', channel)
                elif isinstance(event, Join):
                    conn.send_command('PRIVMSG', channel, message)
                    conn.send_command('QUIT')
                    await send_outgoing_data()
                    return
                elif isinstance(event, Error):
                    return

            await send_outgoing_data()


parser = ArgumentParser(description='A sample IRC client')
parser.add_argument('host', help='address of irc server (foo.bar.baz or foo.bar.baz:port)')
parser.add_argument('nickname', help='nickname to register as')
parser.add_argument('channel', help='channel to join once registered')
parser.add_argument('message', help='message to send once joined')
args = parser.parse_args()
host, _, port = args.host.partition(':')

curio.run(send_message_to_channel(host, int(port or 6667), args.nickname, args.channel,
                                  args.message))
