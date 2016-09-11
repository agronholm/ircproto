from ircproto.constants import *
from ircproto.utils import match_hostmask


class IRCChannel(object):
    """
    Represents the state of an IRC channel.

    :ivar str name: name of the channel
    :ivar str topic: current topic
    :ivar str key: current channel key
    :ivar int limit: current channel limit (maximum number of users)
    :ivar list users: list of client connections who are currently on this channel
    :ivar list bans: list of hostmasks (matching clients are prohibited from joining)
    :ivar list invites: list of nicknames who are invited to join the channel
    """

    __slots__ = ('name', 'modes', 'topic', 'key', 'limit', 'users', 'bans', 'invites')

    def __init__(self, name, modes):
        self.name = name
        self.modes = modes
        self.topic = self.key = self.limit = None
        self.bans = []
        self.invites = []
        self.users = []


class IRCServer(object):
    """
    Represents the state of an IRC server.

    :ivar str host: host name of the server
    :ivar dict clients: list of all client connections
    :ivar dict channels: dictionary of channel names to :class:`.IRCChannel` instances
    :ivar dict nicknames: dictionary of nicknames to client connections
    """

    __slots__ = ('host', 'default_channel_modes', 'clients', 'servers', 'channels', 'nicknames')

    def __init__(self, host, default_channel_modes='nt'):
        self.host = host
        self.default_channel_modes = default_channel_modes
        self.clients = []
        self.servers = []
        self.channels = {}
        self.nicknames = {}

    def add_client_connection(self, connection):
        self.clients[connection.nickname] = connection

    def add_server_connection(self, connection):
        self.servers[connection.host] = connection

    def handle_join(self, connection, event):
        channel_name = event.channel
        channel = self.channels.get(channel_name)
        if not channel:
            channel = self.channels[channel_name] = IRCChannel(channel_name,
                                                               self.default_channel_modes)
        else:
            if channel.limit and len(channel.users) >= channel.limit:
                connection.process_reply(ERR_CHANNELISFULL, channel=channel_name)
                return
            elif any(match_hostmask(connection, mask) for mask in channel.bans):
                connection.process_reply(ERR_BANNEDFROMCHAN, channel=channel_name)
                return
            elif 'i' in channel.modes and connection.nickname not in channel.invites:
                connection.process_reply(ERR_INVITEONLYCHAN, channel=channel_name)
                return

        channel.users.append(connection)
        connection.process_reply(RPL_TOPIC, channel.topic)
        for conn in (channel.users + self.servers):
            conn.reply()
