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

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

import os.path
import csv
from sp_glob import fieldnames

# ---------------------------------------------------------------------------
# Class
# ---------------------------------------------------------------------------

class CSVWriter:
    """
    @authors: Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: Write documents into 3 CSV files: Authors, Documents, Sessions.

    """

    def __init__( self, status=1 ):
        self._status = status

    def __fields_to_dict(self, fields):
        d = {}
        for f in fields:
            d[f] = f
        return d

    def write( self, docs, pathname ):
        try:
            if os.path.exists(os.path.join(pathname,"Documents.csv")) is True:
                os.remove(os.path.join(pathname,"Documents.csv"))
            if os.path.exists(os.path.join(pathname,"Sessions.csv")) is True:
                os.remove(os.path.join(pathname,"Sessions.csv"))
            if os.path.exists(os.path.join(pathname,"Authors.csv")) is True:
                os.remove(os.path.join(pathname,"Authors.csv"))
            if os.path.exists(os.path.join(pathname,"Conference.csv")) is True:
                os.remove(os.path.join(pathname,"Conference.csv"))

            out_documents = csv.DictWriter(open(os.path.join(pathname,"Documents.csv"), 'wb'), fieldnames=fieldnames['Documents'])
            out_documents.writerow( self.__fields_to_dict(fieldnames['Documents']) )

            out_sessions = csv.DictWriter(open(os.path.join(pathname,"Sessions.csv"), 'wb'), fieldnames=fieldnames['Sessions'])
            out_sessions.writerow( self.__fields_to_dict(fieldnames['Sessions']) )

            out_authors = csv.DictWriter(open(os.path.join(pathname,"Authors.csv"), 'wb'), fieldnames=fieldnames['Authors'])
            out_authors.writerow( self.__fields_to_dict(fieldnames['Authors']) )

            out_conf = csv.DictWriter(open(os.path.join(pathname,"Conference.csv"), 'wb'), fieldnames=fieldnames['Conference'])
            out_conf.writerow( self.__fields_to_dict(fieldnames['Conference']) )

        except IOError:
            raise

        for doc in docs:
            if doc.get_status()==self._status:
                for auth in doc.get_authors():
                    Docid = str(doc.get_docid())
                    Title = doc.get_title().encode('utf-8')
                    LastName = self.__format(auth.get_lastname()).encode('utf-8')
                    FirstName = self.__format(auth.get_firstname()).encode('utf-8')
                    Email = self.__format(auth.get_email()).encode('utf-8')
                    PDFDiag = str(doc.get_pdfdiagnosis())

                    affiliationList = list()

                    for numlabo in auth.get_labos():
                        labo = doc.get_laboratory()[int(numlabo)]
                        affiliationList.append(self.__format(', '.join(labo.get_affiliations())))

                    if ( len(affiliationList) != 0):
                        affiliations = ' '.join(affiliationList).encode('utf-8')
                    else:
                        affiliations = ' '

                    out_documents.writerow({"DOCID":Docid, "TITLE":Title, "LASTNAME":LastName, "FIRSTNAME":FirstName, "SESSION_ID":"", "RANK":"", "PAGE_NUMBER":"", "PDF_DIAGNOSIS":PDFDiag})
                    out_authors.writerow({"LASTNAME":LastName, "FIRSTNAME":FirstName, "EMAIL":Email, "AFFILIATION":affiliations})

    def __format(self,s):
        a = s.replace("\s", " ")
        return a


#-----------------------------------------------------------------------------
