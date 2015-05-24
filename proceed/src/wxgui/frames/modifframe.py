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
import wx.grid
import wx.calendar

import os.path
import logging
import datetime

from wxgui.models.datadocument import Document
from wxgui.models.dataauthor   import Author
from wxgui.models.datasession  import Session
import wxgui.models.datasession

from wxgui.sp_consts import BACKGROUND_COLOR
from wxgui.sp_consts import FONTFAMILY
from wxgui.sp_consts import FONTSIZE
from sp_glob import ICONS_PATH
from wxgui.sp_icons  import DOCUMENT_ICON
from wxgui.sp_icons  import AUTHOR_ICON
from wxgui.sp_icons  import SESSION_ICON

# ---------------------------------------------------------------------------


class ModifFrame( wx.Dialog ):
    """
    @authors: Bastien Herbaut, Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: Used to modify Document, Author or Session instances.

    """

    def __init__(self, parent, id, title, pagename, eltid):
        """
        Create a new ModifFrame instance.
        Used to modify Document, Author or Session instances.
        """
        logging.debug('Mofification in '+pagename)
        wx.Dialog.__init__(self, parent, id, title, size=(640, 520),style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        self.parent   = parent
        self.pagename = pagename
        self.eltid    = eltid
        self.SetMinSize((520, 420))

        self.initialize()

    # End __init__
    # ------------------------------------------------------------------------


    def initialize(self):

        self.SetBackgroundColour(BACKGROUND_COLOR)
        self.MainSizer = wx.BoxSizer(wx.VERTICAL)

        for children in self.GetChildren():
            children.Destroy()

        self.createContent()

        btnSizer = self.CreateButtonSizer(wx.OK)
        self.MainSizer.Add(btnSizer, flag=wx.EXPAND|wx.ALL, border=10)

        self.SetSizer(self.MainSizer)

    # End initialize
    # ------------------------------------------------------------------------


    def GetParent(self):
        return self.parent

    # End GetParent
    # ------------------------------------------------------------------------


    # ------------------------------------------------------------------------
    # Create the content of a ModifFrame
    # ------------------------------------------------------------------------


    def AddStaticText(self, panel, sizer, label, bold=False):
        if bold is True:
            myfont = wx.Font(pointSize=FONTSIZE, family=FONTFAMILY, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_BOLD, encoding=wx.FONTENCODING_UTF8)
        else:
            myfont = wx.Font(pointSize=FONTSIZE, family=FONTFAMILY, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_NORMAL, encoding=wx.FONTENCODING_UTF8)
        txt = wx.StaticText(panel, -1, label)
        txt.SetFont(myfont)
        sizer.Add(txt)
        return txt


    def AddLongTextCtrl(self, panel, sizer, label):
        myfont = wx.Font(pointSize=FONTSIZE, family=FONTFAMILY, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_NORMAL, encoding=wx.FONTENCODING_UTF8)
        txt = wx.TextCtrl(panel, -1, "", size=wx.Size(600,60), style=wx.TE_LEFT|wx.TE_MULTILINE)
        txt.SetFont(myfont)
        txt.WriteText( label )
        sizer.Add(txt,proportion=1)
        return txt


    def AddTextCtrl(self, panel, sizer, label):
        myfont = wx.Font(pointSize=FONTSIZE, family=FONTFAMILY, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_NORMAL, encoding=wx.FONTENCODING_UTF8)
        txt = wx.TextCtrl(panel, -1, "", size=wx.Size(600,30), style=wx.TE_LEFT)
        txt.SetFont(myfont)
        txt.WriteText( label )
        #txt.SetInsertionPoint(0)
        #txt.ShowPosition(0)

        sizer.Add(txt,proportion=1)
        return txt


    def AddTitle(self, icon, title):
        titlesizer = wx.BoxSizer(wx.HORIZONTAL)

        iconbmp = wx.StaticBitmap(self, bitmap=wx.Bitmap(os.path.join(ICONS_PATH,icon)))
        text1 = wx.StaticText(self, label=title)
        text1.SetFont(wx.Font(FONTSIZE+4, wx.SWISS, wx.NORMAL, wx.BOLD))
        line1 = wx.StaticLine(self)

        titlesizer.Add(iconbmp, flag=wx.TOP|wx.RIGHT|wx.ALIGN_RIGHT, border=5)
        titlesizer.Add(text1, flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        self.MainSizer.Add(titlesizer, 0, flag=wx.EXPAND, border=5)
        self.MainSizer.Add(line1, flag=wx.EXPAND|wx.BOTTOM, border=5)

    # ------------------------------------------------------------------------


    def createContent(self):

        if self.pagename == "Documents":
            self.createContentFor_Doc()

        elif self.pagename == "Authors":
            self.createContentFor_Auth()

        elif self.pagename == "Sessions":
            self.createContentFor_Session()

        else:
            raise Exception('Un-appropriate selection to modify\n')

    # End createContent
    # ------------------------------------------------------------------------


    def createContentFor_Doc(self):

        if self.eltid is None: return

        self.DocObj = self.parent._dataPages['Documents'][self.eltid]

        ############### DOCID ###############
        self.AddTitle(DOCUMENT_ICON, self.DocObj.get_docid())

        ############### TITLE ###############
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.AddStaticText(self,hSizer,"Title: \t\t")
        TitleTxtCtrl = self.AddLongTextCtrl(self,hSizer,self.DocObj.get_title())
        self.Bind(wx.EVT_TEXT, lambda event: self.OnChangeDoc(event, TitleTxtCtrl, "title"), TitleTxtCtrl)
        self.MainSizer.Add(hSizer, flag=wx.EXPAND|wx.ALL, proportion=1, border=10)

        ############### AUTHORS  ###############
        hSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.AddStaticText(self,hSizer,"Authors: \t\t")

        self.authorsGrid = wx.grid.Grid(self)

        self.authorsGrid.SetMargins(0,0)
        self.authorsGrid.CreateGrid(len(self.DocObj.get_authors()),2)
        self.authorsGrid.SetDefaultColSize(160)

        self.authorsGrid.DisableDragRowSize()
        self.authorsGrid.DisableDragColSize()
        self.authorsGrid.DisableDragGridSize()
        self.authorsGrid.SetDefaultCellAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)
        self.authorsGrid.SetDefaultCellBackgroundColour(BACKGROUND_COLOR)
        self.authorsGrid.SetLabelBackgroundColour(BACKGROUND_COLOR)

        self.authorsGrid.SetColLabelValue(0,"Last Name")
        self.authorsGrid.SetColLabelValue(1,"First Name")

        self.Bind(wx.grid.EVT_GRID_EDITOR_SHOWN, self.OnEditorShown , self.authorsGrid )
        self.Bind(wx.grid.EVT_GRID_CELL_CHANGE, self.OnEditorClosed , self.authorsGrid )

        self.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.OnRemove , self.authorsGrid )

        i = 0
        for author in self.DocObj.get_authors():
            self.authorsGrid.SetCellValue(i, 0, author.get_lastname())
            self.authorsGrid.SetCellValue(i, 1, author.get_firstname())
            self.authorsGrid.SetRowLabelValue(i, " Remove ")
            i += 1

        hSizer.Add(self.authorsGrid, flag=wx.EXPAND|wx.ALL)
        AddButton = wx.Button(self, -1, "Add an author")
        self.Bind(wx.EVT_BUTTON, self.OnAddAuthor, AddButton)
        hSizer.Add(AddButton, flag=wx.ALL)
        self.MainSizer.Add(hSizer, flag=wx.EXPAND|wx.ALL, proportion=2, border=10)

        ############### SESSION  ###############
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.AddStaticText(self,hSizer,"Session: \t\t")

        SessionsList = self.parent._dataPages['Sessions'].values()
        choices = list()
        for session in SessionsList:
            choices.append(session.get_sessionid())
        choices = sorted(choices)
        session = self.DocObj.get_session()
        if session != "":
            session = session.get_sessionid()
        choices.append('')

        SessionCtrl = wx.Choice(self, -1, choices=choices)
        SessionCtrl.SetStringSelection(session)
        SessionCtrl.Bind(wx.EVT_CHOICE,  lambda event: self.OnChangeDoc(event, SessionCtrl, "session"), SessionCtrl)
        hSizer.Add(SessionCtrl, proportion=1)

        self.MainSizer.Add(hSizer, flag=wx.ALL, proportion=1, border=10)

        ############### RANK  ###############
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.AddStaticText(self,hSizer,"Rank: \t\t")

        SpinCtrlRank = wx.SpinCtrl(self, -1)
        SpinCtrlRank.SetRange(0, 100)
        SpinCtrlRank.SetValue(self.DocObj.get_rank())

        SpinCtrlRank.Bind(wx.EVT_SPINCTRL,  lambda event: self.OnChangeDoc(event, SpinCtrlRank, "rank"), SpinCtrlRank)
        hSizer.Add(SpinCtrlRank)

        self.MainSizer.Add(hSizer, flag=wx.EXPAND|wx.ALL, proportion=1, border=10)

    # ------------------------------------------------------------------------


    def createContentFor_Auth(self):

        if self.eltid is None: return

        self.AuthObj = self.parent._dataPages['Authors'][self.eltid]

        ############### AUTHOR ID ###############
        self.AddTitle(AUTHOR_ICON, self.AuthObj.get_authorid())

        ############### LASTNAME ###############
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.AddStaticText(self,hSizer,"Last name: \t")
        LastnameCtrl = self.AddTextCtrl(self,hSizer,self.AuthObj.get_lastname())
        LastnameCtrl.Bind(wx.EVT_TEXT, lambda event: self.OnChangeAuth(event, LastnameCtrl, "lastname"), LastnameCtrl)
        self.MainSizer.Add(hSizer, flag=wx.EXPAND|wx.ALL, proportion=1, border=10)

        ############### FIRSTNAME ###############
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.AddStaticText(self,hSizer,"First name: \t")
        FirstnameCtrl = self.AddTextCtrl(self,hSizer,self.AuthObj.get_firstname())
        FirstnameCtrl.Bind(wx.EVT_TEXT, lambda event: self.OnChangeAuth(event, FirstnameCtrl, "firstname"), FirstnameCtrl)
        self.MainSizer.Add(hSizer, flag=wx.EXPAND|wx.ALL, proportion=1, border=10)

        ############### EMAIL ###############
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.AddStaticText(self,hSizer,"Email: \t\t")
        EmailCtrl = self.AddTextCtrl(self,hSizer,self.AuthObj.get_email())
        EmailCtrl.Bind(wx.EVT_TEXT, lambda event: self.OnChangeAuth(event, EmailCtrl, "email"), EmailCtrl)
        self.MainSizer.Add(hSizer, flag=wx.EXPAND|wx.ALL, proportion=1, border=10)

        ############### AFFILIATION ###############
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.AddStaticText(self,hSizer,"Affiliation: \t")
        AffiliationCtrl = self.AddTextCtrl(self,hSizer,self.AuthObj.get_affiliation())
        AffiliationCtrl.Bind(wx.EVT_TEXT, lambda event: self.OnChangeAuth(event, AffiliationCtrl, "affiliation"), AffiliationCtrl)
        self.MainSizer.Add(hSizer, flag=wx.EXPAND|wx.ALL, proportion=1, border=10)


    # ------------------------------------------------------------------------


    def createContentFor_Session(self):
        if self.eltid is None: return

        self.SessionObj = self.parent._dataPages['Sessions'][self.eltid]

        ############### SESSION ID ###############
        self.AddTitle(SESSION_ICON, self.SessionObj.get_sessionid())

        ############### NAME ###############
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.AddStaticText(self,hSizer,"Name: \t\t")
        nameCtrl = self.AddTextCtrl(self,hSizer,self.SessionObj.get_session_name())
        nameCtrl.Bind(wx.EVT_TEXT, lambda event: self.OnChangeSession(event, nameCtrl, "session_name"), nameCtrl)
        self.MainSizer.Add(hSizer, flag=wx.EXPAND|wx.ALL, proportion=1, border=10)

        ############### RANK  ###############
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.AddStaticText(self,hSizer,"Rank: \t\t")

        SpinCtrlRank = wx.SpinCtrl(self, -1)
        SpinCtrlRank.SetRange(0, 100)
        SpinCtrlRank.SetValue(self.SessionObj.get_rank())

        SpinCtrlRank.Bind(wx.EVT_SPINCTRL,  lambda event: self.OnChangeSession(event, SpinCtrlRank, "rank"), SpinCtrlRank)
        hSizer.Add(SpinCtrlRank)

        self.MainSizer.Add(hSizer, flag=wx.EXPAND|wx.ALL, proportion=1, border=10)

        ############### DATE ###############
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.AddStaticText(self,hSizer,"Date: \t")
        self.caldate = wx.calendar.CalendarCtrl(self, -1, wx.DateTime_Now(),
                                        style=wx.calendar.CAL_SHOW_HOLIDAYS | wx.calendar.CAL_SUNDAY_FIRST |
                                        wx.calendar.CAL_SEQUENTIAL_MONTH_SELECTION)
        # click on day
        self.caldate.Bind(wx.calendar.EVT_CALENDAR_DAY, self.onCalSelected)
        # change month
        self.caldate.Bind(wx.calendar.EVT_CALENDAR_MONTH, self.onCalSelected)
        # change year
        self.caldate.Bind(wx.calendar.EVT_CALENDAR_YEAR, self.onCalSelected)
        hSizer.Add(self.caldate, proportion=0)

        self.MainSizer.Add(hSizer, flag=wx.EXPAND|wx.ALL, proportion=1, border=10)

        ############### H-DEB  ###############
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.AddStaticText(self,hSizer,"Start time: \t")
        hdebCtrl = self.AddTextCtrl(self,hSizer,self.SessionObj.get_h_deb())
        hdebCtrl.Bind(wx.EVT_TEXT, lambda event: self.OnChangeSession(event, hdebCtrl, "h-deb"), hdebCtrl)
        self.MainSizer.Add(hSizer, flag=wx.EXPAND|wx.ALL, proportion=1, border=10)

        ############### H-FIN  ###############
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.AddStaticText(self,hSizer,"End time: \t")
        hfinCtrl = self.AddTextCtrl(self,hSizer,self.SessionObj.get_h_fin())
        hfinCtrl.Bind(wx.EVT_TEXT, lambda event: self.OnChangeSession(event, hfinCtrl, "h-fin"), hfinCtrl)
        self.MainSizer.Add(hSizer, flag=wx.EXPAND|wx.ALL, proportion=1, border=10)

        ############### CHAIRMAN ###############
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.AddStaticText(self,hSizer,"Chairman: \t")
        chairCtrl = self.AddTextCtrl(self,hSizer,self.SessionObj.get_chairman())
        chairCtrl.Bind(wx.EVT_TEXT, lambda event: self.OnChangeSession(event, chairCtrl, "chairman"), chairCtrl)
        self.MainSizer.Add(hSizer, flag=wx.EXPAND|wx.ALL, proportion=1, border=10)

        ############### LOCATION ###############
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.AddStaticText(self,hSizer,"Location: \t")
        locCtrl = self.AddTextCtrl(self,hSizer,self.SessionObj.get_location())
        locCtrl.Bind(wx.EVT_TEXT, lambda event: self.OnChangeSession(event, locCtrl, "location"), locCtrl)
        self.MainSizer.Add(hSizer, flag=wx.EXPAND|wx.ALL, proportion=1, border=10)

    # ------------------------------------------------------------------------


    # ------------------------------------------------------------------------
    # Callbacks
    # ------------------------------------------------------------------------


    def onCalSelected(self, event):

        setdate = event.GetDate()
        if setdate.IsValid():
            ymd = map(int, setdate.FormatISODate().split('-'))
            setdate = datetime.date(*ymd)
            self.SessionObj.set_date( setdate )


    def OnEditorShown(self, e):

        row       = e.GetRow()
        lastname  = self.authorsGrid.GetCellValue(row, 0)
        firstname = self.authorsGrid.GetCellValue(row, 1)

        author = Author(lastname,firstname)
        authorid = author.get_authorid()

        self.authorBeforeChange = self.parent._dataPages['Authors'][authorid]


    def OnEditorClosed(self, e):

        row = e.GetRow()
        if e.GetCol() == 0:
            lastname = self.authorsGrid.GetCellValue(row, 0)
            self.authorBeforeChange.set_lastname(lastname)
        elif e.getCol() == 1:
            firstname = self.authorsGrid.GetCellValue(row, 1)
            self.authorBeforeChange.set_lastname(firstname)


    def OnChangeDoc(self, e, CtrlObj, ValueToChange):

        if ValueToChange == "title":
            self.DocObj.set_title(CtrlObj.GetValue())
        elif ValueToChange == "session":
            sessionid = CtrlObj.GetStringSelection()
            if sessionid != "":
                session = self.parent._dataPages['Sessions'][sessionid]
            else:
                session = ""
            self.DocObj.set_session(session)
        elif ValueToChange == "rank":
            rank = CtrlObj.GetValue()
            self.DocObj.set_rank( int(rank) )


    def OnChangeAuth(self, e, CtrlObj, ValueToChange):

        if ValueToChange == 'lastname':
            self.AuthObj.set_lastname(CtrlObj.GetValue())
        elif ValueToChange == 'firstname':
            self.AuthObj.set_firstname(CtrlObj.GetValue())
        elif ValueToChange == 'email':
            self.AuthObj.set_email(CtrlObj.GetValue())
        elif ValueToChange == 'affiliation':
            self.AuthObj.set_affiliation(CtrlObj.GetValue())


    def OnAddAuthor(self, e):

        AddAuthorWindow = AddAuthor(self, -1, self.DocObj)
        retCode = AddAuthorWindow.ShowModal()

        if retCode == wx.ID_OK:
            author = AddAuthorWindow.GetAuthorSelected()

            self.authorsGrid.AppendRows(1)
            lastRow = self.authorsGrid.GetNumberRows()
            self.authorsGrid.SetCellValue(lastRow-1,0,author.get_lastname())
            self.authorsGrid.SetCellValue(lastRow-1,1,author.get_firstname())

            authorList = self.DocObj.get_authors()
            authorList.append( author )
            self.DocObj.set_authors(authorList)
            self.Refresh()

        AddAuthorWindow.Destroy()


    def OnChangeSession(self, e, CtrlObj, ValueToChange):

        if ValueToChange == 'session_name':
            self.SessionObj.set_session_name(CtrlObj.GetValue())
            # TODO: propagate to documents!

        elif ValueToChange == 'h-deb':
            self.SessionObj.set_h_deb(CtrlObj.GetValue())

        elif ValueToChange == 'h-fin':
            self.SessionObj.set_h_fin(CtrlObj.GetValue())

        elif ValueToChange == 'chairman':
            self.SessionObj.set_chairman(CtrlObj.GetValue())

        elif ValueToChange == 'location':
            self.SessionObj.set_location(CtrlObj.GetValue())

        elif ValueToChange == "rank":
            self.SessionObj.set_rank( CtrlObj.GetValue() )


    def OnRemove(self, e):

        col = e.GetCol()
        row = e.GetRow()

        if(col == -1 and row != -1):

            dlg = wx.MessageDialog(self, "Do you really want to remove this author?", "Warning", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
            retCode = dlg.ShowModal()

            if retCode == wx.ID_YES:
            # destruction de la partie concernée dans l'objet document.
                lastname = self.authorsGrid.GetCellValue(row, 0)
                firstname = self.authorsGrid.GetCellValue(row, 1)
                author = Author(lastname,firstname)
                authorid = author.get_authorid()

                authorToRemove = self.parent._dataPages['Authors'][authorid]
                self.parent._dataPages['Documents'][self.eltid].get_authors().remove(authorToRemove)

                self.Refresh()


    def Refresh(self):
        self.initialize()

        w, h = self.GetSize()

        self.SetSizeWH(w, h + 1)
        self.SetSizeWH(w, h)

# ----------------------------------------------------------------------------


class AddAuthor(wx.Dialog):

    def __init__(self, parent, id, DocObject):

        wx.Dialog.__init__(self, parent, id, "Add author", size=(240, 180),style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        self.SetMinSize((200, 200))
        self.DocObject = DocObject
        self.parent = parent.GetParent()
        self.initialize()


    def initialize(self):

        self.SetBackgroundColour(BACKGROUND_COLOR)

        MainSizer = wx.BoxSizer(wx.VERTICAL)

        choices = list()
        for author in self.parent._dataPages['Authors'].values():
            if author not in self.DocObject.get_authors():
                choices.append(author.get_authorid())

        self.authorSelecteur = wx.Choice(self, -1, choices=sorted(choices))
        MainSizer.Add(self.authorSelecteur, proportion=1, flag=wx.ALL|wx.ALIGN_CENTER, border=50)

        btnSizer = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        MainSizer.Add(btnSizer)

        self.SetSizer(MainSizer)


    def GetAuthorSelected(self):
        authorid = self.authorSelecteur.GetStringSelection()
        return self.parent._dataPages['Authors'][authorid]


