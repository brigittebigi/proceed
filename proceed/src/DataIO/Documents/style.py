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

__docformat__ = "epytext"

# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

import platform


# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------

FONT_SIZES  = [10,11,12]
PAPER_SIZES = ['letterpaper', 'a4paper', 'legalpaper', 'a5paper', 'executivepaper', 'b5paper']


# ----------------------------------------------------------------------------
# Class
# ----------------------------------------------------------------------------

class documentsLaTeXStyle:
    """
    @authors: Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: Class to fix LaTeX documents style.

    """
    def __init__( self ):
        self.set_simple()


    def set_simple(self):
        self._title    = '\\renewcommand{\\title}[1]{\LaTeXtitle{\Large\\textbf{#1}}}'
        self._authors  = ''#\\renewcommand\\Authfont{\\normal}'
        self._labos    = '\\renewcommand\\Affilfont{\small}'
        self._email    = '\\newcommand{\\emailaddress}[1]{\\newline{\small\sf#1}}'
        self._keywords = '\\newcommand{\\keywords}[1]{}'
        self._abstract = '\\renewcommand\\abstract[1]{#1}'


    def set_amlap(self):
        # Fix a default style.
        # It was originally developed and used for AMLAP 2013 conference.
        self._title    = '\\renewcommand{\\title}[1]{\LaTeXtitle{\Large\\textsf{\\textbf{#1}}}}'
        self._authors  = '\\renewcommand\\Authfont{\scshape\small}'
        self._labos    = '\\renewcommand\\Affilfont{\itshape\small}'
        self._email    = '\\newcommand{\\emailaddress}[1]{\\newline{\sf#1}}'
        self._keywords = '\\newcommand{\\keywords}[1]{\\noindent{\small{\\textbf{Keywords}: }#1\par \\vskip.7\\baselineskip}}'
        self._abstract = '\\renewcommand\\abstract[1]{\\noindent{\small{\\textbf{Abstract}: }#1}}'


    def set_taln(self):
        self._title    = '\\renewcommand{\\title}[1]{\LaTeXtitle{\Large{\\textbf{#1}}}}'
        self._authors  = '\\renewcommand\\Authfont{\scshape}'
        self._labos    = '\\renewcommand\\Affilfont{\\normalfont}'
        self._email    = '\\newcommand{\\emailaddress}[1]{\\newline{\sf#1}}'
        self._keywords = u'\\newcommand{\\keywords}[1]{\\noindent{\small{\\textbf{Mots cl\'es}: }#1\par \\vskip.7\\baselineskip}}'
        self._abstract = u'\\renewcommand\\abstract[1]{\\noindent{\small{\\textbf{R\'esum\'e}. }#1}}'



# ----------------------------------------------------------------------------
# Class
# ----------------------------------------------------------------------------


class documentsProp:
    """
    @authors: Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: Class to fix documents properties.

    """
    def __init__( self ):

        self._fontsize  = "12pt"     # accept only: 10pt, 11pt, 12pt
        self._papersize = "a4paper"  # accept only: letterpaper (11��8.5 in), a4paper (29.7��21 cm), legalpaper (14��8.5 in), a5paper (21��14.8 cm), executivepaper (10.5��7.25 in), and b5paper (25��17.6 cm)
        self._margins   = Margins()
        self._margins.SetLeft(30)
        self._margins.SetRight(25)
        self._margins.SetTop(25)
        self._margins.SetBottom(25)
        self._parindent = 0          # accept from 0 to 20
        self._parskip   = 6          # accept from 0 to 20
        self._encoding  = "utf8"
        if 'windows' in platform.system().lower():
            self._encoding  = "latin1"
        elif 'mac' in platform.system().lower():
            self._encoding = "applemac"

    #-------------------------------------------------------------------------
    # Getters...
    #-------------------------------------------------------------------------

    def Get(self):
        """
        Return the instance.
        """
        return self

    # End Get
    #-------------------------------------------------------------------------


    def GetFontSize(self):
        """
        Return the document font size.
        """
        return self._fontsize

    # End GetFontSize
    #-------------------------------------------------------------------------


    def GetPaperSize(self):
        """
        Return the document paper size.
        """
        return self._papersize

    # End GetPaperSize
    #-------------------------------------------------------------------------


    def GetMargins(self):
        """
        Return the document margins.
        """
        return self._margins

    # End GetMargins
    #-------------------------------------------------------------------------


    def GetParindent(self):
        """
        Return the document paragraph indentation.
        """
        return self._parindent

    # End GetParindent
    #-------------------------------------------------------------------------


    def GetParskip(self):
        """
        Return the document paragraph skip (space between 2 paragraphs).
        """
        return self._parskip

    # End GetParskip
    #-------------------------------------------------------------------------


    def GetEncoding(self):
        """
        Return the document input enc.
        """
        return self._encoding

    # End GetEncoding
    #-------------------------------------------------------------------------


    #-------------------------------------------------------------------------
    # Setters...
    #-------------------------------------------------------------------------

    def SetFontSize(self, size):
        """
        Set the document font size.

        @param size (int) Font size. One of 10, 11 or 12.

        """

        if size in FONT_SIZES:
            self._fontsize = str(size)+"pt"
        else:
            raise ValueError('Font size not correct.')

    # End SetFontSize
    #-------------------------------------------------------------------------


    def SetPaperSize(self, format):
        """
        Set the document paper size.

        @param format (string) Paper format. One of: 'letterpaper', 'a4paper',
        'legalpaper', 'a5paper', 'executivepaper', 'b5paper'

        """

        if format in PAPER_SIZES:
            self._papersize = format
        else:
            raise ValueError('Paper size not correct.')

    # End SetPaperSize
    #-------------------------------------------------------------------------


    def SetMargins(self, margins):
        """
        Set the document margins.

        @param margins (Margins)

        """
        self._margins = margins

    # End GetMargins
    #-------------------------------------------------------------------------


    def SetMarginsFromValues(self, top=None, bottom=None, left=None, right=None):
        """
        Set the document margins from their values.

        @param top (int) Size of the top margin in millimeters
        @param bottom (int) Size of the bottom margin in millimeters
        @param left (int) Size of the left margin in millimeters
        @param right (int) Size of the right margin in millimeters

        """
        if top: self._margins.SetTop(top)
        if bottom: self._margins.SetBottom(bottom)
        if left: self._margins.SetLeft(left)
        if right: self._margins.SetRight(right)

    # End SetMarginsFromValues
    #-------------------------------------------------------------------------


    def SetParindent(self, value):
        """
        Set the document paragraph indentation.

        @param value (int) from 0 to 20.

        """
        if value in range(0,20):
            self._parindent = value
        else:
            raise ValueError('Bad Paragraph Indentation value.')

    # End SetParindent
    #-------------------------------------------------------------------------


    def SetParskip(self, value):
        """
        Set the document paragraph skip (space between 2 paragraphs).

        @param value (int) from 0 to 20

        """
        if value in range(0,20):
            self._parskip = value
        else:
            raise ValueError('Bad paragraph skip value.')

    # End SetParskip
    #-------------------------------------------------------------------------


# End documentsProp
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
# Class Margins
#-----------------------------------------------------------------------------

class Margins:
    """
    Fix margins: top, bottom, left, right.

    Default values are 0.
    """

    def __init__(self, margin=0):
        """
        Create a new Margins instance with default values.
        """
        self._left   = margin
        self._right  = margin
        self._top    = margin
        self._bottom = margin

    # End __init__
    #-------------------------------------------------------------------------


    #-------------------------------------------------------------------------
    # Getters...
    #-------------------------------------------------------------------------

    def Get(self):
        """
        Return the Margins instance.
        """
        return self

    # End Get
    #-------------------------------------------------------------------------


    def GetLeft(self):
        """
        Return left margin value (int).
        """
        return self._left

    # End GetLeft
    #-------------------------------------------------------------------------


    def GetRight(self):
        """
        Return right margin value (int).
        """
        return self._right

    # End GetRight
    #-------------------------------------------------------------------------


    def GetTop(self):
        """
        Return top margin value (int).
        """
        return self._top

    # End GetTop
    #-------------------------------------------------------------------------


    def GetBottom(self):
        """
        Return left margin value (int).
        """
        return self._bottom

    # End GetBottom
    #-------------------------------------------------------------------------


    #-------------------------------------------------------------------------
    # Setters...
    #-------------------------------------------------------------------------

    def Set(self, other):
        """
        Set other margin values to self.
        """
        # copy values
        self._left   = other.GetLeft()
        self._right  = other.GetRight()
        self._top    = other.GetTop()
        self._bottom = other.GetBottom()

    # End Set
    #-------------------------------------------------------------------------


    def SetMargins(self, margin):
        """
        Set all margins to a specific value (int).
        """
        self._left   = margin
        self._right  = margin
        self._top    = margin
        self._bottom = margin

    # End SetMargins
    #-------------------------------------------------------------------------


    def SetLeft(self, margin):
        """
        Set left margin to a specific value (int).
        """
        self._left = margin

    # End Set
    #-------------------------------------------------------------------------


    def SetRight(self, margin):
        """
        Set right margin to a specific value (int).
        """
        self._right = margin

    # End Set
    #-------------------------------------------------------------------------


    def SetTop(self, margin):
        """
        Set top margin to a specific value (int).
        """
        self._top = margin

    # End Set
    #-------------------------------------------------------------------------


    def SetBottom(self, margin):
        """
        Set bottom margin to a specific value (int).
        """
        self._bottom = margin

    # End Set
    #-------------------------------------------------------------------------

# End Margins
#-----------------------------------------------------------------------------

