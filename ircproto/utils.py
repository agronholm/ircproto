import re

from ircproto.exceptions import ProtocolError

nickname_re = re.compile(b'[a-zA-Z[\]\\\\`_^{|}][a-zA-Z[\]\\\\`_^{|}0-9-]{0,8}$')
channel_re = re.compile(b'([#+&]|![A-Z0-9]{5})[^\x00\x0b\r\n ,:]+$')
hostmask_re = re.compile(b'(?:[^\x00?*]|[^\x00\\\\]\\?|\\*)+')


def validate_channel_name(name):
    """
    Ensure that a channel name conforms to the restrictions of RFC 2818.

    :param bytes name: the channel name to validate
    :raises ..exceptions.ProtocolError: if the channel name is invalid

    """
    if not channel_re.match(name):
        raise ProtocolError(u'invalid channel name: %s' % name.decode('ascii',
                                                                      errors='backslashreplace'))


def validate_nickname(name):
    """
    Ensure that a nickname conforms to the restrictions of RFC 2818.

    :param bytes name: the nickname to validate
    :raises ..exceptions.ProtocolError: if the nickname is invalid

    """
    if not nickname_re.match(name):
        raise ProtocolError(u'invalid nickname: %s' % name.decode('ascii',
                                                                  errors='backslashreplace'))


def validate_hostmask(mask):
    """
    Ensure that a host mask conforms to the restrictions of RFC 2818.

    :param bytes mask: the mask to validate
    :raises ..exceptions.ProtocolError: if the host mask is invalid

    """
    if not hostmask_re.match(mask):
        raise ProtocolError(u'invalid host mask: %s' % mask.decode('ascii',
                                                                   errors='backslashreplace'))


def match_hostmask(prefix, mask):
    """
    Match a prefix against a hostmask.

    :param bytes prefix: prefix to match the mask against
    :param bytes mask: a mask that may contain wildcards like ``*`` or ``?``
    :return: ``True`` if the prefix matches the mask, ``False`` otherwise

    """
    prefix_index = mask_index = 0
    escape = False
    while prefix_index < len(prefix) and mask_index < len(mask):
        mask_char = mask[mask_index]
        prefix_char = prefix[prefix_index]
        if mask[mask_index] == b'\\':
            escape = True
            mask_index += 1
            mask_char = mask[mask_index]

        prefix_index += 1
        mask_index += 1
        if escape or mask_char not in b'?*':
            if mask_char != prefix_char:
                return False
        elif mask_char == b'?':
            pass
        elif mask_char == b'*':
            if mask_index < len(mask):
                mask_char = mask[mask_index]
                prefix_index = prefix.find(mask_char, prefix_index)
                if prefix_index == -1:
                    return False
            else:
                break

    return True
