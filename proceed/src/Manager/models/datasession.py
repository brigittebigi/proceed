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

        self.sessionid    = self.clean(sessionid)
        self.session_name = self.clean(session_name)
        self.rank         = rank
        self.date         = date
        self.h_deb        = h_deb
        self.h_fin        = h_fin
        self.chairman     = self.clean(chairman)
        self.location     = self.clean(location)

    # End __init__
    # -----------------------------------------------------------------------


    def clean(self, entry):
        """
        Clean a string and encode to UTF-8.

        @param entry is the string to clean
        @return a string without special chars

        """
        s = ""
        if isinstance(entry, unicode):
            s = self.__clean(entry)
        elif entry is None:
            s = ""
        else:
            try:
                _unicode = entry.decode("utf-8")
            except UnicodeDecodeError as e:
                raise e
            s = self.__clean(_unicode)
        return s

    def __clean(self, entry):
        """ Clean a unicode string by removing tabs, CR/LF. """
        return " ".join(entry.split())

    # End clean
    # -----------------------------------------------------------------------


    def IsEmpty(self):
        """
        Check if the session id is valid.
        """
        if len(self.sessionid) == 0:
            return True
        return False

    # End IsEmpty
    # -----------------------------------------------------------------------


    def prepare_save(self):

        if isinstance(self.date,date):
            return [{"SESSION_ID":self.sessionid.encode('utf8'), "SESSION_NAME":self.session_name.encode('utf8'), "RANK":str(self.rank), "DATE":self.date.isoformat(), "H-DEB":self.h_deb.encode('utf8'), "H-FIN":self.h_fin.encode('utf8'), "CHAIRMAN":self.chairman.encode('utf8'), "LOCATION":self.location.encode('utf8')}]

        else:
            return [{"SESSION_ID":self.sessionid.encode('utf8'), "SESSION_NAME":self.session_name.encode('utf8'), "RANK":str(self.rank), "DATE":"", "H-DEB":self.h_deb.encode('utf8'), "H-FIN":self.h_fin.encode('utf8'), "CHAIRMAN":self.chairman.encode('utf8'), "LOCATION":self.location.encode('utf8')}]


    # ------------------------------------------------------------------------
    ########## GETTERS ##########
    # ------------------------------------------------------------------------

    def get_sessionid(self):
        return self.sessionid

    def get_session_name(self):
        return self.session_name

    def get_rank(self):
        return self.rank

    def get_date(self):
        return self.date

    def get_h_deb(self):
        return self.h_deb

    def get_h_fin (self):
        return self.h_fin

    def get_chairman(self):
        return self.chairman

    def get_location(self):
        return self.location


    # ------------------------------------------------------------------------
    ########## SETTERS ##########
    # ------------------------------------------------------------------------

    def set_sessionid(self, new_sessionid):
        self.sessionid = new_sessionid

    def set_session_name(self, new_session_name):
        self.session_name = new_session_name

    def set_rank(self, new_rank):
        self.rank = new_rank

    def set_date(self, new_date):
        self.date = new_date

    def set_h_deb(self, new_h_deb):
        self.h_deb = new_h_deb

    def set_h_fin (self, new_h_fin):
        self.h_fin = new_h_fin

    def set_chairman(self, new_chairman):
        self.chairman = new_chairman

    def set_location(self, new_location):
        self.location = new_location

    def set(self, other):
        if not isinstance(other,"Session"):
            return
        self.sessionid    = other.get_sessionid()
        self.session_name = other.get_session_name()
        self.rank         = other.get_rank()
        self.date         = other.get_date()
        self.h_deb        = other.get_h_deb()
        self.h_fin        = other.get_h_fin()
        self.chairman     = other.get_chairman()
        self.location     = other.get_location()

    # ------------------------------------------------------------------------
    # ------------------------------------------------------------------------


    def __eq__(self, other) :
        if not isinstance(other,Session):
            return False
        if(self.sessionid != other.get_sessionid()):
            return False
        return True


    def __ne__(self, other) :
        return not self == other

# ----------------------------------------------------------------------------
