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
#           http://sldr.org/sldr00800/preview/
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
# ----------------------------------------------------------------------------
# File: consts.py
# ----------------------------------------------------------------------------

import os.path
import wx

from sp_glob import BASE_PATH
from sp_glob import program, version

# ---------------------------------------------------------------------------
# Define all paths (relatively to SPPAS base path)
# ---------------------------------------------------------------------------

PREFS_FILE = os.path.join( BASE_PATH , "etc", "proceed.prefs")
HELP_PATH  = os.path.join( os.path.dirname(BASE_PATH), "documentation", "etc")
DOC_IDX    = os.path.join( HELP_PATH, "doc", "markdown.idx")

HELP_IDX_EXT = ".idx"


# ---------------------------------------------------------------------------
# Base components:

FRAME_STYLE = wx.DEFAULT_FRAME_STYLE|wx.CLOSE_BOX
FRAME_TITLE = program + " - " + version

# ---------------------------------------------------------------------------
# GUI design.

MIN_PANEL_W = 180
MIN_PANEL_H = 220

MIN_FRAME_W=640
MIN_FRAME_H=400

if wx.Platform == "__WXMSW__":
    FRAME_H  = 600   # expected "good" height
    PANEL_W  = 320   # Left/Right panel (FLP)
else:
    FRAME_H  = 520   # expected "good" height
    PANEL_W  = 380

MENU_ICONSIZE   = 16
TB_ICONSIZE     = 24
BUTTON_ICONSIZE = 32

# ---------------------------------------------------------------------------

if wx.Platform == '__WXMAC__':
    FONTSIZE = 12
elif wx.Platform == '__WXGTK__':
    FONTSIZE = 9
else:
    FONTSIZE = 10

TB_FONTSIZE     = FONTSIZE - 2
HEADER_FONTSIZE = FONTSIZE + 4

FONTFAMILY = wx.FONTFAMILY_DECORATIVE
    # Choose one of:
        #wx.FONTFAMILY_DEFAULT     Chooses a default font.
        #wx.FONTFAMILY_DECORATIVE  A decorative font.
        #wx.FONTFAMILY_ROMAN       A formal, serif font.
        #wx.FONTFAMILY_SCRIPT      A handwriting font.
        #wx.FONTFAMILY_SWISS       A sans-serif font.
        #wx.FONTFAMILY_MODERN      Usually a fixed pitch font.
        #wx.FONTFAMILY_TELETYPE    A teletype font.

# ---------------------------------------------------------------------------

BACKGROUND_COLOR = "#E3E3E3"

ASK_BEFORE_EXIT  = False
    # Choose one of: True/False


# ----------------------------------------------------------------------------
