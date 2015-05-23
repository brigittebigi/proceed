#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# ---------------------------------------------------------------------------
#            ___   __    __    __    ___
#           /     |  \  |  \  |  \  /        Automatic
#           \__   |__/  |__/  |___| \__      Annotation
#              \  |     |     |   |    \     of
#           ___/  |     |     |   | ___/     Speech
#           =============================
#
#           http://sldr.org/sldr000800/preview/
#
# ---------------------------------------------------------------------------
# developed at:
#
#       Laboratoire Parole et Langage
#
#       Copyright (C) 2011-2015  Brigitte Bigi
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
# File: name.py
# ----------------------------------------------------------------------------

__docformat__ = """epytext"""
__authors__   = """Brigitte Bigi (brigitte.bigi@gmail.com)"""
__copyright__ = """Copyright (C) 2011-2015  Brigitte Bigi"""


# ----------------------------------------------------------------------------

import sys
import os
import random
import tempfile
from datetime import date

# ----------------------------------------------------------------------------

class genName():
    """
    @author: Brigitte Bigi
    @contact: brigitte.bigi((AATT))lpl-aix.fr
    @license: GPL
    @summary: A utility class which generates a random file name of a non-existing file.

    """
    def __init__(self):
        self.name = "/"
        while (os.path.exists(self.name) is True):
            self.set_name()


    def set_name(self):
        """
        Set a new file name.
        """
        # random float value
        randval  = str(int(random.random()*10000))
        # process pid
        pid      = str(os.getpid())
        # today's date
        today    = str(date.today())

        # filename
        filename = "sppas_tmp_"+today+"_"+pid+"_"+randval

        # final file name is path/filename
        tempdir = tempfile.gettempdir() # get the system temporary directory
        self.name = os.path.join(tempdir,filename)


    def get_name(self):
        """
        Get the current file name.
        """
        return str(self.name)


# ----------------------------------------------------------------------------

if __name__ == "__main__":
    print genName().get_name()

