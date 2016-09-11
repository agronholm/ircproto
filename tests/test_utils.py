import pytest

from ircproto.exceptions import ProtocolError
from ircproto.utils import validate_nickname


@pytest.mark.parametrize('name', [
    b'a',
    b'[]\\_^{|}-',
    b'nick1'
])
def test_validate_nickname(name):
    validate_nickname(name)


@pytest.mark.parametrize('name', [
    b'',
    b'toolongggg',
    b'1nick',
    b'\x00nick',
    b'nick name'
], ids=['empty', 'toolong', 'starts_with_number', 'starts_with_nul', 'space'])
def test_validate_nickname_invalid(name):
    exc = pytest.raises(ProtocolError, validate_nickname, name)
    assert str(exc.value) == (u'IRC protocol violation: invalid nickname: %s' %
                              name.decode('ascii', errors='backslashreplace'))
