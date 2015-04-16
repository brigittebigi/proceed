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
import logging

from Manager.models.datasession  import Session
from Manager.models.datadocument import Document
from Manager.models.dataauthor   import Author

import Manager.consts as consts

# ---------------------------------------------------------------------------
# Class
# ---------------------------------------------------------------------------

class InformationPanel( wx.Panel ):
    """
    @author: Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: A panel with a set of information (key/data).

    """

    def __init__(self, parent):
        """
        Constructor.
        """
        wx.Panel.__init__(self, parent, -1, style=wx.NO_BORDER)
        self.SetBackgroundColour(consts.BACKGROUND_COLOR)

        sizer = wx.BoxSizer( wx.VERTICAL )
        self.SetSizer( sizer )
        self.number_of_infos = 0

    # ------------------------------------------------------------------------


    def CleanContent(self):
        logging.debug(' Remove current information. ')
        while self.number_of_infos > 0:
            self.GetSizer().Hide(self.number_of_infos-1)
            self.GetSizer().Remove(self.number_of_infos-1)
            self.number_of_infos -= 1
        self.Update()
        self.Fit()

    # ------------------------------------------------------------------------


    def AddContent(self, anyObject):
        if isinstance(anyObject, Document):
            self.AddContentForDocument(anyObject)
        elif isinstance(anyObject, Author):
            self.AddContentForAuthor(anyObject)
        elif isinstance(anyObject, Session):
            self.AddContentForSession(anyObject)
        else:
            raise TypeError('Invalid object type: none of Author, Document or Session.')

    # ------------------------------------------------------------------------


    def AddContentForDocument(self, DocObject):

        self.CleanContent()
        logging.debug(' Show document information. ')

        ############ TITLE ############
        self.__addTextInfo("Title: \t", DocObject.get_title())

        ############ AUTHORS ############
        authstr = ""
        for author in DocObject.get_authors():
            authstr = authstr + author.get_firstname()+" "+author.get_lastname()+", "
        self.__addTextInfo("Authors: \t", authstr)

        ############ SESSION ############
        if isinstance(DocObject.get_session(), Session):
            sessionid = DocObject.get_session().get_sessionid()
        else:
            sessionid = "No session set"
        self.__addTextInfo("Session: \t", sessionid)

        ############ RANK ############
        rank = DocObject.get_rank()
        if( rank == 0 or rank == ""):
            rank = "No rank set"
        self.__addTextInfo("Rank in the session: ", str(rank))

        self.Layout()
        self.Fit()

    # ------------------------------------------------------------------------


    def AddContentForSession(self, SessionObject):

        self.CleanContent()
        logging.debug(' Show session information. ')

        ############ SESSION NAME ############
        name = SessionObject.get_session_name()
        if name == "":
            name = "Nothing set"
        self.__addTextInfo("Name: \t\t\t", name)

        ############ SESSION RANK IN THE DAY ############
        rank = SessionObject.get_rank()
        if rank == 0:
            rank = "No value"
        self.__addTextInfo("Rank in the day: \t", str(rank))

        ############ DATE ############
        date = str(SessionObject.get_date())
        if date == None or date == "":
            date = "Nothing set"
        self.__addTextInfo("Date: \t\t\t", date)

        ############ HOURS ############
        start_time = SessionObject.get_h_deb()
        if start_time == "":
            start_time = "Nothing set"
        self.__addTextInfo("Start time: \t\t", start_time)

        ############ HOURS ############
        end_time = SessionObject.get_h_fin()
        if end_time == "":
            end_time = "Nothing set"
        self.__addTextInfo("End time: \t\t", end_time)

        ############ chairman ############
        chairman = SessionObject.get_chairman()
        if chairman == "":
            chairman = "Nothing set"
        self.__addTextInfo("Chairman: \t\t", chairman)

        ############ location ############
        location = SessionObject.get_location()
        if location == "":
            location = "Nothing set"
        self.__addTextInfo("Location: \t\t", location)

        self.Layout()
        self.Fit()

    # ------------------------------------------------------------------------


    def AddContentForAuthor(self, AuthorObject):

        self.CleanContent()
        logging.debug(' Show author information. ')

        ############ LASTNAME ############
        self.__addTextInfo("Last Name: \t", AuthorObject.get_lastname())

        ############ FIRSTNAME ############
        self.__addTextInfo("First Name: \t", AuthorObject.get_firstname())

        ############ EMAIL ############
        if AuthorObject.get_email() != "":
            email = AuthorObject.get_email()
        else:
            email = 'No email set'
        self.__addTextInfo("Email: \t\t", email)

        ############ AFFILIATION ############
        if AuthorObject.get_affiliation() != "":
            affiliation = AuthorObject.get_affiliation()
        else:
            affiliation = 'No affiliation set'
        self.__addTextInfo("Affiliation: \t", affiliation)

        ############ DOCUMENTS ############
        # TODO: trouver une façon PROPRE d'obtenir la liste des docs...
        docs = ""
        for d in self.GetTopLevelParent().nbp._dataPages['Documents'].values():
            if AuthorObject in d.get_authors():
                docs = docs + d.get_docid() + ", "
        self.__addTextInfo("Documents ID: \t", docs)

        self.Layout()
        self.Fit()

    # ------------------------------------------------------------------------


    def __addTextInfo(self, label, info):

        hSizer = wx.BoxSizer(wx.HORIZONTAL)

        txt = wx.StaticText(self, -1, label)
        font = wx.Font(consts.FONTSIZE, consts.FONTFAMILY, wx.NORMAL, wx.BOLD)
        txt.SetFont(font)
        hSizer.Add(txt)

        if info is not None:
            txt = wx.StaticText(self, -1, info)
            font = wx.Font(consts.FONTSIZE, consts.FONTFAMILY, wx.NORMAL, wx.NORMAL)
            txt.SetFont(font)
            hSizer.Add(txt)

        self.GetSizer().Add(hSizer, flag=wx.EXPAND|wx.ALL, proportion=1, border=20)
        self.number_of_infos += 1

    # ------------------------------------------------------------------------
