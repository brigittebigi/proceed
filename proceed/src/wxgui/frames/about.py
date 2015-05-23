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
# ----------------------------------------------------------------------------
# File: about.py
# ----------------------------------------------------------------------------

__docformat__ = """epytext"""
__authors__   = """Brigitte Bigi"""
__copyright__ = """Copyright (C) 2011-2015  Brigitte Bigi"""


# -------------------------------------------------------------------------
# Imports
# -------------------------------------------------------------------------

import wx

from sp_glob import program, version, author, copyright, brief, url, license_text
from wxgui.sp_icons import APP_ICON
from wxgui.cutils.imageutils import spBitmap


# ----------------------------------------------------------------------------

class AboutBox( wx.AboutDialogInfo ):
    """
    @author:  Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL, v3
    @summary: This class is used to display an about frame.

    """

    def __init__(self):
        """ Constructor. """

        wx.AboutDialogInfo.__init__(self)
        BMP_APP_ICON = spBitmap( APP_ICON )

        _icon = wx.EmptyIcon()
        _icon.CopyFromBitmap( BMP_APP_ICON )
        self.SetIcon(_icon)

        self.SetName( program )
        self.SetVersion( version )
        self.SetDescription( brief )
        self.SetCopyright( copyright )
        self.SetWebSite( url )
        self.SetLicence( license_text )
        self.AddDeveloper( author )
        self.AddDocWriter( author )
        self.AddArtist('')

    #---------------------------------------------------------------------

# ----------------------------------------------------------------------------
