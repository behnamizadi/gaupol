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


"""Manual editing of subtitle data."""


try:
    from psyco.classes import *
except ImportError:
    pass

from gaupol.gui.constants import NO, SHOW, HIDE, DURN, ORIG, TRAN
from gaupol.gui.delegates.delegate import Delegate


class ManualEditAction(object):

    """Manual edit action for subtitle data."""
    
    def __init__(self, project, old_value, new_value, row, col):
        
        self.project   = project
        self.old_value = old_value
        self.new_value = new_value

        # row and col point to ListStore.
        self.row = row
        self.col = col

        if col == TRAN:
            self.document = 'translation'
        else:
            self.document = 'main'

        edit_mode = project.edit_mode
        subtitle  = row + 1

        DESCRIPTIONS = [
            None,
            _('Editing show %s of subtitle %d')     % (edit_mode, subtitle),
            _('Editing hide %s of subtitle %d')     % (edit_mode, subtitle),
            _('Editing duration of subtitle %d')    % subtitle,
            _('Editing text of subtitle %d')        % subtitle,
            _('Editing translation of subtitle %d') % subtitle,
        ]
        
        self.description = DESCRIPTIONS[col]
        
    def do(self):
        """Do editing."""

        self._set_value(self.new_value)

    def redo(self):
        """Redo editing."""
        
        self.do()

    def _set_value(self, value):
        """Set value to data."""

        store = self.project.tree_view.get_model()
        
        if self.col in [SHOW, HIDE, DURN]:
            section = self.project.edit_mode + 's'
            data_col = self.col - 1
        else:
            section = 'texts'
            data_col = self.col - 4

        data_row = store[self.row][NO] - 1
        new_data_row = self.project.data.set_single_value(
            section, data_col, data_row, value
        )
        
        if new_data_row == data_row:

            self.project.reload_tree_view_data_in_row(self.row)

        else:
        
            self.project.reload_tree_view_data_in_rows(data_row, new_data_row)
            
            subtitle = new_data_row + 1
            new_store_row = None
            
            for i in range(len(store)):
                if store[i][NO] == subtitle:
                    new_store_row = i
                    break

            tree_col = self.project.tree_view.get_column(self.col)
            self.project.tree_view.set_cursor(new_store_row, tree_col)

            # Instance variable pointing to store row needs to be updated to
            # be able to undo at the correct row.
            self.row = new_store_row
        
    def undo(self):
        """Undo editing."""

        self._set_value(self.old_value)


class ManualEditor(Delegate):

    """Manual editor for subtitle data."""

    def on_tree_view_cell_edited(self, project, new_value, row, col):
        """Edit value in tree view cell."""

        self._set_action_sensitivities(True)
        self.set_status_message(None)
        store = project.tree_view.get_model()

        # new_value is by default a string.
        if project.edit_mode == 'frame' and col in [SHOW, HIDE, DURN]:
            new_value = int(new_value)

        old_value = store[row][col]

        if old_value == new_value:
            return

        action = ManualEditAction(project, old_value, new_value, row, col)
        self.do_action(project, action)

    def on_tree_view_cell_editing_started(self, project, col):
        """Set menubar and toolbar actions insensitive while editing."""

        self._set_action_sensitivities(False)

        if col in [ORIG, TRAN]:
            message = _('Use Ctrl+Enter for line-break')
            self.set_status_message(message, False)

    def _set_action_sensitivities(self, sensitive):
        """Set  sensitivity of menubar and toolbar actions."""

        action_groups = self.uim.get_action_groups()
        for group in action_groups:
            group.set_sensitive(sensitive)

        self.uim.get_widget('/ui/toolbar').set_sensitive(sensitive)
        self.uim.get_widget('/ui/menubar').set_sensitive(sensitive)
