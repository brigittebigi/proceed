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
# File: cthemes.py
# ----------------------------------------------------------------------------

__docformat__ = """epytext"""
__authors__   = """Brigitte Bigi"""
__copyright__ = """Copyright (C) 2011-2015  Brigitte Bigi"""


# -------------------------------------------------------------------------
# Imports
# -------------------------------------------------------------------------

from structs.option import Option
from structs.themes import BaseTheme, Themes
import platform

# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------

FONT_SIZES  = [10,11,12]
PAPER_SIZES = ['letterpaper', 'a4paper', 'legalpaper', 'a5paper', 'executivepaper', 'b5paper']


# ----------------------------------------------------------------------------
# Specific themes for SppasEdit component
# ----------------------------------------------------------------------------
#

class ThemeBasic( BaseTheme ):
    """
    The theme which assign all required options, with default values.
    Already used for TRASP 2013 and Larp 2014.
    """

    def __init__(self):

        BaseTheme.__init__(self)

        # Papers: ["a4paper", "letterpaper", "b5paper", "a5paper" ]
        self._choice['PAPER_SIZE']    = Option('str', 'a4paper', "Paper format")
        self._choice['FONT_SIZE']     = Option('str', '12pt', "Font size")
        self._choice["MARGIN_LEFT"]   = Option('int', 30) # millimeters
        self._choice["MARGIN_RIGHT"]  = Option('int', 30) # millimeters
        self._choice["MARGIN_TOP"]    = Option('int', 25) # millimeters
        self._choice["MARGIN_BOTTOM"] = Option('int', 25) # millimeters
        self._choice['ENCODING']      = Option('str', 'utf8')
        self._choice['PARINDENT']     = Option('int', 0)
        self._choice['PARSKIP']       = Option('int', 6)

        self._choice['TITLE'] 		= Option('str', '\\renewcommand{\\title}[1]{\LaTeXtitle{\Large\\textbf{#1}}}')
        self._choice['LABOS']		= Option('str', '\\renewcommand\\Affilfont{\small}')
        self._choice['AUTHORS']		= Option('str', '\\renewcommand\\Authfont{\\normalfont}')
        self._choice['EMAIL']       = Option('str', '\\newcommand{\\emailaddress}[1]{\\newline{\small\sf#1}}')
        self._choice['KEYWORDS']    = Option('str', '\\newcommand{\\keywords}[1]{}')
        self._choice['ABSTRACT']    = Option('str' ,'\\renewcommand\\abstract[1]{#1}')

        # Just a reminder about LaTeX:
        # \textrm   \rmfamily   Roman family
        # \textsf   \sffamily   Sans serif family
        # \texttt   \ttfamily   Typewriter family
        #
        # \textup   \upshape    Upright shape
        # \textit   \itshape    Italic shape
        # \textsl   \slshape    Slanted shape
        # \textsc   \scshape    Small caps shape
        #
        # \textmd   \mdseries   Medium series
        # \textbf   \bfseries   Boldface series

        if 'windows' in platform.system().lower():
            self._encoding  = "latin1"
        elif 'mac' in platform.system().lower():
            self._encoding = "applemac"

# ----------------------------------------------------------------------------

class ThemePalme( ThemeBasic ):
    """ Theme already used for Amlap 2013 conference """

    def __init__(self):

        ThemeBasic.__init__(self)

        self._choice['TITLE'] 		= Option('str', '\\renewcommand{\\title}[1]{\LaTeXtitle{\Large\\textsf{\\textbf{#1}}}}')
        self._choice['LABOS']		= Option('str', '\\renewcommand\\Affilfont{\itshape\small}')
        self._choice['EMAIL']    	= Option('str', '\\newcommand{\\emailaddress}[1]{\\newline{\sf#1}}')
        self._choice['KEYWORDS']	= Option('str', '\\newcommand{\\keywords}[1]{\\noindent{\small{\\textbf{Keywords}: }#1\par \\vskip.7\\baselineskip}}')
        self._choice['ABSTRACT'] 	= Option('str' ,'\\renewcommand\\abstract[1]{\\noindent{\small{\\textbf{Abstract}: }#1}}')
        self._choice['AUTHORS']		= Option('str', '\\renewcommand\\Authfont{\scshape\small}')

# ----------------------------------------------------------------------------

class ThemeNalte( ThemeBasic ):
    """ Theme already used for TALN 2014 conference """

    def __init__(self):

        ThemeBasic.__init__(self)

        self._choice['TITLE'] 		= Option('str', '\\renewcommand{\\title}[1]{\LaTeXtitle{\Large{\\textbf{#1}}}}')
        self._choice['LABOS']		= Option('str', '\\renewcommand\\Affilfont{\\normalfont}')
        self._choice['EMAIL']    	= Option('str', '\\newcommand{\\emailaddress}[1]{\\newline{\sf#1}}')
        self._choice['KEYWORDS']	= Option('str', u'\\newcommand{\\keywords}[1]{\\noindent{\small{\\textbf{Mots clés}: }#1\par \\vskip.7\\baselineskip}}')
        self._choice['ABSTRACT'] 	= Option('str', u'\\renewcommand\\abstract[1]{\\noindent{\small{\\textbf{Résumé}. }#1}}')
        self._choice['AUTHORS']		= Option('str', '\\renewcommand\\Authfont{\scshape}')

# ----------------------------------------------------------------------------

all_themes = Themes()
all_themes.add_theme(u'basic', ThemeBasic())
all_themes.add_theme(u'palme', ThemePalme())
all_themes.add_theme(u'nalte', ThemeNalte() )

# ----------------------------------------------------------------------------
