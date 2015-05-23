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

from options import Option

# ----------------------------------------------------------------------------
# Set of THEMES
# ----------------------------------------------------------------------------


class Theme:
    """
    @author: Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: Factory class for a theme, to store all preferences of the user.

    """

    def __init__(self):
        """
        Constructor.

        A Theme is a dictionary with key/option.

        """
        self._choice = {}

    # End __init__
    # -----------------------------------------------------------------------


    def get_choice(self, key):
        """ Return a value from its key. """

        if not key in self._choice.keys():
            return None
        return self._choice[key]

    # End get_choice
    # -----------------------------------------------------------------------


    def get_choices(self):
        """ Return the dictionary with all pairs key/value. """

        return self._choice

    # End get_choice
    # -----------------------------------------------------------------------


# ---------------------------------------------------------------------------


class ThemeDefault(Theme):
    """ Default theme. """

    def __init__(self):

        Theme.__init__(self)

        # Papers: ["a4paper", "letterpaper", "b5paper", "a5paper" ]
        self._choice['PAGE_FORMAT']   = Option('str', 'a4paper')
        self._choice['PAGE_NUMBER']   = Option('int', 1)

        self._choice["TOP_MARGIN"]    = Option('int', 30) # millimeters
        self._choice["BOTTOM_MARGIN"] = Option('int', 20) # millimeters
        self._choice["HEADER_SIZE"]   = Option('int', 20) # pt
        self._choice["FOOTER_SIZE"]   = Option('int', 10) # pt

        self._choice['HEADER_LEFT']   = Option('str', '')
        self._choice['HEADER_CENTER'] = Option('str', '')
        self._choice['HEADER_RIGHT']  = Option('str', '')#\\session')
        self._choice['HEADER_STYLE']  = Option('str', '\\it') # "\\rm","\\it","\\em","\\emph","\\bf","\\sl","\\sf","\\sc","\\tt"
        self._choice['HEADER_COLOR']  = Option('str', '20,20,20')
        self._choice['HEADER_RULER']  = Option('bool', True)

        self._choice['FOOTER_LEFT']   = Option('str', '')
        self._choice['FOOTER_CENTER'] = Option('str', '\\thepage')
        self._choice['FOOTER_RIGHT']  = Option('str', '')
        self._choice['FOOTER_STYLE']  = Option('str', '\\bf') # "\\rm","\\it","\\em","\\emph","\\bf","\\sl","\\sf","\\sc","\\tt"
        self._choice['FOOTER_COLOR']  = Option('str', '20,20,20')
        self._choice['FOOTER_RULER']  = Option('bool', False)

        self._choice['GENERATE_PROGRAM']            = Option('bool', True)
        self._choice['GENERATE_PROGRAM_OVERVIEW']   = Option('bool', True)
        self._choice['GENERATE_TABLEOFCONTENTS']    = Option('bool', True)
        self._choice['GENERATE_MERGED_SUBMISSIONS'] = Option('bool', True)
        self._choice['GENERATE_AUTHORS_INDEX']      = Option('bool', True)
        self._choice['GENERATE_AUTHORS_LIST']       = Option('bool', True)

        self._choice['TITLE_PROGRAM']          = Option('str', 'Program')
        self._choice['TITLE_PROGRAM_OVERVIEW'] = Option('str', 'Program overview')
        self._choice['TITLE_TABLEOFCONTENTS']  = Option('str', 'Table of contents')
        self._choice['TITLE_AUTHORS_INDEX']    = Option('str', 'Author Index')
        self._choice['TITLE_AUTHORS_LIST']     = Option('str', 'List of authors')

        # Sort by session types first (1. keynotes, then 2. orals then 3. posters)
        self._choice['SORT_BY_SESSION_TYPE_FIRST'] = Option('bool', False)


# ---------------------------------------------------------------------------


class ThemeAbstractTALN(Theme):
    """ Default theme. """

    def __init__(self):

        Theme.__init__(self)

        # Papers: ["a4paper", "letterpaper", "b5paper", "a5paper" ]
        self._choice['PAGE_FORMAT']   = Option('str', 'a4paper')
        self._choice['PAGE_NUMBER']   = Option('int', 1)

        self._choice["TOP_MARGIN"]    = Option('int', 25) # millimeters
        self._choice["BOTTOM_MARGIN"] = Option('int', 15) # millimeters
        self._choice["HEADER_SIZE"]   = Option('int', 20) # pt
        self._choice["FOOTER_SIZE"]   = Option('int', 10) # pt

        self._choice['HEADER_LEFT']   = Option('str', u'21\\textsuperscript{\`eme} Traitement Automatique des Langues Naturelles, Marseille, 2014')
        self._choice['HEADER_CENTER'] = Option('str', '')
        self._choice['HEADER_RIGHT']  = Option('str', 'session')
        self._choice['HEADER_STYLE']  = Option('str', '\\it') # "\\rm","\\it","\\em","\\emph","\\bf","\\sl","\\sf","\\sc","\\tt"
        self._choice['HEADER_COLOR']  = Option('str', '30,120,200')
        self._choice['HEADER_RULER']  = Option('bool', True)

        self._choice['FOOTER_LEFT']   = Option('str', '')
        self._choice['FOOTER_CENTER'] = Option('str', '\\thepage')
        self._choice['FOOTER_RIGHT']  = Option('str', '')
        self._choice['FOOTER_STYLE']  = Option('str', '\\bf') # "\\rm","\\it","\\em","\\emph","\\bf","\\sl","\\sf","\\sc","\\tt"
        self._choice['FOOTER_COLOR']  = Option('str', '0,0,150')
        self._choice['FOOTER_RULER']  = Option('bool', False)

        self._choice['GENERATE_PROGRAM']            = Option('bool', True)
        self._choice['GENERATE_PROGRAM_OVERVIEW']   = Option('bool', True)
        self._choice['GENERATE_TABLEOFCONTENTS']    = Option('bool', True)
        self._choice['GENERATE_MERGED_SUBMISSIONS'] = Option('bool', True)
        self._choice['GENERATE_AUTHORS_INDEX']      = Option('bool', True)
        self._choice['GENERATE_AUTHORS_LIST']       = Option('bool', True)

        self._choice['TITLE_PROGRAM']           = Option('str', u'Programme')
        self._choice['TITLE_PROGRAM_OVERVIEW']  = Option('str', u'Panorama')
        self._choice['TITLE_TABLEOFCONTENTS']   = Option('str', u'Table des mati\`eres')
        self._choice['TITLE_AUTHORS_INDEX']     = Option('str', u'Index des auteurs')
        self._choice['TITLE_AUTHORS_LIST']      = Option('str', u'Liste des auteurs')

        # Do not sort by session types first (1. keynotes, then 2. orals then 3. posters)
        self._choice['SORT_BY_SESSION_TYPE_FIRST'] = Option('bool', False)


# ---------------------------------------------------------------------------


class ThemeProceedingsTALN(Theme):
    """ Default theme. """

    def __init__(self):

        Theme.__init__(self)

        # Papers: ["a4paper", "letterpaper", "b5paper", "a5paper" ]
        self._choice['PAGE_FORMAT']   = Option('str', 'a4paper')
        self._choice['PAGE_NUMBER']   = Option('int', 1)

        self._choice["TOP_MARGIN"]    = Option('int', 25) # millimeters
        self._choice["BOTTOM_MARGIN"] = Option('int', 15) # millimeters
        self._choice["HEADER_SIZE"]   = Option('int', 20) # pt
        self._choice["FOOTER_SIZE"]   = Option('int', 10) # pt

        # No header (already in each paper)
        self._choice['HEADER_LEFT']   = Option('str', '')
        self._choice['HEADER_CENTER'] = Option('str', '')
        self._choice['HEADER_RIGHT']  = Option('str', 'session')
        self._choice['HEADER_STYLE']  = Option('str', '\\it') # "\\rm","\\it","\\em","\\emph","\\bf","\\sl","\\sf","\\sc","\\tt"
        self._choice['HEADER_COLOR']  = Option('str', '30,120,200')
        self._choice['HEADER_RULER']  = Option('bool', False)

        # Just page number as footer
        self._choice['FOOTER_LEFT']   = Option('str', '')
        self._choice['FOOTER_CENTER'] = Option('str', '\\thepage')
        self._choice['FOOTER_RIGHT']  = Option('str', '')
        self._choice['FOOTER_STYLE']  = Option('str', '\\bf') # "\\rm","\\it","\\em","\\emph","\\bf","\\sl","\\sf","\\sc","\\tt"
        self._choice['FOOTER_COLOR']  = Option('str', '0,0,150')
        self._choice['FOOTER_RULER']  = Option('bool', False)

        # Export in PDF...
        self._choice['GENERATE_PROGRAM']            = Option('bool', True)
        self._choice['GENERATE_PROGRAM_OVERVIEW']   = Option('bool', True)
        self._choice['GENERATE_TABLEOFCONTENTS']    = Option('bool', True)
        self._choice['GENERATE_MERGED_SUBMISSIONS'] = Option('bool', True)
        self._choice['GENERATE_AUTHORS_INDEX']      = Option('bool', True)
        self._choice['GENERATE_AUTHORS_LIST']       = Option('bool', False)

        self._choice['TITLE_PROGRAM']           = Option('str', u'Programme')
        self._choice['TITLE_PROGRAM_OVERVIEW']  = Option('str', u'Panorama')
        self._choice['TITLE_TABLEOFCONTENTS']   = Option('str', u'Table des mati\`eres')
        self._choice['TITLE_AUTHORS_INDEX']     = Option('str', u'Index des auteurs')
        self._choice['TITLE_AUTHORS_LIST']      = Option('str', u'Liste des auteurs')

        # Sort by session types first (1. keynotes, then 2. orals then 3. posters)
        self._choice['SORT_BY_SESSION_TYPE_FIRST'] = Option('bool', False)


# ----------------------------------------------------------------------------


class ThemeAbstractsLARP(Theme):
    """ Default theme. """

    def __init__(self):

        Theme.__init__(self)

        # Papers: ["a4paper", "letterpaper", "b5paper", "a5paper" ]
        self._choice['PAGE_FORMAT']   = Option('str', 'a4paper')
        self._choice['PAGE_NUMBER']   = Option('int', 1)

        self._choice["TOP_MARGIN"]    = Option('int', 25) # millimeters
        self._choice["BOTTOM_MARGIN"] = Option('int', 15) # millimeters
        self._choice["HEADER_SIZE"]   = Option('int', 20) # pt
        self._choice["FOOTER_SIZE"]   = Option('int', 15) # pt

        # No header (already in each paper)
        self._choice['HEADER_LEFT']   = Option('str', 'LARP7')
        self._choice['HEADER_CENTER'] = Option('str', '3-5 Sep 2014 Aix-en-Provence (France)')
        self._choice['HEADER_RIGHT']  = Option('str', 'session')
        self._choice['HEADER_STYLE']  = Option('str', '\\it') # "\\rm","\\it","\\em","\\emph","\\bf","\\sl","\\sf","\\sc","\\tt"
        self._choice['HEADER_COLOR']  = Option('str', '139,53,49')
        self._choice['HEADER_RULER']  = Option('bool', False)

        # Just page number as footer
        self._choice['FOOTER_LEFT']   = Option('str', '')
        self._choice['FOOTER_CENTER'] = Option('str', '\\thepage')
        self._choice['FOOTER_RIGHT']  = Option('str', '')
        self._choice['FOOTER_STYLE']  = Option('str', '\\bf') # "\\rm","\\it","\\em","\\emph","\\bf","\\sl","\\sf","\\sc","\\tt"
        self._choice['FOOTER_COLOR']  = Option('str', '120,80,60')
        self._choice['FOOTER_RULER']  = Option('bool', False)

        # Export in PDF...
        self._choice['GENERATE_PROGRAM']            = Option('bool', True)
        self._choice['GENERATE_PROGRAM_OVERVIEW']   = Option('bool', True)
        self._choice['GENERATE_TABLEOFCONTENTS']    = Option('bool', True)
        self._choice['GENERATE_MERGED_SUBMISSIONS'] = Option('bool', True)
        self._choice['GENERATE_AUTHORS_INDEX']      = Option('bool', True)
        self._choice['GENERATE_AUTHORS_LIST']       = Option('bool', True)

        self._choice['TITLE_PROGRAM']          = Option('str', 'Program')
        self._choice['TITLE_PROGRAM_OVERVIEW'] = Option('str', 'Program overview')
        self._choice['TITLE_TABLEOFCONTENTS']  = Option('str', 'Table of contents')
        self._choice['TITLE_AUTHORS_INDEX']    = Option('str', 'Author Index')
        self._choice['TITLE_AUTHORS_LIST']     = Option('str', 'List of authors')

        # Sort by session types first (1. keynotes, then 2. orals then 3. posters)
        self._choice['SORT_BY_SESSION_TYPE_FIRST'] = Option('bool', False)


# ----------------------------------------------------------------------------

# Tuples with all available themes:
THEMES = (
            (u"Default",             ThemeDefault() ),
            (u"Abstracts of TALN",   ThemeAbstractTALN() ),
            (u"Proceedings of TALN", ThemeProceedingsTALN() ),
            (u"Proceedings of LARP", ThemeAbstractsLARP() )
        )

# ----------------------------------------------------------------------------
