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

__docformat__ = "epytext"

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

import codecs
import csv
import logging

from DataIO.Documents.documents import document, author, laboratory
from readgeneric import readGeneric

# ---------------------------------------------------------------------------

def unicode_csv_reader(unicode_csv_data,  **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                             delimiter = ";", **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')

# ---------------------------------------------------------------------------
# Class
# ---------------------------------------------------------------------------

class readEasyChair( readGeneric ):
    """
    @authors: Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: Read CSV files extracted from easychair XLSX snapshot file.

    """

    def __init__( self ):
        pass


    # overwrite
    def GetDocs(self, filename, authorsfilename=None):
        """
        Return a list of document instances from filename.

        @param filename is the CSV file name containing submissions.
        @param authorsfilename contains details about authors (optional).

        CSV files are supposed to be UTF-8 encoded and the separator is ';'.
        """
        # Get submissions
        withauthors = not authorsfilename
        self.DocTab = self.createDocuments(filename,withauthors)

        # Get details about authors
        if authorsfilename is not None:
            self.addAuthors(authorsfilename)

        return self.DocTab


    def createDocuments ( self,filename,withauthors ):

        documentsTab = list()

        with codecs.open(filename, "r", encoding='utf8') as f:
             
            reader = unicode_csv_reader(f)           
            rownum = 0
            for line in reader:
                # Save header row.
                if rownum == 0:
                    keynames = line
                    print keynames
                    rownum = 1
                    continue

                tabline = line
                try:
                    # Document identifier
                    docid = tabline[ keynames.index('#') ].strip()
                    if not len(docid):
                        continue

                    # Create a new document instance
                    newDoc = document( docid )

                    # Data
                    title    = tabline[ keynames.index('title') ].strip()
                    keywords = tabline[ keynames.index('keywords') ].strip()
                    decision = tabline[ keynames.index('decision') ].strip()
                    abstract = tabline[ keynames.index('abstract') ].strip()
                    # tracks are in easychair but not in sciencesconf
                    # but... subjects are in sciencesconfs and not in easychair
                    # so, use subject instance to manage tracks!
                    track = tabline[ keynames.index('track') ].strip()

                    newDoc.set_title( title )
                    newDoc.set_subject( track )
                    newDoc.set_keywords( self._parse_keywords(keywords) )
                    newDoc.set_status(   self._parse_decision(decision) )
                    newDoc.set_abstract( self._parse_abstract(abstract) )

                    if withauthors is True:
                        authors  = tabline[ keynames.index('authors') ].strip()
                        newDoc.set_authors(  self._parse_authors(authors)  )

                    # append the new document in the list
                    documentsTab.append(newDoc)

                except Exception, e:
                    print " ... ERROR", str(e)
                    pass

        return documentsTab


    def addAuthors(self, filename):

        if not self.DocTab: return

        with codecs.open(filename, "r", encoding='utf8') as f:
            keynames = f.readline().strip().split(';')
            for line in f:
                tabline = line.split(';')
                # each line is an author
                newAuthor = author( tabline[ keynames.index('#') ].strip() )
                newAuthor.set_firstname(  tabline[ keynames.index('first names') ].strip() )
                newAuthor.set_lastname(  tabline[ keynames.index('last name') ].strip() )
                newAuthor.set_email( tabline[ keynames.index('email') ].strip() )
                newAuthor.set_url( tabline[ keynames.index('Web site') ].strip() )
                newAuthor.set_corresponding( len( tabline[ keynames.index('corresponding') ].strip() ) )

                docid = tabline[ keynames.index('submission') ].strip()
                for d in self.DocTab:
                    if d.get_docid() == docid:
                        # Add the labo to the doc (if not already done)
                        laboidx = self.addLabo(d, keynames, tabline)
                        # Add the labo to the author
                        newAuthor.set_labos(laboidx) # with easychair, an author can have only one lab.
                        # Add the author to the doc
                        d.append_author( newAuthor )
                        break


    def addLabo(self, doc, keynames, tabline):
        labname = tabline[ keynames.index('organization') ].strip()
        country = tabline[ keynames.index('country') ].strip()

        for lab in doc.get_laboratory():
            if lab.get_nom() == labname:
                return [ lab.get_num() ]

        lab = laboratory( len( doc.get_laboratory() ))
        lab.set_nom( labname )
        lab.set_country( country )
        doc.append_laboratory( lab )
        for lab in doc.get_laboratory():
            if lab.get_nom() == labname:
                return [ lab.get_num() ]

        return [ lab.get_num() ]


    def _parse_authors(self, line):
        # It is supposed that the lastname is the last string!
        authors = list()
        line = line.replace(' and ', ' , ')
        tabline = line.split(',')
        for a in tabline:
            tab_a = a.split()
            newAuthor = author(0)
            firstname = " ".join(tab_a[0:-1])
            lastname  = tab_a[-1]
            newAuthor.set_firstname( firstname )
            newAuthor.set_lastname( lastname )
            authors.append( newAuthor )
        return authors


    def _parse_keywords(self, line):
        # It is supposed that keywords are separated by "~"
        return line.split('~')


    def _parse_decision(self, line):
        if "accept" in line:
            return 1
        if "reject" in line:
            return 3
        return 0


    def _parse_abstract(self, line):
        line = line.replace (' ~', '')
        return line.strip()


# with open('example.csv', 'rb') as csvfile:
#     dialect = csv.Sniffer().sniff(csvfile.read(1024))
#     csvfile.seek(0)
#     reader = csv.DictReader(csvfile, fieldnames=None, restkey=None, restval=None, dialect=dialect, *args, **kwds)
#
#     Create an object which operates like a regular reader but maps the information read into a dict
#     whose keys are given by the optional fieldnames parameter. The fieldnames parameter is a sequence
#     whose elements are associated with the fields of the input data in order.
#     These elements become the keys of the resulting dictionary. If the fieldnames parameter is omitted,
#     the values in the first row of the csvfile will be used as the fieldnames. If the row read has more
#     fields than the fieldnames sequence, the remaining data is added as a sequence keyed by the value
#     of restkey. If the row read has fewer fields than the fieldnames sequence, the remaining keys take
#     the value of the optional restval parameter. Any other optional or keyword arguments are passed to
#     the underlying reader instance.


