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

    def write( self, docs, pathname ):
        try:
            if os.path.exists(os.path.join(pathname,"Documents.csv")) is True:
                os.remove(os.path.join(pathname,"Documents.csv"))
            if os.path.exists(os.path.join(pathname,"Sessions.csv")) is True:
                os.remove(os.path.join(pathname,"Sessions.csv"))
            if os.path.exists(os.path.join(pathname,"Authors.csv")) is True:
                os.remove(os.path.join(pathname,"Authors.csv"))

            out_documents = csv.DictWriter(open(os.path.join(pathname,"Documents.csv"), 'wb'), fieldnames=["DOCID", "TITLE", "LASTNAME", "FIRSTNAME", "SESSION_ID", "RANK", "PAGE_NUMBER"])
            out_documents.writerow({"DOCID":"DOCID", "TITLE":"TITLE", "LASTNAME":"LASTNAME", "FIRSTNAME":"FIRSTNAME", "SESSION_ID":"SESSION_ID", "RANK":"RANK", "PAGE_NUMBER":"PAGE_NUMBER"})

            out_sessions = csv.DictWriter(open(os.path.join(pathname,"Sessions.csv"), 'wb'), fieldnames=["SESSION_ID", "SESSION_NAME", "DATE_STR", "DATE", "H-DEB", "H-FIN", "CHAIRMAN", "LOCATION"])
            out_sessions.writerow({"SESSION_ID":"SESSION_ID", "SESSION_NAME":"SESSION_NAME", "DATE_STR":"DATE_STR", "DATE":"DATE", "H-DEB":"H-DEB", "H-FIN":"H-FIN", "CHAIRMAN":"CHAIRMAN", "LOCATION":"LOCATION"})

            out_authors = csv.DictWriter(open(os.path.join(pathname,"Authors.csv"), 'wb'), fieldnames=["LASTNAME", "FIRSTNAME", "EMAIL", "AFFILIATION"])
            out_authors.writerow({"LASTNAME":"LASTNAME", "FIRSTNAME":"FIRSTNAME", "EMAIL":"EMAIL", "AFFILIATION":"AFFILIATION"})

        except IOError,e:
            raise e

        for doc in docs:
            print "docid=",doc.get_docid()
            if doc.get_status()==self._status:
                print " ... ",doc.get_pdfdiagnosis()
                for auth in doc.get_authors():
                    Docid = str(doc.get_docid())
                    Title = doc.get_title()
                    LastName = self.__format(auth.get_lastname())
                    FirstName = self.__format(auth.get_firstname())
                    Email = self.__format(auth.get_email())

                    affiliationList = list()

                    for numlabo in auth.get_labos():
                        labo = doc.get_laboratory()[int(numlabo)]
                        affiliationList.append(self.__format(', '.join(labo.get_affiliations())))

                    if ( len(affiliationList) != 0):
                        affiliations = ' '.join(affiliationList)
                    else:
                        affiliations = ' '

                    out_documents.writerow({"DOCID":Docid.encode('utf-8'), "TITLE":Title.encode('utf-8'), "LASTNAME":LastName.encode('utf-8'), "FIRSTNAME":FirstName.encode('utf-8'), "SESSION_ID":"", "RANK":"", "PAGE_NUMBER":""})
                    out_authors.writerow({"LASTNAME":LastName.encode('utf-8'), "FIRSTNAME":FirstName.encode('utf-8'), "EMAIL":Email.encode('utf-8'), "AFFILIATION":affiliations.encode('utf-8')})

    def __format(self,s):
        # = s.replace("_", "\_")
        # = a.replace("%", "\%")
        # = a.replace("&", "\&")
        a = s.replace("\s", " ")
        return a


#-----------------------------------------------------------------------------
