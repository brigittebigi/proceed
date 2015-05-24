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


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

import logging
import codecs
import pickle

from wxgui.models.themes import THEMES
from options import Option
from sp_glob import SETTINGS_FILE


# ----------------------------------------------------------------------------
# Class Preferences
# ----------------------------------------------------------------------------


class Preferences:
    """
    @author: Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: This class is used to manage a dictionary of settings.

    """

    def __init__(self, theme=None):
        """
        Constructor.

        Creates a dict of Option() instances, with option id as key.

        """
        self._prefs = {}

        # Set a default theme to assign values in the dictionary.
        if theme is None:
            theme = 0
        self.SetTheme( theme )

    # End __init__
    # ------------------------------------------------------------------------


    # ------------------------------------------------------------------------
    # Getters and Setters
    # ------------------------------------------------------------------------


    def GetValue(self, key):
        """ Return the typed-value of the given key. """

        return self._prefs[key].get_value()

    # End GetValue
    # ------------------------------------------------------------------------


    def SetValue(self, key, t=None, v=None, text=''):
        """ Set a new couple key/(type,typed-value,text). """

        if not key in self._prefs:
            self._prefs[key] = Option(optiontype=t, optionvalue=v, optiontext=text)

        self._prefs[key].set_value(v)

    # End SetValue
    # ------------------------------------------------------------------------


    def SetOption(self, key, option):
        """ Set a new couple key/Option. """

        self._prefs[key] = option

    # End SetOption
    # ------------------------------------------------------------------------


    def GetTheme(self):
        """ Return the index of the current theme. """

        return self._prefs['THEME']

    # End GetTheme
    # ------------------------------------------------------------------------


    def SetTheme(self, idx):
        """ Set a new theme, from the list of themes. """

        logging.debug('Set to theme %d.'%idx)

        try:
            theme = THEMES[idx][1]
            self._prefs['THEME'] = idx
        except Exception,e:
            logging.debug('Set to theme %d failed. Error: %s'%(idx,str(e)))
            return

        for key in theme.get_choices():
            option = theme.get_choice(key)
            if option is not None:
                self.SetOption(key, option)

    # End SetTheme
    # ------------------------------------------------------------------------


# ----------------------------------------------------------------------------


class Preferences_IO( Preferences ):
    """ Input/Output preferences. """

    def __init__(self, filename=None):
        """ Create a new dictionary of preferences. """

        Preferences.__init__(self)

        if not filename:
            self._filename = SETTINGS_FILE
        else:
            self._filename = filename

    # End __init__
    # ------------------------------------------------------------------------


    def Read(self):
        """
        Read user preferences from a file.
        Return True if preferences have been read.
        """

        try:
            with codecs.open(self._filename, mode="r") as f:
                self._prefs = pickle.load(f)
        except Exception, e:
            return False

        return True

    # End Read
    # ------------------------------------------------------------------------


    def Write(self):
        """
        Save user preferences into a file.
        Return True if preferences have been saved.
        """
        try:
            with codecs.open(self._filename, mode="w") as f:
                pickle.dump(self._prefs, f, pickle.HIGHEST_PROTOCOL)
        except Exception, e:
            logging.debug('Preferences NOT saved, error: %s'%str(e))
            return False

        logging.debug('Preferences saved successfully')
        return True

    # End Write
    # ------------------------------------------------------------------------


    def Copy(self):
        """
        Return a deep copy of self.
        """
        #import copy
        #return copy.deepcopy( self._prefs ) -->
        # TypeError: object.__new__(PySwigObject) is not safe, use PySwigObject.__new__()

        p = Preferences_IO()
        d = {}
        for key in self._prefs.keys():
            if key == 'THEME':
                p.SetTheme(self._prefs[key])
            else:
                t = self._prefs[key].get_type()
                v = self._prefs[key].get_untypedvalue()
                txt = self._prefs[key].get_text()
                p.SetOption(key, Option(t,v,txt))

        return p

    # End Copy
    # ------------------------------------------------------------------------

# ----------------------------------------------------------------------------
