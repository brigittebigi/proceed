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

import os.path
import wx

from wxgui.sp_icons import APP_EXPORT_PDF_ICON
from wxgui.frames.export_settings import ExportSettings

from structs.prefs import Preferences_IO
from wxgui.models.writers import pdf_writer
from wxgui.models.writers import EVT_RESULT

# ---------------------------------------------------------------------------
# Class
# ---------------------------------------------------------------------------

class GenerateFrame( wx.Dialog ):
    """
    @authors: Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: Used to export data in a PDF document.

    """

    def __init__(self, parent, id, title, documents, authors, sessions, path):
        """
        Constructor.
        """
        wx.Dialog.__init__(self, parent, id, title, size=(380, 200),style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        _icon = wx.EmptyIcon()
        _icon.CopyFromBitmap( wx.Bitmap(APP_EXPORT_PDF_ICON, wx.BITMAP_TYPE_ANY) )
        self.SetIcon(_icon)

        self.SetMinSize((380, 200))

        sizer = self._create_content(self)

        # Members
        self.documents = documents
        self.authors   = authors
        self.sessions  = sessions
        self.path      = path
        self._prefsIO  = Preferences_IO()

        # Try to get prefs from a file, or fix default values.
        if not self._prefsIO.Read():
            self._reset_prefs()

        # And indicate we don't have a worker thread yet
        self.pdfwriter = None

        # Set up event handler for any worker thread results
        EVT_RESULT(self,self.OnResult)

        self.SetSizer(sizer)
        self.Centre()

    # End __init__
    # ------------------------------------------------------------------------


    def _reset_prefs(self):
        # Page
        self._prefsIO.SetValue('PAGE_FORMAT','str', 'a4paper')
        self._prefsIO.SetValue('PAGE_NUMBER','int', 1)
        self._prefsIO.SetValue("TOP_MARGIN",'int', 30)    # millimeters
        self._prefsIO.SetValue("BOTTOM_MARGIN",'int', 20) # millimeters
        self._prefsIO.SetValue("HEADER_SIZE",'int', 20)   # pt
        self._prefsIO.SetValue("FOOTER_SIZE",'int', 10)   # pt

        # Header
        self._prefsIO.SetValue('HEADER_LEFT','str', '')
        self._prefsIO.SetValue('HEADER_CENTER','str', '')
        self._prefsIO.SetValue('HEADER_RIGHT','str', '\\session')
        self._prefsIO.SetValue('HEADER_STYLE','str', '\\it') # "\\rm","\\it","\\em","\\emph","\\bf","\\sl","\\sf","\\sc","\\tt"
        self._prefsIO.SetValue('HEADER_COLOR','str', '20,20,20')
        self._prefsIO.SetValue('HEADER_RULER','bool', True)

        # Footer
        self._prefsIO.SetValue('FOOTER_LEFT','str', '')
        self._prefsIO.SetValue('FOOTER_CENTER','str', '\\thepage')
        self._prefsIO.SetValue('FOOTER_RIGHT','str', '')
        self._prefsIO.SetValue('FOOTER_STYLE','str', '\\bf') # "\\rm","\\it","\\em","\\emph","\\bf","\\sl","\\sf","\\sc","\\tt"
        self._prefsIO.SetValue('FOOTER_COLOR','str', '20,20,20')
        self._prefsIO.SetValue('FOOTER_RULER','bool', False)

        # Generate
        self._prefsIO.SetValue('GENERATE_PROGRAM','bool', True)
        self._prefsIO.SetValue('GENERATE_PROGRAM_OVERVIEW','bool', True)
        self._prefsIO.SetValue('GENERATE_TABLEOFCONTENTS','bool', True)
        self._prefsIO.SetValue('GENERATE_MERGED_SUBMISSIONS','bool', True)
        self._prefsIO.SetValue('GENERATE_AUTHORS_INDEX','bool', True)
        self._prefsIO.SetValue('GENERATE_AUTHORS_LIST','bool', True)

        # Titles
        self._prefsIO.SetValue('TITLE_PROGRAM','str', 'Program')
        self._prefsIO.SetValue('TITLE_PROGRAM_OVERVIEW','str', 'Program overview')
        self._prefsIO.SetValue('TITLE_TABLEOFCONTENTS','str', 'Table of contents')
        self._prefsIO.SetValue('TITLE_AUTHORS_INDEX','str', 'Author Index')
        self._prefsIO.SetValue('TITLE_AUTHORS_LIST','str', 'List of authors')

        # Sort by session types first (1. keynotes, then 2. orals then 3. posters)
        self._prefsIO.SetValue('SORT_BY_SESSION_TYPE_FIRST','bool', False)

    #-------------------------------------------------------------------------


    def _create_content(self, panel):
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)

        self.gauge = wx.Gauge(panel, -1, 6, size=(360, 30))
        self.text = wx.StaticText(panel, -1, 'Fix settings then click on the start button.')
        self.btn0 = wx.Button(panel, wx.ID_PREFERENCES, 'Settings')
        self.btn1 = wx.Button(panel, wx.ID_APPLY, 'Start')
        self.btn2 = wx.Button(panel, wx.ID_STOP, 'Stop')

        self.Bind(wx.EVT_BUTTON, self.OnPrefs, self.btn0)
        self.Bind(wx.EVT_BUTTON, self.OnOk,    self.btn1)
        self.Bind(wx.EVT_BUTTON, self.OnStop,  self.btn2)

        hbox1.Add(self.gauge, 1, wx.ALIGN_CENTRE)
        hbox2.Add(self.btn0, 1, wx.RIGHT,  5)
        hbox2.Add(self.btn1, 1, wx.LEFT, 5)
        hbox2.Add(self.btn2, 1, wx.LEFT, 5)
        hbox3.Add(self.text, 1)

        vbox.Add((0, 10), 0)
        vbox.Add(hbox2, 0, wx.ALIGN_CENTRE)
        vbox.Add((0, 10), 0)
        vbox.Add(hbox3, 1, wx.ALIGN_CENTRE)
        vbox.Add(hbox1, 1, wx.ALIGN_CENTRE)

        btnSizer = self.CreateButtonSizer( wx.OK )
        vbox.Add(btnSizer, flag=wx.EXPAND|wx.ALL, border=20)

        return vbox

    # End _gaugePanel
    # -----------------------------------------------------------------------


    # -----------------------------------------------------------------------
    # Callbacks
    # -----------------------------------------------------------------------


    def OnPrefs(self,event):
        """ Open the settings frame. """

        dlg = ExportSettings( self, "Fix settings...", self._prefsIO )
        dlg.ShowModal()
        self._prefsIO = dlg.GetPreferences()

    # End OnPrefs
    # -----------------------------------------------------------------------


    def OnOk(self, event):
        """ Start Computation. """

        if not self.pdfwriter:
            self.text.SetLabel('Task in Progress.')
            self.gauge.SetRange( 6 ) # number of files to generate!
            self.gauge.SetValue( 0 )

            self.pdfwriter = pdf_writer(self, self._prefsIO, self.documents, self.authors, self.sessions, self.path)
            self.pdfwriter.start()

    # End OnOk
    # -----------------------------------------------------------------------


    def OnStop(self, event):
        """ Stop Computation. """

        # Flag the worker thread to stop if running
        if self.pdfwriter:
            self.text.SetLabel('Trying to abort computation...')
            self.pdfwriter.abort()

    # End OnStop
    # -----------------------------------------------------------------------


    def OnResult(self, event):
        """ Show current status. """

        if event.tasktext is None:
            # Thread aborted (using our convention of None return)
            self.text.SetLabel('Computation aborted.')
        elif event.tasknum == -1:
            # Process results here
            self.text.SetLabel( event.tasktext )
            self.btn0.Disable()
            self.btn1.Disable()
            self.btn2.Disable()
            self.pdfwriter = None
        else:
            self.gauge.SetValue( event.tasknum )
            self.text.SetLabel( event.tasktext )
            self.Layout()

    # End OnResult
    # -----------------------------------------------------------------------

# ---------------------------------------------------------------------------
