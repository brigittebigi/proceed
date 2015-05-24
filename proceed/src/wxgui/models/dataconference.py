#!/usr/bin/python
# -*- coding: UTF-8 -*-
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

from utils.commons import clean

# ---------------------------------------------------------------------------

class Conference:
    """
    @authors: Maeva Lauzier, Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: Storage class for a conference.

    """

    def __init__(self, conference_name="", acronym="", place="", date_from="", date_to=""):
        """
        Create a new Conference instance.

        @param conference_name (String)
        @param place (int)
        @param rank (int)
        @param date_to (datetime.date) is the starting day written with isoformat()
        @param date_from (datetime.date) is the ending written with isoformat()

        """

        self._conference_name = clean(conference_name)
        self._acronym         = clean(acronym)
        self._place           = clean(place)
        self._date_from       = clean(date_from)
        self._date_to         = clean(date_to)

    # End __init__
    # -----------------------------------------------------------------------

    def prepare_save(self):
        c = self._conference_name
        a = self._acronym
        p = self._place
        f = self._date_from
        t = self._date_to

        return [{"CONFERENCE_NAME":c, "ACRONYM":a, "PLACE":p, "DATE_FROM":f, "DATE_TO":t}]


    # ------------------------------------------------------------------------
    ########## GETTERS ##########
    # ------------------------------------------------------------------------

    def get_conf_name(self):
        return self._conference_name

    def get_acronym(self):
        return self._acronym

    def get_place(self):
        return self._place

    def get_date_from(self):
        return self._date_from

    def get_date_to(self):
        return self._date_to


    # ------------------------------------------------------------------------
    ########## SETTERS ##########
    # ------------------------------------------------------------------------

    def set_conf_name(self, new_conf_name):
        self._conference_name = clean(new_conf_name)

    def set_acronym(self, a):
        self._acronym = clean(a)

    def set_place(self, new_place):
        self._place = clean(new_place)

    def set_date_from(self, new_date):
        self._date_from = clean(new_date)

    def set_date_to(self, new_date):
        self._date_to = clean(new_date)

    def set(self, other):
        if not isinstance(other,"Conference"):
            return
        self._conference_name = other.get_conf_name()
        self._acronym         = other.get_acronym()
        self._place           = other.get_place()
        self._date_from       = other.get_date_from()
        self._date_to         = other.get_date_to()

    # ------------------------------------------------------------------------
    # ------------------------------------------------------------------------

    def __eq__(self, other) :
        if not isinstance(other,"Conference"):
            return False
        if(self._conference_name != other.get_conference_name()):
            return False
        return True


    def __ne__(self, other) :
        return not self == other

# ----------------------------------------------------------------------------
