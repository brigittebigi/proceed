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

from datasession  import Session

# ---------------------------------------------------------------------------

class Validate:
    """
    @authors: Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: Check if all data are OK.

    """

    def __init__(self, documents, authors, sessions):
        """
        Create a new Validate instance.

        @param documents (dict) is a dictionay of Document instances with docid as keys
        @param authors (dict) is a dictionary of Author instances with authorid as keys
        @param sessions (dict) is a dictionary of Session instances with sessionid as keys

        """
        self.documents = documents
        self.authors   = authors
        self.sessions  = sessions

    # -----------------------------------------------------------------------


    def pdffiles(self, path):
        """
        Check if all pdf files are in the directory.
        Return the list of missing files.
        """
        no_pdf = []
        for doc in self.documents.values():
            pdfdoc = os.path.join(path, doc.get_docid() + ".pdf")
            if os.path.isfile(pdfdoc) is False:
                no_pdf.append(pdfdoc)
        return no_pdf

    # -----------------------------------------------------------------------


    def session_in_documents(self):
        """
        Check if all documents are related to a session.
        Return the list of docid without session.
        """
        no_session = []
        for doc in self.documents.values():
            docsession = doc.get_session()
            if isinstance(docsession,Session) is False:
                no_session.append(doc.get_docid())
        return no_session

    # -----------------------------------------------------------------------


    def rank_in_documents(self):
        """
        Check if all documents have a rank.
        Return the list of docid without rank.
        """
        no_rank = []
        for doc in self.documents.values():
            rank = doc.get_rank()
            if rank == 0:
                no_rank.append(doc.get_docid())
        return no_rank

    # -----------------------------------------------------------------------


    def name_in_sessions(self):
        """
        Check if all sessions (with at least one document) have a name.
        """
        no_name = []
        for doc in self.documents.values():
            docsession = doc.get_session()
            if isinstance(docsession,Session) is True:
                sessionid = docsession.get_sessionid()
                try:
                    session = self.sessions[sessionid]
                    if session.get_session_name() == "" and sessionid not in no_name:
                        no_name.append(sessionid)
                except KeyError:
                    if sessionid not in no_name:
                        no_name.append(sessionid)
        return no_name

    # -----------------------------------------------------------------------


    def date_in_sessions(self):
        """
        Check if all sessions (with at least one document) have a date.
        """
        no_date = []
        for doc in self.documents.values():
            docsession = doc.get_session()
            if isinstance(docsession,Session) is True:
                sessionid = docsession.get_sessionid()
                try:
                    session = self.sessions[sessionid]
                    if session.get_date() == "" and sessionid not in no_date:
                        no_date.append(sessionid)
                except KeyError:
                    if sessionid not in no_date:
                        no_date.append(sessionid)
        return no_date

    # -----------------------------------------------------------------------


    def rank_in_sessions(self):
        """
        Check if all sessions (with at least one document) have a rank.
        """
        no_rank = []
        for doc in self.documents.values():
            docsession = doc.get_session()
            if isinstance(docsession,Session) is True:
                sessionid = docsession.get_sessionid()
                try:
                    session = self.sessions[sessionid]
                    if session.get_rank() == "" and sessionid not in no_rank:
                        no_rank.append(sessionid)
                except KeyError:
                    if sessionid not in no_rank:
                        no_rank.append(sessionid)
        return no_rank

    # -----------------------------------------------------------------------

# ---------------------------------------------------------------------------

