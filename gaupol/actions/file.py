# -*- coding: utf-8 -*-

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

"""File and project actions for :class:`gaupol.Application`."""

import aeidon
import gaupol
_ = aeidon.i18n._

from gi.repository import Gtk


class AppendFileAction(gaupol.Action):

    """Append subtitles from file to the current project."""

    def __init__(self):
        """Initialize an :class:`AppendFileAction` object."""
        gaupol.Action.__init__(self, "append_file")
        self.props.label = _("_Append File…")
        self.props.stock_id = Gtk.STOCK_ADD
        self.props.tooltip = _("Append subtitles from file "
                               "to the current project")

        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(len(page.project.subtitles) > 0)


class CloseAllProjectsAction(gaupol.Action):

    """Close all open projects."""

    def __init__(self):
        """Initialize a :class:`CloseAllProjectsAction` object."""
        gaupol.Action.__init__(self, "close_all_projects")
        self.props.label = _("_Close All")
        self.props.stock_id = Gtk.STOCK_CLOSE
        self.props.tooltip =  _("Close all open projects")
        self.accelerator = "<Shift><Control>W"
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(application.pages)


class CloseProjectAction(gaupol.Action):

    """Close project."""

    def __init__(self):
        """Initialize a :class:`CloseProjectAction` object."""
        gaupol.Action.__init__(self, "close_project")
        self.props.label = _("_Close")
        self.props.stock_id = Gtk.STOCK_CLOSE
        self.props.tooltip = _("Close the current project")
        self.accelerator = "<Control>W"
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)


class EditHeadersAction(gaupol.Action):

    """Edit file headers."""

    def __init__(self):
        """Initialize an :class:`EditHeadersAction` object."""
        gaupol.Action.__init__(self, "edit_headers")
        self.props.label = _("_Headers")
        self.props.stock_id = Gtk.STOCK_PROPERTIES
        self.props.tooltip = _("Edit file headers")
        self.accelerator = "<Alt>Return"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        has_header_found = False
        if page.project.main_file is not None:
            if page.project.main_file.format.has_header:
                has_header_found = True
        if page.project.tran_file is not None:
            if page.project.tran_file.format.has_header:
                has_header_found = True
        aeidon.util.affirm(has_header_found)


class NewProjectAction(gaupol.Action):

    """Create a new project."""

    def __init__(self):
        """Initialize a :class:`NewProjectAction` object."""
        gaupol.Action.__init__(self, "new_project")
        self.props.label = _("_New")
        self.props.stock_id = Gtk.STOCK_NEW
        self.props.tooltip = _("Create a new project")
        self.accelerator = "<Control>N"
        self.action_group = "main-safe"


class OpenMainFilesAction(gaupol.Action):

    """Open main files."""

    __gtype_name__ = "OpenMainFilesAction"

    def __init__(self):
        """Initialize an :class:`OpenMainFilesAction` object."""
        gaupol.Action.__init__(self, "open_main_files")
        self.props.is_important = True
        self.props.label = _("_Open…")
        self.props.short_label = _("Open")
        self.props.stock_id = Gtk.STOCK_OPEN
        self.props.tooltip = _("Open main files")
        self.accelerator = "<Control>O"
        self.action_group = "main-safe"


class OpenMainFilesRecentAction(gaupol.RecentAction):

    """Open main files."""

    group = "gaupol-main"

    def __init__(self):
        """Initialize an :class:`OpenMainFilesRecentAction` object."""
        gaupol.RecentAction.__init__(self, "open_main_files_recent")
        self.props.is_important = True
        self.props.label = _("_Open…")
        self.props.short_label = _("Open")
        self.props.stock_id = Gtk.STOCK_OPEN
        self.props.tooltip = _("Open main files")
        self.action_group = "main-safe"


class OpenRecentMainFileAction(gaupol.RecentAction):

    """Show the recent main file menu."""

    group = "gaupol-main"

    def __init__(self):
        """Initialize a :class:`OpenRecentMainFileAction` object."""
        gaupol.RecentAction.__init__(self, "open_recent_main_file")
        self.props.is_important = True
        self.props.label = _("Open _Recent")
        self.action_group = "main-safe"


class OpenRecentTranslationFileAction(gaupol.RecentAction):

    """Show the recent translation file menu."""

    group = "gaupol-translation"

    def __init__(self):
        """Initialize a :class:`OpenRecentTranslationFileAction` object."""
        gaupol.RecentAction.__init__(self, "open_recent_translation_file")
        self.props.is_important = False
        self.props.label = _("Open R_ecent Translation")
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)


class OpenTranslationFileAction(gaupol.Action):

    """Open a translation file."""

    def __init__(self):
        """Initialize an :class:`OpenTranslationFileAction` object."""
        gaupol.Action.__init__(self, "open_translation_file")
        self.props.label = _("Open _Translation…")
        self.props.short_label = _("Open Translation")
        self.props.stock_id = Gtk.STOCK_OPEN
        self.props.tooltip = _("Open a translation file")
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.main_file is not None)


class QuitAction(gaupol.Action):

    """Quit Gaupol."""

    def __init__(self):
        """Initialize a :class:`QuitAction` object."""
        gaupol.Action.__init__(self, "quit")
        self.props.label = _("_Quit")
        self.props.stock_id = Gtk.STOCK_QUIT
        self.props.tooltip = _("Quit Gaupol")
        self.accelerator = "<Control>Q"
        self.action_group = "main-safe"


class SaveAllDocumentsAction(gaupol.Action):

    """Save all open documents."""

    def __init__(self):
        """Initialize a :class:`SaveAllDocumentsAction` object."""
        gaupol.Action.__init__(self, "save_all_documents")
        self.props.label = _("_Save All")
        self.props.stock_id = Gtk.STOCK_SAVE
        self.props.tooltip = _("Save all open documents")
        self.accelerator = "<Shift><Control>L"
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(application.pages)


class SaveAllDocumentsAsAction(gaupol.Action):

    """Save all open documents with different properties."""

    def __init__(self):
        """Initialize a :class:`SaveAllDocumentsAsAction` object."""
        gaupol.Action.__init__(self, "save_all_documents_as")
        self.props.label = _("Save _All As…")
        self.props.stock_id = Gtk.STOCK_SAVE_AS
        self.props.tooltip = _("Save all open documents with "
                               "different properties")

        self.action_group = "main-safe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm([x for x in application.pages
                            if x.project.main_file is not None])


class SaveMainDocumentAction(gaupol.Action):

    """Save the current main document."""

    def __init__(self):
        """Initialize a :class:`SaveMainDocumentAction` object."""
        gaupol.Action.__init__(self, "save_main_document")
        self.props.is_important = True
        self.props.label = _("_Save")
        self.props.stock_id = Gtk.STOCK_SAVE
        self.props.tooltip = _("Save the current main document")
        self.accelerator = "<Control>S"
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)


class SaveMainDocumentAsAction(gaupol.Action):

    """Save the current main document with a different name."""

    def __init__(self):
        """Initialize a :class:`SaveMainDocumentAsAction` object."""
        gaupol.Action.__init__(self, "save_main_document_as")
        self.props.label = _("Save _As…")
        self.props.short_label = _("Save As")
        self.props.stock_id = Gtk.STOCK_SAVE_AS
        self.props.tooltip = _("Save the current main document "
                               "with a different name")

        self.accelerator = "<Shift><Control>S"
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)


class SaveTranslationDocumentAction(gaupol.Action):

    """Save the current translation document."""

    def __init__(self):
        """Initialize a :class:`SaveTranslationDocumentAction` object."""
        gaupol.Action.__init__(self, "save_translation_document")
        self.props.label = _("Save Trans_lation")
        self.props.stock_id = Gtk.STOCK_SAVE
        self.props.tooltip = _("Save the current translation document")
        self.accelerator = "<Control>T"
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)


class SaveTranslationDocumentAsAction(gaupol.Action):

    """Save the current translation document with a different name."""

    def __init__(self):
        """Initialize a :class:`SaveTranslationDocumentAsAction` object."""
        gaupol.Action.__init__(self, "save_translation_document_as")
        self.props.label = _("Save Translat_ion As…")
        self.props.short_label = _("Save Translation As")
        self.props.stock_id = Gtk.STOCK_SAVE_AS
        self.props.tooltip = _("Save the current translation document "
                               "with a different name")

        self.accelerator = "<Shift><Control>T"
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)


class SelectVideoFileAction(gaupol.Action):

    """Select a video file."""

    def __init__(self):
        """Initialize a :class:`SelectVideoFileAction` object."""
        gaupol.Action.__init__(self, "select_video_file")
        self.props.label = _("Select _Video…")
        self.props.stock_id = Gtk.STOCK_FILE
        self.props.tooltip = _("Select a video file")
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.main_file is not None)


class SplitProjectAction(gaupol.Action):

    """Split the current project in two."""

    def __init__(self):
        """Initialize a :class:`SplitProjectAction` object."""
        gaupol.Action.__init__(self, "split_project")
        self.props.label = _("Spli_t Project…")
        self.props.tooltip = _("Split the current project in two")
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(len(page.project.subtitles) > 1)


__all__ = tuple(x for x in dir() if x.endswith("Action"))
