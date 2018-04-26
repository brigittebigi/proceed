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

import codecs

from DataIO.Documents.documents import document, author, laboratory
from readgeneric import readGeneric

# ---------------------------------------------------------------------------


class readEasyChair(readGeneric):
    """
    :authors: Brigitte Bigi
    :contact: brigitte.bigi@gmail.com
    :license: GPL
    
    Read CSV files extracted from easychair XLSX snapshot file.

    """
    def __init__(self):
        self.DocTab = None

    # -----------------------------------------------------------------------

    # overwrite
    def GetDocs(self, filename, authorsfilename=None):
        """ Return a list of document instances from filename.

        :param filename: (str) the CSV file name containing submissions.
        :param authorsfilename: details about authors (optional).

        CSV files are supposed to be UTF-8 encoded and the separator is ';'.

        """
        # Get submissions
        withauthors = not authorsfilename
        self.DocTab = self.createDocuments(filename, withauthors)

        # Get details about authors
        if authorsfilename is not None:
            self.addAuthors(authorsfilename)

        return self.DocTab

    # -----------------------------------------------------------------------

    def createDocuments(self, filename, withauthors):

        documents = list()

        with codecs.open(filename, "r", encoding='utf8') as f:
             
            reader = readGeneric.unicode_csv_reader(f)
            rownum = 0
            for line in reader:
                # Save header row.
                if rownum == 0:
                    keynames = line
                    rownum = 1
                    continue

                tabline = line
                try:
                    # Document identifier
                    docid = tabline[keynames.index('#')].strip()
                    if not len(docid):
                        continue

                    # Create a new document instance
                    new_doc = document(docid)

                    # Data
                    title = tabline[keynames.index('title')].strip()
                    keywords = tabline[keynames.index('keywords')].strip()
                    decision = tabline[keynames.index('decision')].strip()
                    abstract = tabline[keynames.index('abstract')].strip()
                    # tracks are in easychair but not in sciencesconf
                    # but... subjects are in sciencesconfs and not in easychair
                    # so, use subject instance to manage tracks!
                    track = tabline[keynames.index('track')].strip()

                    new_doc.set_title(title)
                    new_doc.set_subject(track)
                    new_doc.set_keywords(readEasyChair._parse_keywords(keywords))
                    new_doc.set_status(readEasyChair._parse_decision(decision))
                    new_doc.set_abstract(readEasyChair._parse_abstract(abstract))

                    if withauthors is True:
                        authors = tabline[keynames.index('authors')].strip()
                        new_doc.set_authors(readEasyChair._parse_authors(authors))

                    # append the new document in the list
                    documents.append(new_doc)

                except Exception as e:
                    print(" ... ERROR: {}".format(str(e)))

        return documents

    # -----------------------------------------------------------------------

    def addAuthors(self, filename):

        if not self.DocTab:
            return

        with codecs.open(filename, "r", encoding='utf8') as f:
            keynames = f.readline().strip().split(';')
            for line in f:
                tabline = line.split(';')
                # each line is an author
                new_author = author(tabline[keynames.index('#')].strip())
                new_author.set_firstname(tabline[ keynames.index('first names')].strip())
                new_author.set_lastname(tabline[ keynames.index('last name')].strip())
                new_author.set_email(tabline[keynames.index('email')].strip())
                new_author.set_url(tabline[keynames.index('Web site')].strip())
                new_author.set_corresponding(len(tabline[keynames.index('corresponding')].strip()))

                docid = tabline[keynames.index('submission')].strip()
                for d in self.DocTab:
                    if d.get_docid() == docid:
                        # Add the labo to the doc (if not already done)
                        laboidx = self.addLabo(d, keynames, tabline)
                        # Add the labo to the author
                        new_author.set_labos(laboidx)  # with easychair, an author can have only one lab.
                        # Add the author to the doc
                        d.append_author(new_author)
                        break

    # -----------------------------------------------------------------------

    def addLabo(self, doc, keynames, tabline):
        labname = tabline[keynames.index('organization')].strip()
        country = tabline[keynames.index('country')].strip()

        for lab in doc.get_laboratory():
            if lab.get_nom() == labname:
                return [lab.get_num()]

        lab = laboratory(len(doc.get_laboratory()))
        lab.set_nom(labname)
        lab.set_country(country)
        doc.append_laboratory(lab)
        for lab in doc.get_laboratory():
            if lab.get_nom() == labname:
                return [lab.get_num()]

        return [lab.get_num()]

    # -----------------------------------------------------------------------
    # Private
    # -----------------------------------------------------------------------

    @staticmethod
    def _parse_authors(line):
        # It is supposed that the lastname is the last string!
        authors = list()
        line = line.replace(' and ', ', ')
        tabline = line.split(',')
        for a in tabline:
            tab_a = a.split()
            new_author = author(0)
            firstname = " ".join(tab_a[0:-1])
            lastname = tab_a[-1]
            new_author.set_firstname(firstname)
            new_author.set_lastname(lastname)
            authors.append(new_author)

        return authors

    # -----------------------------------------------------------------------

    @staticmethod
    def _parse_keywords(line):
        # It is supposed that keywords are separated by "~"
        return line.split('~')

    # -----------------------------------------------------------------------

    @staticmethod
    def _parse_decision(line):
        if "accept" in line:
            return 1
        if "reject" in line:
            return 3
        return 0

    # -----------------------------------------------------------------------

    @staticmethod
    def _parse_abstract(line):
        line = line.replace(' ~', '')
        return line.strip()

