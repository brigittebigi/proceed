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

__docformat__ = "epytext"

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

import wx
import sys
import os.path
from sp_glob import ICONS_PATH
from sp_glob import BASE_PATH
from sp_glob import SETTINGS_FILE

# ----------------------------------------------------------------------------
# GUI design
# ----------------------------------------------------------------------------

CONFIGPATH = os.path.join( os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),"etc")

DOCFILENAME  = os.path.join( BASE_PATH, "documentation", "documentation.html")
USERFILENAME = SETTINGS_FILE

# Frames
APP_ICON            = os.path.join(ICONS_PATH, "app.ico")
APP_CHECK_ICON      = os.path.join(ICONS_PATH, "appcheck.ico")
APP_EXPORT_PDF_ICON = os.path.join(ICONS_PATH, "appexport-pdf.ico")

# For the toolbar of the main frame
EXIT_ICON           = os.path.join(ICONS_PATH, "exit.png")
OPEN_ICON           = os.path.join(ICONS_PATH, "open.png")
SAVE_ICON           = os.path.join(ICONS_PATH, "save.png")
CHECK_ICON          = os.path.join(ICONS_PATH, "check.png")
EXPORT_ICON         = os.path.join(ICONS_PATH, "export.png")
ADD_ICON            = os.path.join(ICONS_PATH, "add.png")
EDIT_ICON           = os.path.join(ICONS_PATH, "edit.png")
DELETE_ICON         = os.path.join(ICONS_PATH, "delete.png")
ABOUT_ICON          = os.path.join(ICONS_PATH, "about.png")

# For the other frames
AUTHOR_ICON         = os.path.join(ICONS_PATH, "author.png")
DOCUMENT_ICON       = os.path.join(ICONS_PATH, "document.png")
SESSION_ICON        = os.path.join(ICONS_PATH, "session.png")



BACKGROUND_COLOR = "#E3E3E3"

ASK_BEFORE_EXIT  = False
    # Choose one of: True/False

FONTFAMILY = wx.FONTFAMILY_DECORATIVE
    # Choose one of:
        #wx.FONTFAMILY_DEFAULT     Chooses a default font.
        #wx.FONTFAMILY_DECORATIVE  A decorative font.
        #wx.FONTFAMILY_ROMAN       A formal, serif font.
        #wx.FONTFAMILY_SCRIPT      A handwriting font.
        #wx.FONTFAMILY_SWISS       A sans-serif font.
        #wx.FONTFAMILY_MODERN      Usually a fixed pitch font.
        #wx.FONTFAMILY_TELETYPE    A teletype font.

FONTSIZE = 10 # PointSize


# ----------------------------------------------------------------------------
# Notebook pages
# ----------------------------------------------------------------------------

PAGESLIST  = ['Documents','Authors','Sessions']
fieldnames = {}
fieldnames[PAGESLIST[0]] = ["DOCID", "TITLE", "LASTNAME", "FIRSTNAME", "SESSION_ID", "RANK", "PAGE_NUMBER"]
fieldnames[PAGESLIST[1]] = ["LASTNAME", "FIRSTNAME", "EMAIL", "AFFILIATION"]
fieldnames[PAGESLIST[2]] = ["SESSION_ID", "SESSION_NAME", "RANK", "DATE", "H-DEB", "H-FIN", "CHAIRMAN", "LOCATION"]

# ----------------------------------------------------------------------------

