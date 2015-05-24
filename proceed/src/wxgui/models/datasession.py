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

from datetime import date
from utils.commons import clean

# ---------------------------------------------------------------------------


class Session:
    """
    @authors: Bastien Herbaut, Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: Storage class for a session.

    """

    def __init__(self, sessionid, session_name="", rank=0, date=None, h_deb="", h_fin="", chairman="", location=""):
        """
        Create a new Session instance.

        @param sessionid (String) is a unique value used to identify the session
        @param sesion_name (String)
        @param rank (int)
        @param date (datetime.date) is written with isoformat()
        @param h_deb (String) is the starting time
        @param h_fin (String) is the ending time
        @param chairman (String)
        @param location (String)

        """

        self._sessionid    = clean(sessionid)
        self._session_name = clean(session_name)
        self._rank         = int(rank)
        self._date         = date
        self._h_deb        = clean(h_deb)
        self._h_fin        = clean(h_fin)
        self._chairman     = clean(chairman)
        self._location     = clean(location)

    # End __init__
    # -----------------------------------------------------------------------

    def IsEmpty(self):
        """
        Check if the session id is valid.
        """
        if len(self._sessionid) == 0:
            return True
        return False

    # End IsEmpty
    # -----------------------------------------------------------------------

    def prepare_save(self):

        if isinstance(self._date,date):
            return [{"SESSION_ID":self._sessionid, "SESSION_NAME":self._session_name, "RANK":str(self._rank), "DATE":self._date.isoformat(), "H-DEB":self._h_deb, "H-FIN":self._h_fin, "CHAIRMAN":self._chairman, "LOCATION":self._location}]

        else:
            return [{"SESSION_ID":self._sessionid, "SESSION_NAME":self._session_name, "RANK":str(self._rank), "DATE":"", "H-DEB":self._h_deb, "H-FIN":self._h_fin, "CHAIRMAN":self._chairman, "LOCATION":self._location}]


    # ------------------------------------------------------------------------
    ########## GETTERS ##########
    # ------------------------------------------------------------------------

    def get_sessionid(self):
        return self._sessionid

    def get_session_name(self):
        return self._session_name

    def get_rank(self):
        return self._rank

    def get_date(self):
        return self._date

    def get_h_deb(self):
        return self._h_deb

    def get_h_fin (self):
        return self._h_fin

    def get_chairman(self):
        return self._chairman

    def get_location(self):
        return self._location


    # ------------------------------------------------------------------------
    ########## SETTERS ##########
    # ------------------------------------------------------------------------

    def set_sessionid(self, new_sessionid):
        self._sessionid = new_sessionid

    def set_session_name(self, new_session_name):
        self._session_name = new_session_name

    def set_rank(self, new_rank):
        self._rank = new_rank

    def set_date(self, new_date):
        self._date = new_date

    def set_h_deb(self, new_h_deb):
        self._h_deb = new_h_deb

    def set_h_fin (self, new_h_fin):
        self._h_fin = new_h_fin

    def set_chairman(self, new_chairman):
        self._chairman = new_chairman

    def set_location(self, new_location):
        self._location = new_location

    def set(self, other):
        if not isinstance(other,"Session"):
            return
        self._sessionid    = other.get_sessionid()
        self._session_name = other.get_session_name()
        self._rank         = other.get_rank()
        self._date         = other.get_date()
        self._h_deb        = other.get_h_deb()
        self._h_fin        = other.get_h_fin()
        self._chairman     = other.get_chairman()
        self._location     = other.get_location()

    # ------------------------------------------------------------------------
    # ------------------------------------------------------------------------


    def __eq__(self, other) :
        if not isinstance(other,Session):
            return False
        if(self._sessionid != other.get_sessionid()):
            return False
        return True


    def __ne__(self, other) :
        return not self == other

# ----------------------------------------------------------------------------
