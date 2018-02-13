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

import sys
import os.path
from readgeneric import readGeneric

# ---------------------------------------------------------------------------
# Class
# ---------------------------------------------------------------------------

class Reader():
    """
    @authors: Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: Fix the appropriate reader then load documents.

    """

    def __init__(self, arguments={}):
        self._reader = self.__get_reader(arguments)
        self._docs   = None
        if "filename" in arguments.keys():
            file1 = arguments['filename']
            file2 = None
            if 'authorsfilename' in arguments.keys():
                file2 = arguments['authorsfilename']
            self._docs = self._reader.GetDocs( file1,file2 )

    # End __init__
    #-------------------------------------------------------------------------


    def __get_reader(self, arguments):
        """
        Return the reader depending on the reader name in arguments.
        """
        if arguments['readername'] == "sciencesconf":
            from readXML import readXML
            if 'progress' in arguments.keys():
                return readXML( arguments['progress'] )
            return readXML()

        if arguments['readername'] == "easychair":
            from readEasyChair import readEasyChair
            return readEasyChair()

        raise ValueError('Unknown reader')

    # End __get_reader
    #-------------------------------------------------------------------------


    def LoadDocs(self, filename):
        self._docs = self._reader.GetDocs( filename )
        return self._docs

    #-------------------------------------------------------------------------

    def __docs__(self):
        return self._docs

    #-------------------------------------------------------------------------

    docs = property(__docs__)

    #-------------------------------------------------------------------------
