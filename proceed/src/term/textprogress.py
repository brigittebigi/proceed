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
# File: textprogress.py
# ----------------------------------------------------------------------------

__docformat__ = """epytext"""
__authors__   = """Brigitte Bigi (brigitte.bigi@gmail.com)"""
__copyright__ = """Copyright (C) 2011-2015  Brigitte Bigi"""


# ----------------------------------------------------------------------------

import sys
import re
import math
from terminalcontroller import TerminalController


# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------

WIDTH  = 74
BAR    = '%3d%% ${GREEN}[${BOLD}%s%s${NORMAL}${GREEN}]${NORMAL}\n'
HEADER = '${BOLD}${CYAN}%s${NORMAL}\n\n'

# ----------------------------------------------------------------------------

class TextProgress:
    """
    @authors: Brigitte Bigi
    @contact: brigitte.bigi((AATT))lpl-aix.fr
    @license: GPL
    @summary: A 3-lines progress self.bar.

    It looks like::

                            Header
    20% [===========----------------------------------]
                       progress message

    The progress self.bar is colored, if the terminal supports color
    output; and adjusts to the width of the terminal.

    """


    def __init__(self):
        """
        Constructor.
        """
        try:
            self.term = TerminalController()
        except:
            self.term = None

        if not (self.term.CLEAR_EOL and self.term.UP and self.term.BOL):
            self.term = None

        self.bar = BAR
        if self.term:
            self.bar = self.term.render(BAR)
        self.cleared = 1 #: true if we haven't drawn the self.bar yet.
        self.percent = 0
        self.text    = ""

    # End __init__
    # ------------------------------------------------------------------


    def update(self, percent, message):
        """
        Update the progress.

        @param text:     progress self.bar text  (default: None)
        @param fraction: progress self.bar value (default: 0)

        """
        n = int((WIDTH-10)*percent)

        if self.term:
            sys.stdout.write(
                self.term.BOL + self.term.UP + self.term.CLEAR_EOL +
                (self.bar % (100*percent, '='*n, '-'*(WIDTH-10-n))) +
                self.term.CLEAR_EOL + message.center(WIDTH))
        else:
            sys.stdout.write( '  => ' + message + " \n")

        self.percent = percent
        self.text    = message

    # End update
    # ------------------------------------------------------------------


    def clear(self):
        """
        Clear.
        """
        if not self.cleared:
            if self.term:
                sys.stdout.write(self.term.BOL + self.term.CLEAR_EOL +
                                 self.term.UP + self.term.CLEAR_EOL +
                                 self.term.UP + self.term.CLEAR_EOL)
            else:
                sys.stdout.write('\n'*50)
            self.cleared = 1

    # End clear
    # ------------------------------------------------------------------


    def set_fraction(self, percent):
        """
        Set a new progress value.

        @param fraction: new progress value

        """
        self.update(percent,self.text)

    # End set_fraction
    # ------------------------------------------------------------------


    def set_text(self,text):
        """
        Set a new progress text.

        @param text: new progress text

        """
        self.update(self.percent,text)

    # End set_text
    # ------------------------------------------------------------------


    def set_header(self,header):
        """
        Set a new progress label.

        @param label: new progress label

        """
        if self.term:
            self.header = self.term.render(HEADER % header.center(WIDTH))
        else:
            self.header = "          " + header

        sys.stdout.write(self.header)

    # End set_header
    # ------------------------------------------------------------------


    def set_new(self):
        """
        Initialize a new progress line.

        """
        sys.stdout.write('\n')
        self.clear()
        self.text = ""
        self.percent = 0

    # End set_new
    # ------------------------------------------------------------------
