import pytest

from ircproto.events import decode_event
from ircproto.exceptions import ProtocolError, UnknownCommand


def test_decode_event_oversized():
    buffer = bytearray(b':foo!bar@blah PRIVMSG hey' + b'y' * 600 + b'\r\n')
    exc = pytest.raises(ProtocolError, decode_event, buffer)
    assert str(exc.value) == 'IRC protocol violation: received oversized message (627 bytes)'


def test_decode_event_unknown_command():
    buffer = bytearray(b':foo!bar@blah FROBNICATE\r\n')
    exc = pytest.raises(UnknownCommand, decode_event, buffer)
    assert str(exc.value) == 'IRC protocol violation: unknown command: FROBNICATE'


def test_decode_fallback_conversion():
    buffer = bytearray(b':foo!bar@blah PRIVMSG hey du\xe2\xa9k\r\n')
    assert decode_event(buffer, codec='utf-8', fallback_codec='iso-8859-1')
