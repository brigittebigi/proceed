#! /usr/bin/env python
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

import sys
import os
import random
import tempfile
from datetime import date

# ---------------------------------------------------------------------------

class GenName():
    """
    @authors: Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: A class to generates a random file name of a non-existing file.

    """
    def __init__(self,extension=""):
        self.name = "/"
        while (os.path.exists(self.name)==True):
            self.set_name(extension)


    def set_name(self, extension):
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
        filename = "tmp_"+today+"_"+pid+"_"+randval

        # final file name is path/filename
        self.name = filename + extension


    def get_name(self):
        """
        Get the current file name.
        """
        return str(self.name)

# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print GenName().get_name()

# ---------------------------------------------------------------------------
