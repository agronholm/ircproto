from __future__ import unicode_literals

import re
from enum import Enum


class IRCTextColor(Enum):
    """
    Enumeration of colors usable with :func:`styled`.

    Available values:
     * white
     * black
     * navy
     * green
     * red
     * maroon
     * purple
     * olive
     * yellow
     * lightgreen
     * teal
     * cyan
     * royalblue
     * magenta
     * gray
     * lightgray
    """

    white = 0
    black = 1
    navy = 2
    green = 3
    red = 4
    maroon = 5
    purple = 6
    olive = 7
    yellow = 8
    lightgreen = 9
    teal = 10
    cyan = 11
    royalblue = 12
    magenta = 13
    gray = 14
    lightgray = 15


class IRCTextStyle(Enum):
    """
    Enumeration of text styles usable with :func:`styled`.

    Available values:
     * bold
     * italic
     * underline
     * reverse
     * plain
    """

    bold = '\x02'
    italic = '\x1d'
    underline = '\x1f'
    reverse = '\x16'
    plain = '\x0f'

styles_re = re.compile('(\x03\d+(?:,\d+)?)|[\x02\x03\x1d\x1f\x16\x0f]')


def styled(text, foreground=None, background=None, styles=None):
    """
    Apply mIRC compatible colors and styles to the given text.

    :param text: the text to be styled
    :param foreground: the foreground color
    :param background: the background color (only works if foreground is defined too)
    :param styles: a text style or iterable of text styles to apply

    """
    # Apply coloring
    if foreground and not background:
        text = '\x03%d%s\x03' % (foreground.value, text)
    elif foreground and background:
        text = '\x03%d,%d%s\x03' % (foreground.value, background.value, text)

    # Apply text styles
    if styles:
        if isinstance(styles, IRCTextStyle):
            text = styles.value + text
        else:
            text = ''.join(style.value for style in styles) + text

        text += IRCTextStyle.plain.value  # reset to default at the end

    return text


def strip_styles(text):
    """
    Remove all mIRC compatible styles and coloring from the given text.

    :param str text: the text to be sanitized
    :return: input text with styles removed

    """
    return styles_re.sub('', text)
