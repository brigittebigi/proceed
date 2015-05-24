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
# ----------------------------------------------------------------------------
# File: feedback.py
# ----------------------------------------------------------------------------

__docformat__ = """epytext"""
__authors__   = """Brigitte Bigi"""
__copyright__ = """Copyright (C) 2011-2015  Brigitte Bigi"""


# -------------------------------------------------------------------------
# Imports
# -------------------------------------------------------------------------

import wx
import urllib
import webbrowser
import logging

from sp_glob import program
from wxgui.sp_icons import APP_ICON
from wxgui.sp_icons import FEEDBACK_ICON
from wxgui.sp_icons import MAIL_DEFAULT_ICON
from wxgui.sp_icons import MAIL_GMAIL_ICON
from wxgui.sp_icons import MAIL_OTHER_ICON
from wxgui.sp_icons import CANCEL_ICON
from wxgui.cutils.imageutils import spBitmap

from wxgui.cutils.ctrlutils import CreateGenButton

from wxgui.sp_consts import FRAME_STYLE
from wxgui.sp_consts import FRAME_TITLE
from wxgui.sp_consts import HEADER_FONTSIZE


# -------------------------------------------------------------------------
# Constants
# -------------------------------------------------------------------------

DESCRIBE_TEXT = "Describe what you did here..."

ID_DEFAULT = wx.NewId()
ID_GMAIL   = wx.NewId()
ID_OTHER   = wx.NewId()


# -------------------------------------------------------------------------

class FeedbackForm(object):
    """
    @author:  Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: This class is used to send feedback to the author.

    """

    def __init__(self, dialog, webbrowser):
        self.dialog = dialog
        self.webbrowser = webbrowser


    def Populate(self, subject=None, body=None):
        self.dialog.SetToText("brigitte.bigi@gmail.com")
        if subject: self.dialog.SetSubjectText(subject)
        if body: self.dialog.SetBodyText(body)
        if body and body.startswith(DESCRIBE_TEXT):
            self.dialog.SetBodySelection(0, len(DESCRIBE_TEXT))

    def SendWithDefault(self):
        text = self.dialog.GetBodyText()
        text = text.strip()
        self.webbrowser.open("mailto:%s?subject=%s&body=%s" % (
            urllib.quote(self.dialog.GetToText()),
            urllib.quote(self.dialog.GetSubjectText()),
            urllib.quote(text.encode('utf-8'))))

    def SendWithGmail(self):
        self.webbrowser.open("https://mail.google.com/mail/?compose=1&view=cm&fs=1&to=%s&su=%s&body=%s" % (
            urllib.quote(self.dialog.GetToText()),
            urllib.quote(self.dialog.GetSubjectText()),
            urllib.quote(self.dialog.GetBodyText())))

# ----------------------------------------------------------------------------


class FeedbackDialog( wx.Dialog ):
    """
    @author:  Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: This class is used to send feedback to the author.

    """

    def __init__(self, parent=None):
        wx.Dialog.__init__(self, parent, title=FRAME_TITLE+" - Feedback", style=FRAME_STYLE)

        self.controller = FeedbackForm(self, webbrowser)
        self._create_gui()

    # End __init__
    # ------------------------------------------------------------------------


    # ------------------------------------------------------------------------
    # Create the GUI
    # ------------------------------------------------------------------------

    def _create_gui(self):
        self._init_infos()
        self._create_title_label()
        self._create_to_text_field()
        self._create_subject_text_field()
        self._create_body_text_field()
        self._create_send_default_button()
        self._create_send_gmail_button()
        self._create_send_other_button()
        self._create_close_button()
        self._layout_components()
        self._set_focus_component()


    def _init_infos( self ):
        wx.GetApp().SetAppName( "feedback" )
        # icon
        _icon = wx.EmptyIcon()
        _icon.CopyFromBitmap( spBitmap(APP_ICON) )
        self.SetIcon(_icon)

    def _create_title_label(self):
        self.title_layout = wx.BoxSizer(wx.HORIZONTAL)
        bmp = wx.BitmapButton(self,bitmap=spBitmap(FEEDBACK_ICON, 32), style=wx.NO_BORDER)
        font = wx.Font(HEADER_FONTSIZE, wx.MODERN, wx.NORMAL, wx.BOLD, False, u'Consolas')
        self.title_label = wx.StaticText(self, label="Email Feedback", style=wx.ALIGN_CENTER)
        self.title_label.SetFont( font )
        self.title_layout.Add(bmp, flag=wx.TOP|wx.RIGHT|wx.ALIGN_RIGHT, border=5)
        self.title_layout.Add(self.title_label, flag=wx.EXPAND|wx.ALL, border=5)

    def _create_to_text_field(self):
        self.to_text = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_READONLY)

    def _create_subject_text_field(self):
        self.subject_text = wx.TextCtrl(self, wx.ID_ANY)
        self.subject_text.SetValue(program + " feedback")

    def _create_body_text_field(self):
        self.body_text = wx.TextCtrl(self, size=(-1, 200), style=wx.TE_MULTILINE)
        self.body_text.SetForegroundColour(wx.Colour(128,128,128))
        self.body_text.SetBackgroundColour( wx.WHITE )
        self.body_text.SetValue(DESCRIBE_TEXT)
        self.body_text.Bind(wx.EVT_CHAR, self._on_char)

    def _on_char(self, evt):
        self.body_text.SetForegroundColour(wx.BLACK)
        if self.body_text.GetValue() == DESCRIBE_TEXT:
            self.body_text.SetValue('')
            self.body_text.SetFocus()
            self.body_text.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
            self.body_text.Refresh()
        if self._ctrl_a(evt):
            self.body_text.SelectAll()
        else:
            evt.Skip()

    def _ctrl_a(self, evt):
        KEY_CODE_A = 1
        return evt.ControlDown() and evt.KeyCode == KEY_CODE_A

    def _create_send_default_button(self):
        def on_click(event):
            self.controller.SendWithDefault()
        bmp = spBitmap(MAIL_DEFAULT_ICON)
        self.btn_default_client = CreateGenButton(self, ID_DEFAULT, bmp, text=" Default", tooltip="Send with your default email client.", colour=None)#wx.Colour(220,120,180))
        self.Bind(wx.EVT_BUTTON, on_click, self.btn_default_client, ID_DEFAULT)

    def _create_send_gmail_button(self):
        def on_click(event):
            self.controller.SendWithGmail()
        bmp = spBitmap(MAIL_GMAIL_ICON)
        self.btn_gmail = CreateGenButton(self, ID_GMAIL, bmp, text=" Gmail", tooltip="Send with Gmail.", colour=None)#wx.Colour(220,120,180))
        self.Bind(wx.EVT_BUTTON, on_click, self.btn_gmail, ID_GMAIL)

    def _create_send_other_button(self):
        def on_click(evt):
            wx.MessageBox("Copy and paste this email into your favorite email client and send it from there.",
                "Other email client", wx.OK | wx.ICON_INFORMATION)
        bmp = spBitmap(MAIL_OTHER_ICON)
        self.btn_other = CreateGenButton(self,ID_OTHER, bmp, text=" Other", tooltip="Send with another email client.", colour=None)#wx.Colour(220,120,180))
        self.Bind(wx.EVT_BUTTON, on_click, self.btn_other, ID_OTHER)

    def _create_close_button(self):
        bmp = spBitmap(CANCEL_ICON)
        self.btn_close = CreateGenButton(self, wx.ID_CLOSE, bmp, text=" Close", tooltip="Close this frame", colour=None)
        self.btn_close.SetDefault()
        self.btn_close.SetFocus()
        self.SetAffirmativeId(wx.ID_CLOSE)

    def _layout_components(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.title_layout, flag=wx.ALL|wx.EXPAND, border=5)
        vbox.Add(self._create_layout_grid(), flag=wx.ALL|wx.EXPAND, border=5)
        self.SetSizerAndFit(vbox)

    def _create_layout_grid(self):
        grid = wx.FlexGridSizer(4, 2, 5, 5)
        grid.AddGrowableCol(1)
        grid.Add(wx.StaticText(self, label="To: "), flag=wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self.to_text, flag=wx.EXPAND)
        grid.Add(wx.StaticText(self, label="Subject: "), flag=wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self.subject_text, flag=wx.EXPAND)
        grid.Add(wx.StaticText(self, label="Body: "), flag=0)
        grid.Add(self.body_text, flag=wx.EXPAND)
        grid.Add(wx.StaticText(self, label="Send with: "), flag=wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._create_button_box(), flag=wx.EXPAND)
        return grid

    def _create_button_box(self):
        button_box = wx.BoxSizer(wx.HORIZONTAL)
        button_box.Add(self.btn_default_client, flag=wx.RIGHT, border=5)
        button_box.Add(self.btn_gmail, flag=wx.RIGHT, border=5)
        button_box.Add(self.btn_other, flag=wx.RIGHT, border=5)
        button_box.AddStretchSpacer()
        button_box.Add(self.btn_close, flag=wx.LEFT, border=5)
        return button_box

    def _set_focus_component(self):
        self.body_text.SetFocus()


    # ------------------------------------------------------------------------
    # Available methods
    # ------------------------------------------------------------------------

    def GetToText(self):
        return self.to_text.GetValue()

    def GetSubjectText(self):
        return self.subject_text.GetValue()

    def GetBodyText(self):
        return self.body_text.GetValue()

    def SetToText(self, text):
        self.to_text.SetValue(text)

    def SetSubjectText(self, text):
        if text: self.subject_text.SetValue(text)

    def SetBodyText(self, text):
        if text: self.body_text.SetValue(text)

    def SetBodySelection(self, start, end):
        self.body_text.SetSelection(start, end)


# ----------------------------------------------------------------------------


def ShowFeedbackDialog(parent):
    logging.debug('Show feedback dialog...')
    dialog = FeedbackDialog(parent)
    dialog.controller.Populate(None, None)
    dialog.ShowModal()
    dialog.Destroy()

# ---------------------------------------------------------------------------
