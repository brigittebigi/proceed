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

import Manager.consts as consts

from Manager.frames.export_settings import ExportSettings
from Manager.models.prefs   import Preferences_IO
from Manager.models.writers import pdf_writer
from Manager.models.writers import EVT_RESULT

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
        _icon.CopyFromBitmap( wx.Bitmap(consts.APP_EXPORT_PDF_ICON, wx.BITMAP_TYPE_ANY) )
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
        # No specific settings for now (exept options in themes).
        pass

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
