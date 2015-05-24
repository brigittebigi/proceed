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

from wxgui.models.datadocument import Document
from wxgui.models.dataauthor   import Author
from wxgui.models.datasession  import Session

from wxgui.sp_consts import BACKGROUND_COLOR
from wxgui.sp_consts import FONTSIZE
from wxgui.sp_consts import FONTFAMILY

DEFAULT_LABEL = '[session-id]'

# ---------------------------------------------------------------------------


class CreateDocument( wx.Dialog ):
    """
    @authors: Bastien Herbaut, Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: Used to create Document instances.

    """

    def __init__(self, parent, id, title):

        wx.Dialog.__init__(self, parent, id, title, size=(320, 200),style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.parent   = parent
        self.SetBackgroundColour(BACKGROUND_COLOR)

        hSizer = wx.BoxSizer(wx.VERTICAL)
        self.AddStaticText(self,hSizer,"Enter the document ID: ")
        self.TxtCtrl = self.AddTextCtrl(self,hSizer,"")

        btnSizer = self.CreateButtonSizer(wx.CANCEL|wx.OK)
        hSizer.Add(btnSizer, flag=wx.EXPAND|wx.ALL, border=10)

        self.SetSizer(hSizer)
        self.SetMinSize((320, 240))

    # End __init__
    # ------------------------------------------------------------------------


    def GetId(self):
        return self.TxtCtrl.GetValue().strip()

    # ------------------------------------------------------------------------


    def AddStaticText(self, panel, sizer, label, bold=False):
        if bold is True:
            myfont = wx.Font(pointSize=FONTSIZE, family=FONTFAMILY, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_BOLD, encoding=wx.FONTENCODING_UTF8)
        else:
            myfont = wx.Font(pointSize=FONTSIZE, family=FONTFAMILY, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_NORMAL, encoding=wx.FONTENCODING_UTF8)
        txt = wx.StaticText(panel, -1, label)
        txt.SetFont(myfont)
        sizer.Add(txt, proportion=1, flag=wx.EXPAND|wx.ALL, border=10)
        return txt


    def AddTextCtrl(self, panel, sizer, label):
        myfont = wx.Font(pointSize=FONTSIZE, family=FONTFAMILY, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_NORMAL, encoding=wx.FONTENCODING_UTF8)
        txt = wx.TextCtrl(panel, -1, label)
        txt.SetFont(myfont)
        txt.SetEditable(True)
        sizer.Add(txt, proportion=1, flag=wx.EXPAND|wx.ALL, border=10)
        return txt


# ---------------------------------------------------------------------------


class CreateAuthor( wx.Dialog ):
    """
    @authors: Bastien Herbaut, Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: Used to create Author instances.

    The identifier is made of firstname and lastname.

    """

    def __init__(self, parent, id, title):

        wx.Dialog.__init__(self, parent, id, title, size=(320, 260),style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.parent   = parent
        self.SetBackgroundColour(BACKGROUND_COLOR)

        vSizer = wx.BoxSizer(wx.VERTICAL)

        self.AddStaticText(self,vSizer,"First Name: ")
        self.FirstName = self.AddTextCtrl(self,vSizer,"")

        self.AddStaticText(self,vSizer,"Last Name: ")
        self.LastName = self.AddTextCtrl(self,vSizer,"")

        btnSizer = self.CreateButtonSizer(wx.CANCEL|wx.OK)
        vSizer.Add(btnSizer, flag=wx.EXPAND|wx.ALL, border=5)

        self.SetSizer(vSizer)
        self.SetMinSize((320, 240))

    # End __init__
    # ------------------------------------------------------------------------


    def GetFirstName(self):
        return self.FirstName.GetValue().strip()


    def GetLastName(self):
        return self.LastName.GetValue().strip()

    # ------------------------------------------------------------------------


    def AddStaticText(self, panel, sizer, label, bold=False):
        if bold==True:
            myfont = wx.Font(pointSize=FONTSIZE, family=FONTFAMILY, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_BOLD, encoding=wx.FONTENCODING_UTF8)
        else:
            myfont = wx.Font(pointSize=FONTSIZE, family=FONTFAMILY, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_NORMAL, encoding=wx.FONTENCODING_UTF8)
        txt = wx.StaticText(panel, -1, label)
        txt.SetFont(myfont)
        sizer.Add(txt, proportion=1, flag=wx.EXPAND|wx.ALL, border=5)
        return txt


    def AddTextCtrl(self, panel, sizer, label):
        myfont = wx.Font(pointSize=FONTSIZE, family=FONTFAMILY, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_NORMAL, encoding=wx.FONTENCODING_UTF8)
        txt = wx.TextCtrl(panel, -1, label)
        txt.SetFont(myfont)
        txt.SetEditable(True)
        sizer.Add(txt, proportion=1, flag=wx.EXPAND|wx.ALL, border=5)
        return txt

    # ------------------------------------------------------------------------


# ------------------------------------------------------------------------


class CreateSession( wx.Dialog ):
    """
    @authors: Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: Used to create Session instances.

    The Session ID is controlled as follow:
        - starts by '['
        - ends by ']'
        - first letter is uppercase
        - first letter is:
            - K for keynotes
            - O for oral session
            - P for poster session
            - anything else for other types of sessions

    The first letter of the session name is used while sorting by session
    types (in the writers).

    """

    def __init__(self, parent, id, title):

        wx.Dialog.__init__(self, parent, id, title, size=(320, 200),style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.SetBackgroundColour(BACKGROUND_COLOR)

        label = wx.StaticText(self, label="Session ID:", pos=wx.DefaultPosition, size=wx.DefaultSize)
        label.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        label.SetBackgroundColour( BACKGROUND_COLOR )

        self.text = wx.TextCtrl(self, size=(150, -1), validator=SessionValidator())
        self.text.SetForegroundColour(wx.Colour(128,128,128))
        self.text.SetValue(DEFAULT_LABEL)

        self.choices = ['Keynote', 'Oral', 'Poster', 'Other' ]
        self.radiobox = wx.RadioBox(self, label="Session type:", choices=self.choices, majorDimension=2)
        self.radiobox.SetForegroundColour(wx.Colour(3,3,87))

        btnSizer = self.CreateButtonSizer(wx.CANCEL|wx.OK)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(label, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=5)
        sizer.Add(self.text, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, border=5)
        sizer.Add(self.radiobox, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, border=5)
        sizer.Add(btnSizer, flag=wx.EXPAND|wx.ALL, border=10)

        self.SetSizer(sizer)
        self.SetMinSize((320, 240))

    # End __init__
    # ------------------------------------------------------------------------

    def OnTextClick(self, event):
        self.text.SetForegroundColour(wx.BLACK)
        if self.text.GetValue() == DEFAULT_LABEL:
            self.OnTextErase(event)

    def OnTextChanged(self, event):
        self.text.SetFocus()
        self.text.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
        self.text.Refresh()

    def OnTextErase(self, event):
        self.text.SetValue('')
        self.text.SetFocus()
        self.text.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
        self.text.Refresh()

    # ------------------------------------------------------------------------

    def GetId(self):
        text = self.text.GetValue().strip()
        idx  = self.radiobox.GetSelection()

        if self.choices[idx] == 'Other':
            # TODO: check if session ID does not start by 'O', 'P' or 'K'
            return text

        elif self.choices[idx] == 'Keynote':
            if text[1] == 'K':
                return text
            else:
                return '[K-' + text[1:]

        elif self.choices[idx] == 'Oral':
            if text[1] == 'O':
                return text
            else:
                return '[O-' + text[1:]

        elif self.choices[idx] == 'Poster':
            if text[1] == 'P':
                return text
            else:
                return '[P-' + text[1:]

    # ------------------------------------------------------------------------

# ---------------------------------------------------------------------------


class SessionValidator( wx.PyValidator ):
    """ Check if TextCtrl can be a sesion ID. """

    def __init__(self):
        wx.PyValidator.__init__(self)

    def Clone(self): # Required method for validator
        return SessionValidator()

    def TransferToWindow(self):
        return True # Prevent wxDialog from complaining.

    def TransferFromWindow(self):
        return True # Prevent wxDialog from complaining.

    def Validate(self, win):
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue()

        if len(text.strip()) == 0:
            textCtrl.SetBackgroundColour("pink")
            textCtrl.SetFocus()
            textCtrl.Refresh()
            return False
        else:
            if not text.startswith('['):
                text = '[' + text
            if not text.endswith(']'):
                text = text + ']'
            textCtrl.SetValue(text)

            textCtrl.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
            textCtrl.Refresh()
            return True

# ---------------------------------------------------------------------------
