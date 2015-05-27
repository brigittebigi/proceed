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

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

import os
from threading import Thread

from indexwriter import IndexWriter
from csvwriter   import CSVWriter
from htmlwriter  import HTMLWriter
from latexwriter import LaTeXWriter

import utils.fileutils as fileutils

# ---------------------------------------------------------------------------
# Class
# ---------------------------------------------------------------------------

class Writer( Thread ):
    """
    @authors: Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: Fix the appropriate writer then write documents.

    """

    def __init__(self, docs):
        Thread.__init__(self)

        self._progress = None
        self._docs = docs
        self._status = 1

        self.start()

    # End __init__
    #-------------------------------------------------------------------------

    def set_progress(self, p):
        self._progress = p


    def set_status(self, s):
#         try:
#             ints = int(s)
#         except Exception,e:
#             raise TypeError('The status value must be an integer value (0-4).')
        if s < 0 or s > 4:
            raise ValueError('The status value is not in an appropriate range (0-4).')
        self._status = s

    # End set_status
    #-------------------------------------------------------------------------


    def writeLaTeX_as_Dir(self, outputname, prefs, tocompile=True):
        """
        Write the authors/title/abstract of each document in separated LaTeX files.
        """
        if self._progress:
            self._progress.set_new()
            self._progress.set_header("Write each abstract in LaTeX")
            self._progress.update(0,"")

        latex = LaTeXWriter( prefs=prefs )
        total = len(self._docs)
        fileutils.createdir(outputname)

        for i,doc in enumerate(self._docs):
            if self._progress:
                # Indicate the file to be processed
                self._progress.set_text( "Paper id: "+doc.get_docid() )

            if doc.get_status() == self._status:
                docfilename = os.path.join(outputname, doc.get_docid()+".tex")
                latex.write_doc( doc, docfilename, tocompile )

            if self._progress:
                self._progress.set_fraction(float((i+1))/float(total))

        # Indicate completed!
        if self._progress:
            self._progress.update(1,"Completed.")
            self._progress.set_header("")


    # End writeLaTeX_as_Dir
    #-------------------------------------------------------------------------

    def write_as_file( self, outputname ):
        """
        Write the list of authors/title/... of each document in a file
        depending on the given extension. Supported extensions are:
        tex, html, idx, csv.
        """

        if outputname.lower().endswith("tex"):
            self.writeLaTeX( outputname )
        elif outputname.lower().endswith("html"):
            self.writeHTML( outputname )
        elif outputname.lower().endswith("idx"):
            self.writeIndex( outputname )
        elif outputname.lower().endswith("csv"):
            self.writeCSV( outputname )
        else:
            raise Exception("Unknown output file format")

    # End write_as_file
    #-------------------------------------------------------------------------


    def writeHTML(self, outputname):
        """
        Write the list of authors/title/... of each document in an HTML file.
        """
        # Remove existing output file
        if os.path.exists(outputname) is True:
            os.remove(outputname)

        # Write the list of authors/title of each document
        html = HTMLWriter( self._status )
        html.write_as_list( self._docs, outputname )

    # End writeHTML
    #-------------------------------------------------------------------------


    def writeLaTeX(self, outputname, prefs):
        """
        Write the list of authors/title/... of each document in a LaTeX file.
        """
        # Remove existing output file
        if os.path.exists(outputname) is True:
            os.remove(outputname)

        # Write the list of authors/title/... of each document
        latex = LaTeXWriter( self._status, prefs )
        latex.write_as_list( self._docs, outputname )

    # End writeLaTeX
    #-------------------------------------------------------------------------


    def writeIndex(self, outputname):
        """
        Write the list of authors/title/... of each document in a IDX file.
        """

        # Remove existing output file
        if os.path.exists(outputname) is True:
            os.remove(outputname)

        # Write the list of authors/title/... of each document
        ind = IndexWriter( self._status )
        ind.write( self._docs, outputname )

    # End writeIndex
    #-------------------------------------------------------------------------


    def writeCSV(self, outputname):
        """
        Write the list of authors/title/... of each document in a CSV file.
        """

        # Write the list of authors/title/... of each document
        ind = CSVWriter( self._status )
        ind.write( self._docs, outputname )

    # End writeCSV
    #-------------------------------------------------------------------------

# End Writer
#-----------------------------------------------------------------------------
