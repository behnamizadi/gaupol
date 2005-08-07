# Copyright (C) 2005 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""Conversions between tags of different subtitle formats."""


import re

try:
    from psyco.classes import *
except ImportError:
    pass

from gaupol.lib.tags.all import *


class TagConverter(object):
    
    """
    Conversions between tags of different subtitle formats.
    
    Tag conversions are done via an internal format, which has a HTML style
    syntax. All essential tags are converted and troublesome tags, such as
    position, and rare tags are removed.
    """
    
    def __init__(self, from_format, to_format):

        from_tags = eval(from_format).DECODE_TAGS
        to_tags   = eval(  to_format).ENCODE_TAGS

        self._from_res = []
        self._to_res   = []

        PATTERN, FLAGS, REPL = 0, 1, 2

        for entry in from_tags:
            try:
                regex = re.compile(entry[PATTERN], entry[FLAGS])
            except TypeError:
                regex = re.compile(entry[PATTERN])
            self._from_res.append([regex, entry[REPL]])

        for entry in to_tags:
            try:
                regex = re.compile(entry[PATTERN], entry[FLAGS])
            except TypeError:
                regex = re.compile(entry[PATTERN])
            self._to_res.append([regex, entry[REPL]])

    def convert_tags(self, string):
        """Convert subtitle tags in string."""

        if not string:
            return string

        REGEX, REPL = 0, 1

        # Convert to internal format ("decode").
        for entry in self._from_res:
            string = entry[REGEX].sub(entry[REPL], string)
        
        # Convert to desired format ("encode").
        for entry in self._to_res:
            string = entry[REGEX].sub(entry[REPL], string)

        return string