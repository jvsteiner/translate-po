#!/usr/bin/env python3
"""
This script is used to fix spaces in translations, in case the translations
output has different trailing and leading spaces than in the original.
"""

import polib


def count_spaces(s):
    left = len(s) - len(s.lstrip())
    right = len(s) - len(s.rstrip())
    return (left*" ", right*" ")


def replace_spaces(s, counts):
    return counts[0] + s + counts[1]


def main(args):
    pofile = polib.pofile(args[0])
    for entry in pofile:
        whitespace = count_spaces(entry.msgid)
        entry.msgstr = replace_spaces(entry.msgstr, whitespace)
    pofile.save(args[1])


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
