class ProtocolError(Exception):
    """Raised by the state machine when the IRC protocol is being violated."""

    def __init__(self, message):
        super(ProtocolError, self).__init__(u'IRC protocol violation: %s' % message)


class UnknownCommand(ProtocolError):
    """Raised by the state machine when an unrecognized command has been received."""

    def __init__(self, command):
        super(UnknownCommand, self).__init__(u'unknown command: %s' % command)
