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
        self.docid       = self.clean(docid)
        self.title       = self.clean(title)
        self.authors     = authors
        self.session     = session
        self.rank        = rank
        self.page        = page

    # End __init__
    # -----------------------------------------------------------------------


    def clean(self, entry):
        """
        Clean a string and encode to UTF-8.

        @param entry is the string to clean
        @return a string without special chars

        """
        s = ""
        if isinstance(entry, unicode):
            s = self.__clean(entry)
        elif entry is None:
            s = ""
        else:
            try:
                _unicode = entry.decode("utf-8")
            except UnicodeDecodeError as e:
                raise e
            s = self.__clean(_unicode)
        return s

    def __clean(self, entry):
        """ Clean a unicode string by removing tabs, CR/LF. """
        return " ".join(entry.split())

    # End clean
    # -----------------------------------------------------------------------


    def IsEmpty(self):

        if( self.docid == "" ):
            return True
        return False

    # End IsEmpty
    # -----------------------------------------------------------------------


    def prepare_save(self):

        rows = list()
        if len(self.authors) > 0:
            if isinstance(self.session, Session):
                for author in self.authors:
                    rows.append({"DOCID":self.docid, "TITLE":self.title.encode('utf8'), "LASTNAME":author.get_lastname().encode('utf8'), "FIRSTNAME":author.get_firstname().encode('utf8'), "SESSION_ID":self.session.get_sessionid().encode('utf8'), "RANK":str(self.rank), "PAGE_NUMBER":str(self.page)})
            else:
                for author in self.authors:
                    rows.append({"DOCID":self.docid, "TITLE":self.title.encode('utf8'), "LASTNAME":author.get_lastname().encode('utf8'), "FIRSTNAME":author.get_firstname().encode('utf8'), "SESSION_ID":"", "RANK":str(self.rank), "PAGE_NUMBER":str(self.page)})
        else:
            if isinstance(self.session, Session):
                rows.append({"DOCID":self.docid, "TITLE":self.title.encode('utf8'), "LASTNAME":"", "FIRSTNAME":"", "SESSION_ID":self.session.get_sessionid().encode('utf8'), "RANK":str(self.rank), "PAGE_NUMBER":str(self.page)})
            else:
                rows.append({"DOCID":self.docid, "TITLE":self.title.encode('utf8'), "LASTNAME":"", "FIRSTNAME":"", "SESSION_ID":"", "RANK":str(self.rank), "PAGE_NUMBER":str(self.page)})

        return rows


    # -----------------------------------------------------------------------
    ########## GETTEURS ##########
    # -----------------------------------------------------------------------

    def get_docid(self):
        return self.docid

    def get_title(self):
        return self.title

    def get_authors(self):
        return self.authors

    def get_session(self):
        return self.session

    def get_rank(self):
        return self.rank

    def get_page(self):
        return self.page


    # -----------------------------------------------------------------------
    ########## SETTEURS ##########
    # -----------------------------------------------------------------------

    def set_docid(self, new_docid):
        self.docid = new_docid

    def set_title(self, new_title):
        self.title = new_title

    def set_authors(self, new_authors):
        self.authors = new_authors

    def set_session(self, new_session):
        self.session = new_session

    def set_rank(self, new_rank):
        self.rank = new_rank

    def set_page(self, new_page):
        self.page = int(new_page)

    def set(self, other):
        if not isinstance(other,"Document"):
            return
        self.docid       = other.get_docid()
        self.title       = other.get_title()
        self.authors     = other.get_authors()
        self.session     = other.get_session()
        self.rank        = other.get_rank()
        self.page        = other.get_page()

    # -----------------------------------------------------------------------
    # -----------------------------------------------------------------------

    def __eq__(self, other) :
        """Surcharge de =="""

        if not isinstance(other, "Document"):
            return False

        if(self.docid != other.get_docid()):
            return False

        return True


    def __ne__(self, other) :
        """Surcharge de !="""
        return not self == other

    # -----------------------------------------------------------------------

