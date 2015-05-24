#!/usr/bin/python
# -*- coding: UTF-8 -*-
# ---------------------------------------------------------------------------
#         ___    __    ___    ___  ____  ____   __
#         |  \  |  \  |   |  /     |     |     |  \   Automatic
#         |__/  |__/  |   |  |     |__   |__   |   |    Conference
#         |     |\_   |   |  |     |     |     |   |    Proceedings
#         |     |  \  |___|  \___  |___  |___  |__/   Generator
#        ==========================================================
#
#           http://www.lpl-aix.fr/~bigi/
#
# ---------------------------------------------------------------------------
# developed at:
#
#       Laboratoire Parole et Langage
#
#       Copyright (C) 2013-2014  Brigitte Bigi
#
#       Use of this software is governed by the GPL, v3
#       This banner notice must not be removed
# ---------------------------------------------------------------------------
#
# Proceed is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Proceed is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Proceed. If not, see <http://www.gnu.org/licenses/>.
#
# ---------------------------------------------------------------------------

__docformat__ = "epytext"


# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

import wx
import os.path
import wx.lib.scrolledpanel as scrolled

from wxgui.models.prefs import Option
from wxgui.models.themes import THEMES

from wxgui.sp_icons import SETTINGS_ICON
from wxgui.sp_icons import SAVE_ICON
from wxgui.sp_icons import APPLY_ICON
from wxgui.sp_icons import CANCEL_ICON
from wxgui.sp_icons import APP_ICON

from wxgui.cutils.imageutils import spBitmap
from wxgui.cutils.ctrlutils import CreateGenButton

from wxgui.sp_consts import FRAME_STYLE
from wxgui.sp_consts import FRAME_TITLE
from wxgui.sp_consts import HEADER_FONTSIZE

from sp_glob import ICONS_PATH

# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------

ID_SAVE   = wx.NewId()

# ---------------------------------------------------------------------------
# Main Settings Frame class
# ---------------------------------------------------------------------------

class ExportSettings( wx.Dialog ):
    """
    Dialog for the user to fix all settings.

    @author: Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: This class is used to fix all user's settings, with a Dialog.

    """

    def __init__(self, parent, title, prefs):
        """
        Create a new dialog fo fix preferences, sorted in a notebook.

        """
        wx.Dialog.__init__(self, parent, title=FRAME_TITLE+" - Settings", style=FRAME_STYLE)

        # Members
        self._prefsIO = prefs

        self._create_gui()

        # Events of this frame
        wx.EVT_CLOSE(self, self.onClose)

    # End __init__
    # ------------------------------------------------------------------------

    # ------------------------------------------------------------------------
    # Create the GUI
    # ------------------------------------------------------------------------

    def _create_gui(self):
        self._init_infos()
        self._create_title_label()
        self._create_notebook()
        self._create_save_button()
        self._create_cancel_button()
        self._create_close_button()
        self._layout_components()
        self._set_focus_component()

    # End __init__
    #-------------------------------------------------------------------------

    def _init_infos( self ):
        wx.GetApp().SetAppName( "settings" )
        # icon
        _icon = wx.EmptyIcon()
        _icon.CopyFromBitmap( spBitmap(APP_ICON) )
        self.SetIcon(_icon)

    def _create_title_label(self):
        self.title_layout = wx.BoxSizer(wx.HORIZONTAL)
        bmp = wx.BitmapButton(self, bitmap=spBitmap(SETTINGS_ICON, 32), style=wx.NO_BORDER)
        font = wx.Font(HEADER_FONTSIZE, wx.MODERN, wx.NORMAL, wx.BOLD, False, u'Consolas')
        self.title_label = wx.StaticText(self, label="User settings", style=wx.ALIGN_CENTER)
        self.title_label.SetFont( font )
        self.title_layout.Add(bmp,  flag=wx.TOP|wx.RIGHT|wx.ALIGN_RIGHT, border=5)
        self.title_layout.Add(self.title_label, flag=wx.EXPAND|wx.ALL|wx.wx.ALIGN_CENTER_VERTICAL, border=5)

    def _create_notebook(self):
        self.notebook = wx.Notebook(self)
        page1 = ThemeSettings(self.notebook, self._prefsIO)
        #page2 = PrefsThemePanel(self.notebook, self.preferences)
        #page3 = PrefsAnnotationPanel(self.notebook, self.preferences)
        # add the pages to the notebook with the label to show on the tab
        self.notebook.AddPage(page1, "General")
        #self.notebook.AddPage(page2, "Icons Theme")
        #self.notebook.AddPage(page3, "Annotation")

    #-------------------------------------------------------------------------

    def _create_save_button(self):
        bmp = spBitmap(SAVE_ICON)
        self.btn_save = CreateGenButton(self, wx.ID_SAVE, bmp, text="Save", tooltip="Save the settings")
        self.Bind(wx.EVT_BUTTON, self.onSave, self.btn_save, wx.ID_SAVE)

    def _create_cancel_button(self):
        bmp = spBitmap(CANCEL_ICON)
        self.btn_cancel = CreateGenButton(self, wx.ID_CANCEL, bmp, text=" Cancel", tooltip="Close this frame")
        self.SetEscapeId(wx.ID_CANCEL)

    def _create_close_button(self):
        bmp = spBitmap(APPLY_ICON)
        self.btn_close = CreateGenButton(self, wx.ID_OK, bmp, text=" Close", tooltip="Close this frame")
        self.btn_close.SetDefault()
        self.btn_close.SetFocus()
        self.SetAffirmativeId(wx.ID_OK)

    def _create_button_box(self):
        button_box = wx.BoxSizer(wx.HORIZONTAL)
        button_box.Add(self.btn_save, flag=wx.RIGHT, border=5)
        button_box.AddStretchSpacer()
        button_box.Add(self.btn_cancel, flag=wx.RIGHT, border=5)
        button_box.Add(self.btn_close, flag=wx.RIGHT, border=5)
        return button_box

    def _layout_components(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.title_layout, 0, flag=wx.ALL|wx.EXPAND, border=5)
        vbox.Add(self.notebook, 1, flag=wx.ALL|wx.EXPAND, border=0)
        vbox.Add(self._create_button_box(), 0, flag=wx.ALL|wx.EXPAND, border=5)
        self.SetSizerAndFit(vbox)

    def _set_focus_component(self):
        self.notebook.SetFocus()

    #-------------------------------------------------------------------------

    #-------------------------------------------------------------------------
    # Callbacks
    #-------------------------------------------------------------------------

    def onSave(self, event):
        """ Save preferences in a file. """

        self._prefsIO.Write()

    #-------------------------------------------------------------------------

    def onClose(self, event):
        self.SetEscapeId(wx.ID_CANCEL)


    #-------------------------------------------------------------------------
    # Getters...
    #-------------------------------------------------------------------------

    def GetPreferences(self):
        """ Return the preferences. """

        return self._prefsIO

    #-------------------------------------------------------------------------


# ----------------------------------------------------------------------------


class ThemeSettings( scrolled.ScrolledPanel ):
    """
    Merge PDF.
    """

    def __init__(self, parent, prefsIO):

        scrolled.ScrolledPanel.__init__(self, parent, style=wx.NO_BORDER)

        self._prefsIO = prefsIO

        choices = []
        for choice in THEMES:
            choices.append(choice[0])
        # TODO:
        # Append a "User defined" theme in the choices, allowing the user
        # to make it's own setting for each option, and save them.

        self.radiobox = wx.RadioBox(self, label="Conference: ",
                                    choices=choices, majorDimension=1)

        # check the current theme
        self.radiobox.SetSelection( self._prefsIO.GetTheme() )
        # bind any theme change
        self.Bind(wx.EVT_RADIOBOX, self.radioClick, self.radiobox)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.radiobox, 1, wx.EXPAND|wx.ALL, border=2)
        self.SetSizer(vbox)

    #-------------------------------------------------------------------------

    def radioClick(self, event):
        """ Set the new theme. """
        self._prefsIO.SetTheme(self.radiobox.GetSelection())


# ----------------------------------------------------------------------------
