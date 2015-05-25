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
# File: prefs.py
# ----------------------------------------------------------------------------

__docformat__ = """epytext"""
__authors__   = """Brigitte Bigi"""
__copyright__ = """Copyright (C) 2011-2015  Brigitte Bigi"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

import logging
import codecs
import pickle

from structs.option  import Option

# ----------------------------------------------------------------------------


class Preferences:
    """
    Manage a dictionary with user's preferences.

    @author:  Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: This class is used to manage a dictionary of settings.

    """

    def __init__(self, theme=None):
        """
        Constructor.

        Creates a dict of Option() instances, with option id as key.
        Theme is used to group specifics options.

        """
        self._prefs = {}

        # Set a default theme to assign values in the dictionary.
        if theme is not None:
            self.SetTheme( theme )
        else:
            self._prefs['THEME'] = None

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

    def GetText(self, key):
        """ Return the text describing the given key. """

        return self._prefs[key].get_text()

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
        """ Return the the current theme. """

        return self._prefs.get('THEME', None)

    # End GetTheme
    # ------------------------------------------------------------------------


    def SetTheme(self, theme):
        """ Set a new theme. """

        logging.debug('Set to a new theme.')

        self._prefs['THEME'] = theme
        for key in theme.get_keys():
            opt = theme.get_choice(key)
            if opt is not None:
                self.SetOption(key, opt)

    # End SetTheme
    # ------------------------------------------------------------------------


# ----------------------------------------------------------------------------


class Preferences_IO( Preferences ):
    """
    Input/Output preferences.

    @author: Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL,v3
    @summary: This class is used to manage a file of settings.

    """

    def __init__(self, filename=None):
        """ Create a new dictionary of preferences. """

        Preferences.__init__(self)
        self._filename = filename

        logging.info('Settings file name is: %s'%self._filename)

    # End __init__
    # ------------------------------------------------------------------------


    def HasFilename(self):
        """
        Return True if a file name was defined.
        """

        if self._filename is None: return False
        return True

    # End HasFilename
    # ------------------------------------------------------------------------


    def Read(self):
        """
        Read user preferences from a file.
        Return True if preferences have been read.
        """

        try:
            with codecs.open(self._filename, mode="rb") as f:
                prefs = pickle.load(f)
        except Exception as e:
            logging.debug('Preferences NOT read, error: %s'%str(e))
            return False

        self._prefs = prefs
        logging.debug('Settings read successfully')
        return True

    # End Read
    # ------------------------------------------------------------------------


    def Write(self):
        """
        Save user preferences into a file.
        Return True if preferences have been saved.
        """

        if self._filename is None:
            return False

        try:
            with codecs.open(self._filename, mode="wb") as f:
                pickle.dump(self._prefs, f, pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            logging.debug('Preferences NOT saved, error: %s'%str(e))
            return False

        logging.debug('Settings saved successfully.')
        return True

    # End Write
    # ------------------------------------------------------------------------


    def Copy(self):
        """
        Return a deep copy of self.
        """
        cpref = Preferences_IO()

        for key in self._prefs.keys():
            if key == 'THEME':
                cpref.SetTheme( self._prefs[key] )
            else:
                t   = self._prefs[key].get_type()
                v   = self._prefs[key].get_untypedvalue()
                txt = self._prefs[key].get_text()
                opt = Option(t,v,txt)
                cpref.SetOption(key, opt)

        return cpref

    # End Copy
    # ------------------------------------------------------------------------

# ----------------------------------------------------------------------------
