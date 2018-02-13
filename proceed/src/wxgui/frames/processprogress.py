#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# ---------------------------------------------------------------------------
#            ___   __    __    __    ___
#           /     |  \  |  \  |  \  /        Automatic
#           \__   |__/  |__/  |___| \__      Annotation
#              \  |     |     |   |    \     of
#           ___/  |     |     |   | ___/     Speech
#           =============================
#
#           http://sldr.org/sldr000800/preview/
#
# ---------------------------------------------------------------------------
# developed at:
#
#       Laboratoire Parole et Langage
#
#       Copyright (C) 2011-2015  Brigitte Bigi
#
#       Use of this software is governed by the GPL, v3
#       This banner notice must not be removed
# ---------------------------------------------------------------------------
#
# SPPAS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SPPAS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SPPAS. If not, see <http://www.gnu.org/licenses/>.
#
# ---------------------------------------------------------------------------
# File: processprogress.py
# ----------------------------------------------------------------------------

__docformat__ = """epytext"""
__authors__   = """Brigitte Bigi"""
__copyright__ = """Copyright (C) 2011-2015  Brigitte Bigi"""

# ----------------------------------------------------------------------------

import wx

from wxgui.sp_icons import APP_ICON
from wxgui.sp_icons import PROCESS_ICON

from wxgui.cutils.imageutils import spBitmap
from wxgui.sp_consts import FRAME_STYLE
from wxgui.sp_consts import FRAME_TITLE
from wxgui.sp_consts import HEADER_FONTSIZE

# ----------------------------------------------------------------------------

class ProcessProgressDialog( wx.MiniFrame ):
    """
    @author:  Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL, v3
    @summary: Frame indicating a progress, with 2 text fields.

    """

    def __init__(self, parent):
        """
        Constructor.
        """

        wx.MiniFrame.__init__(self, parent, title=FRAME_TITLE+" - Progress", size=(420, 220))
        self._create_gui()

    # ------------------------------------------------------------------------
    # Create the GUI
    # ------------------------------------------------------------------------

    def _create_gui(self):
        self._init_infos()
        self._create_title_label()
        self._create_content()
        self._layout_components()

    def _init_infos( self ):
        wx.GetApp().SetAppName( "progress" )
        # icon
        _icon = wx.EmptyIcon()
        _icon.CopyFromBitmap( spBitmap(APP_ICON) )
        self.SetIcon(_icon)

    def _create_title_label(self):
        self.title_layout = wx.BoxSizer(wx.HORIZONTAL)
        bmp = wx.BitmapButton(self, bitmap=spBitmap(PROCESS_ICON, 32), style=wx.NO_BORDER)
        font = wx.Font(HEADER_FONTSIZE, wx.MODERN, wx.NORMAL, wx.BOLD, False, u'Consolas')
        self.title_label = wx.StaticText(self, label="Processing...", style=wx.ALIGN_CENTER)
        self.title_label.SetFont( font )
        self.title_layout.Add(bmp, 0, flag=wx.TOP|wx.RIGHT|wx.ALIGN_RIGHT, border=5)
        self.title_layout.Add(self.title_label, 1, flag=wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=5)


    def _create_content(self):
        # an header text used to print the annotation step
        self.header      = wx.StaticText(self, id=-1, label="", style = wx.ALIGN_CENTRE)
        # the gauge
        self.gauProgress = wx.Gauge(self, range=100, size=(400, 24))
        # a bottom text used to print the current file name
        self.text        = wx.StaticText(self, id=-1, label="", style = wx.ALIGN_CENTRE)


    def _layout_components(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.title_layout, 0, flag=wx.ALL|wx.EXPAND, border=4)
        vbox.Add( self.header,      proportion=0, flag=wx.ALL|wx.EXPAND, border=4)
        vbox.Add( self.gauProgress, proportion=1, flag=wx.ALL|wx.EXPAND, border=4)
        vbox.Add( self.text,        proportion=1, flag=wx.ALL|wx.EXPAND, border=4)
        self.SetSizer( vbox )
        self.SetMinSize((420,200))
        self.Layout()
        self.Raise()
        self.SetFocus()
        self.Center()
        self.Refresh()

    # ------------------------------------------------------------------------

    def set_title(self, title):
        """
        Fix the title label.
        """
        self.title_label.SetLabel(title)
        self.title_label.Refresh()

    # ------------------------------------------------------------------------

    def set_new(self, label="", text="", fraction=0.):
        """
        Initialize a new progress box.

        @param label:    progress box label (default: None)
        @param text:     progress bar text  (default: None)
        @param fraction: progress bar value (default: 0)

        """
        self.set_header(label)
        self.set_text(text)
        self.set_fraction(fraction)
        self.Refresh()
        self.Update()

    def set_fraction(self,fraction):
        """
        Set a new progress value to the progress bar.

        @param fraction: new progress value

        """
        # convert fraction to a percentage (if necessary)
        if fraction < 1:
            fraction = int(fraction*100)
        self.gauProgress.SetValue(fraction)
        self.Refresh()
        self.Update()

    def set_text(self,text):
        """
        Set a new progress text to the progress bar.

        @param text: new progress text

        """
        self.text.SetLabel( text )
        self.Refresh()
        self.Update()

    def set_header(self,label):
        """
        Set a new progress label to the progress box.

        @param label: new progress label

        """
        self.header.SetLabel( label )
        self.Refresh()
        self.Update()

    def update(self,fraction,text):
        """
        Update the progress box.

        @param text:     progress bar text  (default: None)
        @param fraction: progress bar value (default: 0)

        """
        self.set_text(text)
        self.set_fraction(fraction)
        self.Refresh()
        self.Update()

    def close(self):
        """
        Close the progress box.
        """
        self.Destroy()

# ----------------------------------------------------------------------------
