#!/usr/bin/env python
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
# File: option.py
# ----------------------------------------------------------------------------

__docformat__ = """epytext"""
__authors__   = """Brigitte Bigi"""
__copyright__ = """Copyright (C) 2011-2015  Brigitte Bigi"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

import wx

# ----------------------------------------------------------------------------


class Option:
    """
    @author:  Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL, v3
    @summary: This class is used to deal with one option of one preference value.

    One option of one preference value (Private class).

    """

    def __init__(self, optiontype, optionvalue, optiontext=""):
        """
        Creates a new Option() instance.

        Example of use:
            optiontype:  boolean
            optionvalue: True
            optiontext:  This is the text in the preferences dialog

        optiontype is a string; one of:
            boolean, int, float, string, wx.colour, wx.size, wx.font

        """
        self._type  = optiontype.lower()
        self._value = optionvalue
        self._text  = optiontext


    # ------------------------------------------------------------------------
    # Getters
    # ------------------------------------------------------------------------

    def get_type(self):
        """
        Return the type (as a String) of the option.
        """
        return self._type


    def get_untypedvalue(self):
        """
        Return the typed-value.
        """
        return self._value


    def get_value(self):
        """
        Return the typed-value.
        """

        if self._type.startswith('bool'): return self._value

        if self._type.startswith('int') or self._type == 'long' or self._type == 'short': return int(self._value)

        if self._type == 'float' or self._type == 'double': return float(self._value)

        if self._type.startswith('str'): return self._value.decode('utf-8')

        if self._type == 'wx.size':
            #(w,h) = self._value
            #return wx.Size(w,h)
            return int(self._value)

        if self._type == 'wx.colour':
            if self._value is None:
                return None
            (r,g,b) = self._value
            return wx.Colour(r,g,b)

        if self._type == 'wx.font':
            (size, family, style, weight, u, face, enc) = self._value
            return wx.Font(size, family, style, weight, u, face, enc)

        if self._type == 'wx.align':
            if self._value.lower() == 'left':
                return wx.ALIGN_LEFT
            if self._value.lower() == 'right':
                return wx.ALIGN_RIGHT
            return wx.ALIGN_CENTRE

        raise TypeError


    def get_text(self):
        """ Return the text which describes the option. """
        return self._text


    # ------------------------------------------------------------------------
    # Setters
    # ------------------------------------------------------------------------


    def set(self, other):
        """
        Set self to an other instance.
        """
        self._type  = other.get_type()
        self.set_value( other.get_value() )
        self._text  = other.get_text()


    def set_value(self, value):
        """
        Set a new typed-value.
        """
        if self._type == 'wx.font':
            size   = value.GetPointSize()
            family = value.GetFamily()
            style  = value.GetStyle()
            weight = value.GetWeight()
            underline = value.GetUnderlined()
            face = value.GetFaceName()
            encoding = value.GetEncoding()
            self._value = (size, family, style, weight, underline, face, encoding)
        elif self._type == 'wx.size':
            (w,h) = value
            self._value = (w,h)
        elif self._type == 'wx.colour':
            if value is None:
                self._value = None
            (r,g,b) = value
            self._value = (r,g,b)
        elif self._type == 'wx.align':
            if value == wx.ALIGN_LEFT or value == 'left':
                self._value = 'left'
            elif value == wx.ALIGN_RIGHT or value == 'right':
                self._value = 'right'
            else:
                self._value = 'centre'
        else:
            self._value = value


    def set_text(self, text):
        """
        Set a text to describe the option.
        """
        self._text = text

    # ------------------------------------------------------------------------
