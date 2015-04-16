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

import wx
import wx.lib.scrolledpanel as scrolled

import Manager.ui.CustomCheckBox as CCB
import Manager.consts as consts

# ---------------------------------------------------------------------------


class CheckListPanel( scrolled.ScrolledPanel ):
    """
    Store a list of strings.
    Allows to check/uncheck.
    """

    def __init__(self, parent, ID=0, pos=wx.DefaultPosition, size=wx.DefaultSize):

        scrolled.ScrolledPanel.__init__(self, parent, -1, style=wx.TAB_TRAVERSAL|wx.NO_BORDER)
        self.SetBackgroundColour( consts.BACKGROUND_COLOR )
        
        # members
        self._ccblist = list()

        # Create the main sizer
        sizer = wx.BoxSizer( wx.VERTICAL )

        # create the sizer items
        self._text = wx.StaticText(self, -1, "List of identifiers:")
        self._text.SetBackgroundColour( consts.BACKGROUND_COLOR )
        sizer.Add(self._text, proportion=0, flag=wx.ALL, border=5 )

        self._ccbsizer = wx.BoxSizer( wx.VERTICAL )
        sizer.Add(self._ccbsizer, proportion=1, flag=wx.ALL, border=5 )

        self.SetSize(wx.Size(180, 300))
        self.SetSizer( sizer )
        self.SetAutoLayout( True )
        self._LayoutFrame()
        self.SetupScrolling()

    # End __init__
    # ----------------------------------------------------------------------


    def _LayoutFrame(self):
        self.Layout()
        self.SendSizeEvent()

    # ----------------------------------------------------------------------


    # ----------------------------------------------------------------------
    # CCB Callbacks
    # ----------------------------------------------------------------------


    def OnCheckBox(self, event):
        """
        Action when a check box is clicked.
        """

        # Grab the CustomCheckBox that generated the event
        control = event.GetEventObject()
        selid = control.GetLabelText()

        # Get the checked/unchecked value
        value = event.IsChecked()

        # Uncheck the other ccb
        for ccb in self._ccblist:
            if ccb != control:
                ccb.SetValue( False )

        if value is True:
            wx.GetTopLevelParent(self).SetSelected( selid )
        elif value is False:
            wx.GetTopLevelParent(self).UnsetSelected( )

    # End OnCheckBox
    # ----------------------------------------------------------------------


    # ----------------------------------------------------------------------
    # Manage the list of files
    # ----------------------------------------------------------------------

    def AddData(self, flist):
        """
        Add a list of new entries in the list.
        """
        for f in flist:
            self.SetData(f)
        self._LayoutFrame()


    def SetData(self, f):
        """
        Add a new entry in the list.
        """

        # create a CustomCheckBox.
        ccb = CCB.CustomCheckBox(self, -1, f, CCB_MULTIPLE=False)
        ccb.SetBackgroundColour( consts.BACKGROUND_COLOR )
        ccb.SetSpacing( 5 )

        # put the ccb in a sizer (required to enable ccbsizer.Remove())
        s = wx.BoxSizer( wx.HORIZONTAL )
        s.Add(ccb, 1, wx.EXPAND)
        self._ccbsizer.Add(s, proportion=0, flag=wx.TOP, border=10 )

        # add in the list of files
        self._ccblist.append(ccb)

        self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox, ccb)

    # End SetData
    # ----------------------------------------------------------------------


    def UnsetData(self, f):
        """
        Remove the given entry.
        """

        for i,ccb in enumerate(self._ccblist):
            if f == ccb.GetLabelText():
                ccb.Destroy()
                self._ccbsizer.Remove(i)
                del self._ccblist[i]
                self._LayoutFrame()

    # End UnsetData
    # ----------------------------------------------------------------------


    def UnsetSelectedData(self):
        """
        Remove the checked entry.
        """

        for i,ccb in enumerate(self._ccblist):
            if ccb.GetValue() is True:
                ccb.Destroy()
                self._ccbsizer.Remove(i)
                del self._ccblist[i]

        self._LayoutFrame()

    # End UnsetCurrentData
    # ----------------------------------------------------------------------


    def UnsetAllData(self):
        """
        Remove all entries.
        """

        for ccb in self._ccblist:
            ccb.Destroy()
        del self._ccblist
        self._ccblist =list()
        self._ccbsizer.DeleteWindows()
        self._LayoutFrame()

    # End UnsetCurrentData
    # ----------------------------------------------------------------------


    def Select(self, f):
        """
        Check an entry.
        """

        if f is None:
            return
        for ccb in self._ccblist:
            if f == ccb.GetLabelText():
                ccb.SetValue( True )
            else:
                ccb.SetValue( False )

    # End Select
    # ----------------------------------------------------------------------


    def GetSelection(self):
        """
        Return the label text of the selected ccb.
        """
        for ccb in self._ccblist:
            if ccb.IsChecked():
                return ccb.GetLabelText()
        return ''

    # End GetSelection
    # ----------------------------------------------------------------------


    def EmptySelect(self, f):
        """
        Un-select an entry.
        """

        if f is None:
            return
        for ccb in self._ccblist:
            if f == ccb.GetLabelText():
                ccb.SetValue( False )

    # End EmptySelect
    # ----------------------------------------------------------------------

# --------------------------------------------------------------------------
