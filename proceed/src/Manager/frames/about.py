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

# ---------------------------------------------------------------------------
# File: about.py implements the class AboutFrame
# ----------------------------------------------------------------------------

__docformat__ = "epytext"

# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

import wx


# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------

LICENSE = """Proceed is free software; you can redistribute
it and/or modify it under the terms of the GNU General Public License as
published by the Free Software Foundation; either version 3 of the License,
or (at your option) any later version.

Proceed is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details. You should have
received a copy of the GNU General Public License along with Proceed;
if not, write to the Free Software Foundation, Inc., 59 Temple Place,
Suite 330, Boston, MA  02111-1307  USA"""

DESCRIPTION = """Proceed is an advanced manager for conference documents. """

NAME = "Proceed"

VERSION = "1.1"


# ----------------------------------------------------------------------------
# Class AbouFrame
# ----------------------------------------------------------------------------

class AboutFrame( wx.AboutDialogInfo ):
    """
    @author:  Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: This class is used to open an AboutBox.

    Frame about Proceed.

    """

    def __init__(self, icon):
        """ Constructor. """

        wx.AboutDialogInfo.__init__(self)

        self.SetIcon(icon)
        self.SetName(NAME)
        self.SetVersion(VERSION)
        self.SetDescription(DESCRIPTION)
        self.SetCopyright('(C) 2013-2014 Laboratoire Parole et Langage')
        self.SetWebSite('http://www.lpl-aix.fr/~bigi/')
        self.SetLicence(LICENSE)
        self.AddDeveloper('Brigitte Bigi')
        self.AddDocWriter('Brigitte Bigi')
        #self.AddArtist('Oxygen icon set,\nGimp')
        #self.AddTranslator('Brigitte Bigi')

#-----------------------------------------------------------------------------
