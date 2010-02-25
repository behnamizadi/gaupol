# Copyright (C) 2005-2008,2010 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

"""Dialog for informing that preview failed."""

import gaupol
import gtk


class PreviewErrorDialog(gaupol.BuilderDialog):

    """Dialog for informing that preview failed."""

    widgets = ("text_view",)

    def __init__(self, parent, output):
        """Initialize a :class:`PreviewErrorDialog` object."""
        gaupol.BuilderDialog.__init__(self, "previewerr-dialog.ui")
        self._init_data(output)
        self._init_sizes()
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

    def _init_data(self, output):
        """Initialize output text in the text view."""
        text_buffer = self._text_view.get_buffer()
        text_buffer.create_tag("output", family="monospace")
        itr = text_buffer.get_end_iter()
        text_buffer.insert_with_tags_by_name(itr, output, "output")

    def _init_sizes(self):
        """Initialize widget sizes."""
        get_size = gaupol.util.get_text_view_size
        width, height = get_size(self._text_view, "monospace")
        width = width + 112 + gaupol.EXTRA
        width = min(width, int(0.5 * gtk.gdk.screen_width()))
        height = height + 148 + gaupol.EXTRA
        height = min(height, int(0.5 * gtk.gdk.screen_height()))
        self.set_default_size(width, height)
