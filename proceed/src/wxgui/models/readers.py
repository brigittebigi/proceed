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

import csv
import datetime

from dataauthor  import Author
from datasession import Session

# ---------------------------------------------------------------------------

class conference_csv_reader:
    """
    @authors: Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: CSV reader for conference information.

    """
    def __init__(self, fileName):
        self.fileName = fileName

    # -----------------------------------------------------------------------

    def get_Rows(self):
        csvReader = csv.DictReader(open(self.fileName, "rb"))
        return csvReader

    def get_Acronym(self, row):
        return row['ACRONYM']

    def get_ConfName(self, row):
        return row['CONFERENCE_NAME']

    def get_Place(self, row):
        return row['PLACE']

    def get_DateFrom(self, row):
        return row['DATE_FROM']

    def get_DateTo(self, row):
        return row['DATE_TO']

# ---------------------------------------------------------------------------

class documents_csv_reader:
    """
    @authors: Bastien Herbaut, Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: CSV reader for documents.

    """
    def __init__(self, fileName):
        self.fileName = fileName

    # -----------------------------------------------------------------------

    def get_Rows(self):
        csvReader = csv.DictReader(open(self.fileName, "rb"))
        return csvReader

    def get_DocId(self, row):
        return row['DOCID']

    def get_DocTitle(self, row):
        return row["TITLE"]

    def get_Author(self, row):
        return Author(row["LASTNAME"],row["FIRSTNAME"])

    def get_Session(self, row):
        if row["SESSION_ID"] != "":
            return Session(row["SESSION_ID"])
        return ""

    def get_Rank(self, row):
        rank = row["RANK"]
        if len(rank)==0:
            return 0
        try:
            r = int(rank)
        except Exception:
            raise TypeError('Can not convert rank='+rank+' into line='+row['DOCID'])
        return r

    def get_NumPage(self, row):
        return row["PAGE_NUMBER"]

    def get_Diagnosis(self, row):
        d = row["PDF_DIAGNOSIS"]
        if len(d)==0:
            return -2
        try:
            r = int(d)
        except Exception:
            raise TypeError('Can not convert pdf diagnosis='+d+' into line='+row['DOCID'])
        return r

    # -----------------------------------------------------------------------

    def get_all_ids(self):

        csvReader = csv.DictReader(open(self.fileName, "rb"))
        docidList = list()
        for row in csvReader:
            docid = self.get_DocId(row)
            if( docid in docidList ):
                continue
            docidList.append(docid)

        return docidList

    # -----------------------------------------------------------------------

    def get_ById(self, docid):

        csvReader = csv.DictReader(open(self.fileName, "rb"))
        good_rows = list()

        for row in csvReader:
            if(self.get_DocId(row) != docid):
                continue
            good_rows.append(row)

        return good_rows

    # -----------------------------------------------------------------------

    def get_ByAuthor(self, AuthorLastName, AuthorFirstName):

        csvReader = csv.DictReader(open(self.fileName, "rb"))
        good_rows = list()
        for row in csvReader:
            if(self.get_AuthorLastName(row) != AuthorLastName):
                continue
            elif(self.get_AuthorFirstName(row) != AuthorFirstName):
                continue
            good_rows.append(row)

        return good_rows

    # -----------------------------------------------------------------------

# ---------------------------------------------------------------------------

class authors_csv_reader:
    """
    @authors: Bastien Herbaut, Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: CSV reader for authors.

    """

    def __init__(self, fileName):
        self.fileName = fileName

    # -----------------------------------------------------------------------

    def get_Rows(self):
        csvReader = csv.DictReader(open(self.fileName, "rb"))
        return csvReader

    def get_FirstName(self, row):
        return row["FIRSTNAME"]

    def get_LastName(self, row):
        return row["LASTNAME"]

    def get_email(self, row):
        return row["EMAIL"]

    def get_Affiliation(self, row):
        return row["AFFILIATION"]

    # -----------------------------------------------------------------------

    def get_all_names(self):

        csvReader = csv.DictReader(open(self.fileName, "rb"))
        authList = list()
        for row in csvReader:
            Names = (self.get_LastName(row), self.get_FirstName(row))
            if(Names in authList):
                continue
            authList.append(Names)

        return authList

    def get_ByNames(self, lastname, firstname):

        csvReader = csv.DictReader(open(self.fileName, "rb"))
        good_rows = list()
        for row in csvReader:
            if(self.get_FirstName(row) == firstname and self.get_LastName(row) == lastname):
                good_rows.append(row)

        return good_rows

    # -----------------------------------------------------------------------

# ---------------------------------------------------------------------------


class sessions_csv_reader:
    """
    @authors: Bastien Herbaut, Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: CSV reader for sessions.

    """


    def __init__(self, fileName):
        self.fileName = fileName

    # -----------------------------------------------------------------------

    def get_Rows(self):
        csvReader = csv.DictReader(open(self.fileName, "rb"))
        return csvReader

    def get_SessionId(self, row):
        return row["SESSION_ID"]

    def get_SessionName(self, row):
        return row["SESSION_NAME"]

    def get_Rank(self, row):
        rank = row["RANK"]
        if len(rank)==0:
            return 0
        try:
            r = int(rank)
        except Exception,e:
            raise TypeError('Can not convert rank='+rank)
        return r

    def get_Date(self, row):
        date_tab = row["DATE"].split("-") #YYYY-MM-DD
        if row["DATE"] != '':
            return datetime.date(int(date_tab[0]),int(date_tab[1]),int(date_tab[2]))
        return ''

    def get_Heure_Deb(self, row):
        return row["H-DEB"]

    def get_Heure_Fin(self, row):
        return row["H-FIN"]

    def get_Chairman(self, row):
        return row["CHAIRMAN"]

    def get_Location(self, row):
        return row["LOCATION"]

    # -----------------------------------------------------------------------
    # Global Data Getters
    # -----------------------------------------------------------------------

    def get_AllId(self):

        csvReader = csv.DictReader(open(self.fileName, "rb"))
        codes = list()
        for row in csvReader:
            codes.append(self.get_SessionId(row))

        return codes

    def get_ById(self, sessionId):

        csvReader = csv.DictReader(open(self.fileName, "rb"))
        good_rows = list()
        for row in csvReader:
            if self.get_SessionId(row) != sessionId:
                continue
            good_rows.append(row)

        return good_rows

    def get_ByDate(self, Date):

        csvReader = csv.DictReader(open(self.fileName, "rb"))
        good_rows = list()
        for row in csvReader:
            if(self.get_Date(row) != Date):
                continue
            good_rows.append(row)

        return good_rows

    # -----------------------------------------------------------------------
