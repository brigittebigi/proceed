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
#
import csv

# ---------------------------------------------------------------------------


class readGeneric(object):
    """
    Base class for an "abstract reader".
    This means that all sub-reader classes must implement these methods.

    Defines the interface for a generic document reader that provides common
    utilities required for generating formatted abstract submissions.

    """
    def GetDocs(self, filename, authorsfilename=None):
        """ Return a list of document instances.

        :param filename: (str)
        :param authorsfilename: (list or None)

        """
        pass

    # -----------------------------------------------------------------------

    @staticmethod
    def unicode_csv_reader(unicode_csv_data, **kwargs):
        # csv.py doesn't do Unicode; encode temporarily as UTF-8:
        csv_reader = csv.reader(readGeneric.utf_8_encoder(unicode_csv_data),
                                delimiter=";", **kwargs)
        for row in csv_reader:
            # decode UTF-8 back to Unicode, cell by cell:
            yield [unicode(cell, 'utf-8') for cell in row]

    # -----------------------------------------------------------------------

    @staticmethod
    def utf_8_encoder(unicode_csv_data):
        for line in unicode_csv_data:
            yield line.encode('utf-8')

    # -----------------------------------------------------------------------

    @staticmethod
    def utf8_csv_reader(utf8_csv_data, **kwargs):
        return csv.reader(readGeneric.utf_8_encoder(utf8_csv_data),
                          delimiter=";", **kwargs)
