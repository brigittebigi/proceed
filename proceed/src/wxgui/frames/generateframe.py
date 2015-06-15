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
import logging
import wx

from sp_glob import SETTINGS_FILE
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

    def __init__(self, parent, idd, title, conference, documents, authors, sessions, path):
        """
        Constructor.
        """
        wx.Dialog.__init__(self, parent, idd, title, size=(380, 200),style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        _icon = wx.EmptyIcon()
        _icon.CopyFromBitmap( wx.Bitmap(APP_EXPORT_PDF_ICON, wx.BITMAP_TYPE_ANY) )
        self.SetIcon(_icon)

        self.SetMinSize((380, 200))

        sizer = self._create_content(self)

        # Members
        self.conference = conference
        self.documents = documents
        self.authors   = authors
        self.sessions  = sessions
        self.path      = path
        self._prefsIO  = Preferences_IO(SETTINGS_FILE)

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
        """
        Fix default preferences.
        """
        # Page
        self._prefsIO.SetValue('PAGE_FORMAT','str', 'a4paper', "Paper format")
        self._prefsIO.SetValue('PAGE_NUMBER','int', 1, "First page number")
        self._prefsIO.SetValue("TOP_MARGIN",'int', 30, "Top margin (mm)")       # millimeters
        self._prefsIO.SetValue("BOTTOM_MARGIN",'int', 20, 'Bottom margin (mm)') # millimeters
        self._prefsIO.SetValue("HEADER_SIZE",'int', 20, 'Header size (pt)')     # pt
        self._prefsIO.SetValue("FOOTER_SIZE",'int', 10,'Footer size (pt)')      # pt

        # Header
        self._prefsIO.SetValue('HEADER_LEFT','str', '', 'Content of the header, at left')
        self._prefsIO.SetValue('HEADER_CENTER','str', '', 'Content of the header, at center')
        self._prefsIO.SetValue('HEADER_RIGHT','str', '\\session', 'Content of the header, at right')
        self._prefsIO.SetValue('HEADER_STYLE','str', '\\it', "Header font style") # "\\rm","\\it","\\em","\\emph","\\bf","\\sl","\\sf","\\sc","\\tt"
        self._prefsIO.SetValue('HEADER_COLOR','str', '20,20,20', "Header RGB color")
        self._prefsIO.SetValue('HEADER_RULER','bool', True, "Separate the header with a ruler")

        # Footer
        self._prefsIO.SetValue('FOOTER_LEFT','str', '', 'Content of the footer, at left')
        self._prefsIO.SetValue('FOOTER_CENTER','str', '\\thepage', 'Content of the footer, at center')
        self._prefsIO.SetValue('FOOTER_RIGHT','str', '', 'Content of the footer, at right')
        self._prefsIO.SetValue('FOOTER_STYLE','str', '\\bf', "Footer font style") # "\\rm","\\it","\\em","\\emph","\\bf","\\sl","\\sf","\\sc","\\tt"
        self._prefsIO.SetValue('FOOTER_COLOR','str', '20,20,20', "Footer color")
        self._prefsIO.SetValue('FOOTER_RULER','bool', False, "Separate the footer with a ruler")

        # Generate
        self._prefsIO.SetValue('GENERATE_PROGRAM','bool', True, "Generate the Program")
        self._prefsIO.SetValue('GENERATE_PROGRAM_OVERVIEW','bool', True, "Generate the Program overview")
        self._prefsIO.SetValue('GENERATE_TABLEOFCONTENTS','bool', True, "Generate the Table of content")
        self._prefsIO.SetValue('GENERATE_MERGED_SUBMISSIONS','bool', True, "Generate the Merged submissions")
        self._prefsIO.SetValue('GENERATE_AUTHORS_INDEX','bool', True, "Generate the Index of Authors")
        self._prefsIO.SetValue('GENERATE_AUTHORS_LIST','bool', True, "Generate the List of authors")

        # Titles
        self._prefsIO.SetValue('TITLE_PROGRAM','str', 'Program', 'Program')
        self._prefsIO.SetValue('TITLE_PROGRAM_OVERVIEW','str', 'Program overview', 'Program overview')
        self._prefsIO.SetValue('TITLE_TABLEOFCONTENTS','str', 'Table of contents', 'Table of contents')
        self._prefsIO.SetValue('TITLE_AUTHORS_INDEX','str', 'Author Index', 'Author Index')
        self._prefsIO.SetValue('TITLE_AUTHORS_LIST','str', 'List of authors', 'List of authors')

        # Sort by session types first (1. keynotes, then 2. orals then 3. posters)
        self._prefsIO.SetValue('SORT_BY_SESSION_TYPE_FIRST','bool', False)

        self._prefsIO.SetValue('COLOUR_1','str', "139,53,49", "Color for session codes")
        self._prefsIO.SetValue('COLOUR_2','str', "120,80,60", "Color for dates")
        self._prefsIO.SetValue('COLOUR_3','str', "190,70,30", "Color for session names")

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
            self.gauge.SetRange( 100 ) # percentage
            self.gauge.SetValue( 0 )

            self.pdfwriter = pdf_writer(self, self._prefsIO, self.conference, self.documents, self.authors, self.sessions, self.path)
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

        if event.taskpercent is not None:
            logging.debug(' set gauge to %d'%int(event.taskpercent))
            self.gauge.SetValue( int(event.taskpercent) )

        elif event.tasktext is None:
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
            self.gauge.SetValue( 0 )
            self.text.SetLabel( event.tasktext )
            self.Layout()

    # End OnResult
    # -----------------------------------------------------------------------

# ---------------------------------------------------------------------------
