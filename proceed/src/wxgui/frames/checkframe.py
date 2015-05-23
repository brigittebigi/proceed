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
import wx.stc
import os.path

from wxgui.models.datadocument import Document
from wxgui.models.dataauthor   import Author
from wxgui.models.datasession  import Session
from wxgui.models.validate     import Validate
import wxgui.consts as consts

# ---------------------------------------------------------------------------


class CheckFrame( wx.Dialog ):
    """
    @authors: Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: Used to show a disgnosis about the data.

    """

    def __init__(self, parent, id, title, documents, authors, sessions, path=None):
        """
        Create a new CheckFrame instance.
        """
        wx.Dialog.__init__(self, parent, id, title, size=(600, 500),style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        self.SetIcon(wx.Icon(consts.APP_CHECK_ICON, wx.BITMAP_TYPE_ANY))

        self.parent = parent
        self.SetMinSize((520, 380))

        self.SetBackgroundColour(consts.BACKGROUND_COLOR)
        self.MainSizer = wx.BoxSizer(wx.VERTICAL)

        self.txtCtrl = wx.stc.StyledTextCtrl(self, -1)
        myfont = wx.Font(pointSize=consts.FONTSIZE, family=consts.FONTFAMILY, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_NORMAL, encoding=wx.FONTENCODING_UTF8)
        self.txtCtrl.SetFont(myfont)

        self.check( Validate( documents, authors, sessions ), path )

        self.MainSizer.Add(self.txtCtrl,proportion=1,flag=wx.EXPAND|wx.BOTTOM, border=5)

        btnSizer = self.CreateButtonSizer(wx.OK)
        self.MainSizer.Add(btnSizer, flag=wx.EXPAND|wx.ALL, border=20)

        self.SetSizer(self.MainSizer)

    # End __init__
    # ------------------------------------------------------------------------


    def separator(self):
        return u"--------------------------------------------------------------\n"


    def new_main_title(self, maintitle):
        __s =  u"==============================================================\n"
        __s = __s + maintitle + u"\n"
        __s = __s + u"==============================================================\n\n"
        return __s


    def new_check_title(self, checktitle):
        __s = self.separator()
        __s = __s + checktitle + u"\n"
        __s = __s + self.separator()
        return __s


    def new_check_result(self, errors):
        __s = u" Perfect. Nothing is missing.\n"
        if len(errors) > 0:
            __s = u" List of missing entries: \n"
            for e in errors:
                __s = __s + "     - " + e.encode('utf8') + u"\n"
        return __s


    def check(self, validator, path):

        self.txtCtrl.AppendText(self.new_main_title(u" Check all fields used by the Header-Footer PDF generator:"))

        if path is not None:
            self.txtCtrl.AppendText(self.new_check_title(u" Check if each docid corresponds to a PDF file:"))
            self.txtCtrl.AppendText(self.new_check_result( sorted(validator.pdffiles(path)) ))
            self.txtCtrl.AppendText(u"\n")

        self.txtCtrl.AppendText(self.new_check_title(u" Check if each document is related to a session:"))
        self.txtCtrl.AppendText(self.new_check_result( sorted(validator.session_in_documents()) ))
        self.txtCtrl.AppendText(u"\n")

        self.txtCtrl.AppendText(self.new_check_title(u" Check if each document with a session has a rank:"))
        self.txtCtrl.AppendText(self.new_check_result( sorted(validator.rank_in_documents()) ))
        self.txtCtrl.AppendText(u"\n")

        self.txtCtrl.AppendText(self.new_check_title(u" Check if each session has a name (only for sessions related to at least one document):"))
        self.txtCtrl.AppendText(self.new_check_result( sorted(validator.name_in_sessions()) ))
        self.txtCtrl.AppendText(u"\n")

        self.txtCtrl.AppendText(self.new_check_title(u" Check if each session has a date (only for sessions related to at least one document):"))
        self.txtCtrl.AppendText(self.new_check_result( sorted(validator.date_in_sessions()) ))
        self.txtCtrl.AppendText(u"\n")

        self.txtCtrl.AppendText(self.new_check_title(u" Check if each session has a rank (only for sessions related to at least one document):"))
        self.txtCtrl.AppendText(self.new_check_result( sorted(validator.rank_in_sessions()) ))
        self.txtCtrl.AppendText(u"\n")

    # ------------------------------------------------------------------------

