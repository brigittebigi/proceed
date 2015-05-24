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

from datasession import Session
from utils.commons import clean

# ---------------------------------------------------------------------------


class Document:
    """
    @authors: Bastien Herbaut, Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: Storage class for a document (a submission).

    """

    def __init__(self, docid, title="", authors=list(), session="", rank=0, page=0):
        """
        Create a new Document instance.

        @param docid (String) is a unique value used to identify a document.
        @param title (String)
        @param authors is a list of Author instances
        @param session is a Session instance
        @param rank (int) is the rank of this document in the session
        @param page (int) is the starting page of the document

        """
        self._docid   = clean(docid)
        self._title   = clean(title)
        self._authors = authors
        self._session = clean(session)
        self._rank    = rank
        self._page    = page

    # End __init__
    # -----------------------------------------------------------------------

    def IsEmpty(self):

        if( self._docid == "" ):
            return True
        return False

    # -----------------------------------------------------------------------

    def prepare_save(self):

        rows = list()
        if len(self._authors) > 0:
            if isinstance(self._session, Session):
                for author in self._authors:
                    rows.append({"DOCID":self._docid, "TITLE":self._title, "LASTNAME":author.get_lastname(), "FIRSTNAME":author.get_firstname(), "SESSION_ID":self._session.get_sessionid(), "RANK":str(self._rank), "PAGE_NUMBER":str(self._page)})
            else:
                for author in self._authors:
                    rows.append({"DOCID":self._docid, "TITLE":self._title, "LASTNAME":author.get_lastname(), "FIRSTNAME":author.get_firstname(), "SESSION_ID":"", "RANK":str(self._rank), "PAGE_NUMBER":str(self._page)})
        else:
            if isinstance(self._session, Session):
                rows.append({"DOCID":self._docid, "TITLE":self._title, "LASTNAME":"", "FIRSTNAME":"", "SESSION_ID":self._session.get_sessionid(), "RANK":str(self._rank), "PAGE_NUMBER":str(self._page)})
            else:
                rows.append({"DOCID":self._docid, "TITLE":self._title, "LASTNAME":"", "FIRSTNAME":"", "SESSION_ID":"", "RANK":str(self._rank), "PAGE_NUMBER":str(self._page)})

        return rows


    # -----------------------------------------------------------------------
    ########## GETTEURS ##########
    # -----------------------------------------------------------------------

    def get_docid(self):
        return self._docid

    def get_title(self):
        return self._title

    def get_authors(self):
        return self._authors

    def get_session(self):
        return self._session

    def get_rank(self):
        return self._rank

    def get_page(self):
        return self._page


    # -----------------------------------------------------------------------
    ########## SETTEURS ##########
    # -----------------------------------------------------------------------

    def set_docid(self, new_docid):
        self._docid = clean(new_docid)

    def set_title(self, new_title):
        self._title = clean(new_title)

    def set_authors(self, new_authors):
        self._authors = new_authors

    def set_session(self, new_session):
        self._session = clean(new_session)

    def set_rank(self, new_rank):
        self._rank = new_rank

    def set_page(self, new_page):
        self._page = new_page

    def set(self, other):
        if not isinstance(other,"Document"):
            return
        self._docid       = other.get_docid()
        self._title       = other.get_title()
        self._authors     = other.get_authors()
        self._session     = other.get_session()
        self._rank        = other.get_rank()
        self._page        = other.get_page()

    # -----------------------------------------------------------------------

    def __eq__(self, other) :
        if not isinstance(other, "Document"):
            return False
        if(self._docid != other.get_docid()):
            return False
        return True

    def __ne__(self, other) :
        return not self == other

    # -----------------------------------------------------------------------
