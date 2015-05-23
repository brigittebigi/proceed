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
# ----------------------------------------------------------------------------
# File: ctrlutils.py
# ----------------------------------------------------------------------------

__docformat__ = """epytext"""
__authors__   = """Brigitte Bigi"""
__copyright__ = """Copyright (C) 2011-2015  Brigitte Bigi"""

# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

import wx
from wx.lib.buttons import GenBitmapButton, GenBitmapTextButton
from wxgui.cutils.imageutils import spBitmap

# ----------------------------------------------------------------------------

def CreateButton(parent, bmp, handler, sizer, colour=None):
    """ Create a bitmap button and bind the event. """

    btn = wx.BitmapButton(parent, -1, bmp, style=wx.NO_BORDER)
    if colour is not None:
        btn.SetBackgroundColour( colour )
    btn.SetInitialSize()
    btn.Bind(wx.EVT_BUTTON, handler)
    btn.Enable( True )

    return btn

# ----------------------------------------------------------------------------

def CreateGenButton(parent, id, bmp, text=None, tooltip=None, colour=None, SIZE=24, font=None):
    """ Create a bitmap button. """

    if text is None:
        button = GenBitmapButton(parent, id, bmp)
    else:
        button = GenBitmapTextButton(parent, id, bmp, text)
        if font: button.SetFont( font )

    button.SetBezelWidth(1)

    if tooltip is not None:
        button.SetToolTipString( tooltip )
    if colour is not None:
        button.SetBackgroundColour( colour )

    return button

# ----------------------------------------------------------------------------
