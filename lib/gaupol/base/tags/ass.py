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


"""Advanced Sub Station Alpha tag library."""


import re

from gaupol.base.tags.ssa import SubStationAlpha


class AdvancedSubStationAlpha(SubStationAlpha):

    """Advanced Sub Station Alpha tag library."""

    decode_tags = [
        (
            # Underline opening
            r'\{\\u1\}', re.IGNORECASE,
            r'<u>'
        ), (
            # Underline closing
            r'\{\\u0\}', re.IGNORECASE,
            r'</u>'
        )
    ] + SubStationAlpha.decode_tags

    encode_tags = [
        (
            # Underline opening
            r'<u>', re.IGNORECASE,
            r'{\\u1}'
        ), (
            # Underline closing
            r'</u>', re.IGNORECASE,
            r'{\\u0}'
        )
    ] + SubStationAlpha.encode_tags