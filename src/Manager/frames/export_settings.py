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

from Manager.models.prefs import Option
from Manager.models.themes import THEMES


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
        wx.Dialog.__init__(self, parent, title=title, style=wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP)

        # Members
        self._prefsIO = prefs
        
        # Frame construction
        sizer = wx.BoxSizer( wx.VERTICAL )
        self._create_notebook( sizer )
        self._create_buttons( sizer )
        self._set_properties( sizer )

    # End __init__
    #-------------------------------------------------------------------------


    def _create_notebook(self, sizer):
        """ Put a notebook in the sizer. """

        # Create a notebook to sort preferences, and its pages
        nb = wx.Notebook(self)
        page1 = ThemeSettings(nb, self._prefsIO)

        # add the pages to the notebook with the label to show on the tab
        nb.AddPage(page1, "Merge PDF")

        sizer.Add(nb, 1, wx.EXPAND)

    #-------------------------------------------------------------------------


    def _create_buttons(self, sizer):
        """ The buttons to close, save, cancel, etc. """

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        ButtonClose  = wx.Button(self, wx.ID_OK)
        ButtonCancel = wx.Button(self, wx.ID_CANCEL)
        #ButtonSave   = wx.Button(self, wx.ID_SAVE)
        #hbox.Add(ButtonSave,   0, flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, border=5)
        hbox.Add(ButtonClose,  0, flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, border=5)
        hbox.Add(ButtonCancel, 0, flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, border=5)

        self.Bind(wx.EVT_BUTTON, self.onSave,  id=wx.ID_SAVE)

        sizer.Add(hbox, 0, flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, border=0)

    #-------------------------------------------------------------------------


    def _set_properties(self, sizer):
        """ Fix the dialog properties. """

        self.SetSizer(sizer)
        self.SetMinSize(wx.Size(500,320))
        self.Centre()
        self.SetFocus()
        self.SetAutoLayout( True )
        self.Layout()


    #-------------------------------------------------------------------------
    # Callbacks
    #-------------------------------------------------------------------------

    def onSave(self, event):
        """ Save preferences in a file. """

        self._prefsIO.Write()

    #-------------------------------------------------------------------------


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
