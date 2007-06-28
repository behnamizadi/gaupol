# Copyright (C) 2005-2007 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA 02110-1301, USA.


"""Updating the application GUI."""


import gaupol.gtk
import gobject
import gtk
import os
_ = gaupol.i18n._


class UpdateAgent(gaupol.Delegate):

    """Updating the application GUI.

    Instance attributes:
     * _message_id:  Statusbar message ID
     * _message_tag: Statusbar GObject timeout tag
    """

    # pylint: disable-msg=E0203,W0201

    __metaclass__ = gaupol.Contractual

    def __init__(self, master):

        gaupol.Delegate.__init__(self, master)
        self._message_id = None
        self._message_tag = None

    def _disable_widgets(self):
        """Make widgets unsensitive and blank."""

        self.tooltips.disable()
        self.window.set_title("Gaupol")
        self.video_button.get_data("label").set_text("")
        self.push_message(None)

    def _update_actions(self, page):
        """Update sensitivities of all UI manager actions for page."""

        action_group = self.get_action_group("main")
        for action in action_group.list_actions():
            action.update_sensitivity(self, page)

    @gaupol.gtk.util.asserted_return
    def _update_revert(self, page):
        """Update tooltips for undo and redo."""

        assert page is not None
        if page.project.can_undo():
            tip = _('Undo "%s"') % page.project.undoables[0].description
            self.get_action("undo_action").props.tooltip = tip
        if page.project.can_redo():
            tip = _('Redo "%s"') % page.project.redoables[0].description
            self.get_action("redo_action").props.tooltip = tip

    def _update_widgets(self, page):
        """Update the states of widgets."""

        if page is None:
            return self._disable_widgets()
        self.tooltips.enable()
        self.window.set_title(page.tab_label.get_text())
        self.get_action(page.edit_mode.action).set_active(True)
        self.get_action(page.project.framerate.action).set_active(True)
        self.framerate_combo.set_active(page.project.framerate)
        for i, name in enumerate(gaupol.gtk.COLUMN.actions):
            visible = page.view.get_column(i).props.visible
            self.get_action(name).set_active(visible)
        video = os.path.basename(page.project.video_path or "")
        self.video_button.get_data("label").set_text(video)
        self.tooltips.set_tip(self.video_button, page.project.video_path)

    def flash_message(self, message):
        """Show message in the statusbar for a short while."""

        self.push_message(message)
        method = self.push_message
        self._message_tag = gobject.timeout_add(6000, method, None)

    def on_activate_next_project_activate(self, *args):
        """Activate the project in the next tab."""

        self.notebook.next_page()

    def on_activate_previous_project_activate(self, *args):
        """Activate the project in the previous tab."""

        self.notebook.prev_page()

    def on_conf_application_window_notify_toolbar_style(self, *args):
        """Change the style of the main toolbar."""

        toolbar = self.uim.get_widget("/ui/main_toolbar")
        style = gaupol.gtk.conf.application_window.toolbar_style
        if style == gaupol.gtk.TOOLBAR_STYLE.DEFAULT:
            return toolbar.unset_style()
        toolbar.set_style(style.value)

    def on_move_tab_left_activate(self, *args):
        """Move the current tab to the left."""

        page = self.get_current_page()
        scroller = page.view.get_parent()
        index = self.pages.index(page)
        self.notebook.reorder_child(scroller, index - 1)

    def on_move_tab_right_activate(self, *args):
        """Move the current tab to the right."""

        page = self.get_current_page()
        scroller = page.view.get_parent()
        index = self.pages.index(page)
        self.notebook.reorder_child(scroller, index + 1)

    def on_notebook_page_reordered_ensure(self, value, *args, **kwargs):
        for i, page in enumerate(self.pages):
            value = self.notebook.get_nth_page(i)
            assert value.get_child() == page.view

    def on_notebook_page_reordered(self, notebook, scroller, index):
        """Update the list of pages to match the new order."""

        view = scroller.get_child()
        page = [x for x in self.pages if x.view == view][0]
        self.pages.remove(page)
        self.pages.insert(index, page)
        self.update_gui()
        self.emit("pages-reordered", page, index)

    @gaupol.gtk.util.asserted_return
    def on_notebook_switch_page(self, notebook, pointer, index):
        """Update GUI for the page switched to."""

        assert self.pages
        page = self.pages[index]
        self.update_gui()
        page.view.grab_focus()

    @gaupol.gtk.util.asserted_return
    def on_view_button_press_event(self, view, event):
        """Display a pop-up menu to edit data."""

        assert event.button == 3
        x = int(event.x)
        y = int(event.y)
        value = view.get_path_at_pos(x, y)
        assert value is not None
        path, column, x, y = value
        if path[0] not in view.get_selected_rows():
            view.set_cursor(path[0], column)
            view.update_headers()
        menu = self.uim.get_widget("/ui/view_popup")
        menu.popup(None, None, None, event.button, event.time)
        return True

    def on_view_move_cursor(self, *args):
        """Update GUI after moving cursor in the view."""

        self.update_gui()

    def on_view_selection_changed(self, *args):
        """Update GUI after changing selection in the view."""

        self.update_gui()

    def on_window_window_state_event(self, window, event):
        """Save window maximization."""

        state = event.new_window_state
        maximized = bool(state & gtk.gdk.WINDOW_STATE_MAXIMIZED)
        gaupol.gtk.conf.application_window.maximized = maximized

    def push_message(self, message):
        """Show message in the statusbar."""

        if self._message_tag is not None:
            gobject.source_remove(self._message_tag)
        if self._message_id is not None:
            self.statusbar.remove(0, self._message_id)
        event_box = self.statusbar.get_ancestor(gtk.EventBox)
        self.tooltips.set_tip(event_box, message)
        if message is not None:
            self._message_id = self.statusbar.push(0, message)
        return False

    def update_gui(self):
        """Update widget sensitivities and states for the current page."""

        page = self.get_current_page()
        self._update_actions(page)
        self._update_widgets(page)
        self._update_revert(page)