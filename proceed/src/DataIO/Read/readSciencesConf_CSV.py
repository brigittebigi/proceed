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
#       Copyright (C) 2013-2018  Brigitte Bigi
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
import logging

from DataIO.Documents.documents import document, author, laboratory
from readgeneric import readGeneric

# ---------------------------------------------------------------------------


class readSciencesConfCSV(readGeneric):
    """
    :authors: Brigitte Bigi
    :contact: brigitte.bigi@gmail.com
    :license: GPL

    Read CSV files extracted from sciencesconf snapshot file.

    """

    def __init__(self):
        self.col_doc_id = 0
        self.col_doc_abstract = 8
        self.col_doc_title = 9
        self.col_doc_keywords = 10
        self.col_doc_statut = 5
        self.col_doc_topic = 7
        self.col_doc_authors = 12
        self.col_doc_labs = 13
        self.DocTab = list()

    # -----------------------------------------------------------------------

    # overwrite
    def GetDocs(self, filename, authorsfilename=None):
        """ Return a list of document instances from filename.

        :param filename: (str) the CSV file name containing submissions.
        :param authorsfilename: IGNORED

        CSV files are supposed to be UTF-8 encoded and the separator is ';'.

        """
        self.DocTab = list()

        with codecs.open(filename, "r", encoding='utf8') as f:
            reader = readGeneric.utf8_csv_reader(f)

            author_nb = 1
            for row_num, line in enumerate(reader):

                logging.info("parse line {:d}".format(row_num))

                # Save header row.
                if row_num == 0:
                    self.col_doc_id = line.index('DOCID')
                    self.col_doc_title = line.index('TITLE')
                    self.col_doc_keywords = line.index('MOTCLE')
                    self.col_doc_abstract = line.index('ABSTRACT')
                    self.col_doc_statut = line.index('STATUT')
                    self.col_doc_topic = line.index('TOPIC')
                    self.col_doc_authors = line.index('AUTHORS')
                    self.col_doc_labs = line.index('LABOS')
                    continue

                try:
                    # Create a new document instance
                    doc_id = line[self.col_doc_id].strip()
                    logging.info(" ... doc ID: {:s}".format(doc_id))
                    new_doc = document(doc_id)

                    # Data about the document
                    title = line[self.col_doc_title].strip()
                    logging.info(" ... title: {:s}".format(title))

                    keywords = line[self.col_doc_keywords].strip()
                    decision = line[self.col_doc_statut].strip()
                    abstract = line[self.col_doc_abstract].strip()

                    new_doc.set_title(title)
                    new_doc.set_subject(self.col_doc_topic)
                    new_doc.set_keywords(self._parse_keywords(keywords))
                    new_doc.set_status(self._parse_decision(decision))
                    new_doc.set_abstract(self._parse_abstract(abstract))
                    logging.info(" ... status: {:d}".format(self._parse_decision(decision)))

                    # Authors of the document
                    # author_nb = new_doc.set_authors(
                    #    readSciencesConfCSV._parse_authors(new_doc,
                    #                                       line[self.col_doc_authors],
                    #                                       author_nb))

                    # append the new document in the list
                    self.DocTab.append(new_doc)

                except Exception as e:
                    print(" ... ERROR with line {:d}: {:s}".format(row_num, str(e)))
            f.close()

        logging.info(" ===>>> {:d} documents.".format(len(self.DocTab)))
        return self.DocTab

    # -----------------------------------------------------------------------
    # Private
    # -----------------------------------------------------------------------

    @staticmethod
    def _parse_labs(document, entry):
        """ -- NOT WORKING -- """

        for i, labo in enumerate(entry.split(",")):
            lab_data = labo.split("-")
            lab = laboratory(lab_data[0].strip())
            all_data = lab_data.split()
            name = list()
            for data in all_data:
                if data.startswith('('):
                    country = data.replace('(', '')
                    country = country.replace(')', '')
                    lab.set_country(country)

            lab.set_nom(" ".join(name))
            document.append_laboratory(lab)

    # -----------------------------------------------------------------------

    @staticmethod
    def _parse_authors(document, entry, nb):
        """ return authors. """

        for i, author in enumerate(entry.split(",")):
            new_author = author(nb)
            nb += 1

            all_data = author.split()
            name = list()
            for data in all_data:
                data = data.strip()
                if data.startswith("<"):
                    email = data.replace('<', '')
                    email = email.replace('>', '')
                    new_author.set_email(email)
                if data.startswith('('):
                    labo_nb = data.replace('(', '')
                    labo_nb = labo_nb.replace(')', '')
                    # we ignore ...
                else:
                    name.append(data)

            new_author.set_firstname(name[0])
            new_author.set_lastname(name[-1])
            if len(name) > 2:
                new_author.set_middlename(" ".join(name[1:-1]))

            # Add the author to the doc
            document.append_author(new_author)

        return nb

    # -----------------------------------------------------------------------

    @staticmethod
    def _parse_keywords(entry):
        # It is supposed that keywords are separated by ","
        return entry.split(',')

    # -----------------------------------------------------------------------

    @staticmethod
    def _parse_decision(entry):
        if "Accepté" in entry:
            return 1
        if "Refusé" in entry:
            return 3
        return 0

    # -----------------------------------------------------------------------

    @staticmethod
    def _parse_abstract(line):
        line = line.replace('\n', ' ')
        return line.strip()

