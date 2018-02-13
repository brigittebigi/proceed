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

from utils.commons import clean

# ---------------------------------------------------------------------------


class Author:
    """
    @authors: Bastien Herbaut, Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: Storage class for an author.

    """

    def __init__(self, lastname, firstname, email="", affiliation="" ):
        """
        Create a new Author instance.

        @param lastname (String)
        @param firstname (String)
        @param email (String)
        @param affiliation

        The Author identifier is made by its firstname and its lastname with
        a "join" sequence (some characters).

        """
        self._joinseq     = "--"

        self._lastname    = clean(lastname)
        self._firstname   = clean(firstname)
        self._authorid    = self._lastname + self._joinseq + self._firstname
        self._email       = clean(email)
        self._affiliation = clean(affiliation)

    # End __init__
    # -----------------------------------------------------------------------

    def IsEmpty(self):
        if self._authorid == self._joinseq:
            return True
        return False

    # End IsEmpty
    # -----------------------------------------------------------------------


    def compare_and_update(self,other):
        if self._authorid != other.get_authorid():
            return False
        if(len(self._email) < len(other.get_email())):
            self._email = other.get_email()
        if(len(self._affiliation) < len(other.get_affiliation())):
            self._affiliation = other.get_affiliation()

        return True

    # -----------------------------------------------------------------------

    def prepare_save(self):
        ln = self._lastname
        fn = self._firstname
        m  = self._email
        a  = self._affiliation
        return [{"LASTNAME":ln , "FIRSTNAME":fn, "EMAIL":m, "AFFILIATION":a}]

    # -----------------------------------------------------------------------
    ########## GETTERS ##########
    # -----------------------------------------------------------------------

    def get_authorid(self):
        return self._authorid

    def get_lastname(self):
        return self._lastname

    def get_firstname(self):
        return self._firstname

    def get_email(self):
        return self._email

    def get_affiliation(self):
        return self._affiliation

    def get_joinseq(self):
        return self._joinseq

    # -----------------------------------------------------------------------
    ########## SETTERS ##########
    # -----------------------------------------------------------------------

    def set_lastname(self, new_lastname):
        self._lastname = clean(new_lastname)

    def set_firstname(self, new_firstname):
        self._firstname = clean(new_firstname)

    def set_email(self, new_email):
        self._email = clean(new_email)

    def set_affiliation(self, new_affiliation):
        self._affiliation = clean(new_affiliation)

    def set(self, other):
        self._authorid    = other.get_authorid()
        self._lastname    = other.get_lastname()
        self._firstname   = other.get_firstname()
        self._email       = other.get_email()
        self._affiliation = other.get_affiliation()
        self._joinseq     = other.get_joinseq()

    # -----------------------------------------------------------------------

    def __eq__(self, other) :
        if not isinstance(other,Author):
            return False
        if (self._authorid == other.get_authorid()):
            return True
        return False

    def __ne__(self, other) :
        return not self == other

    # -----------------------------------------------------------------------
