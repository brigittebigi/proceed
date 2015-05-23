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
        self.joinseq     = "--"

        self.lastname    = self.clean(lastname)
        self.firstname   = self.clean(firstname)
        self.authorid    = self.lastname + self.joinseq + self.firstname
        self.email       = self.clean(email)
        self.affiliation = self.clean(affiliation)

    # End __init__
    # -----------------------------------------------------------------------


    def clean(self, entry):
        """
        Clean a string and encode to UTF-8.

        @param entry is the string to clean
        @return: a string without special chars

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
        if self.authorid == self.joinseq:
            return True
        return False

    # End IsEmpty
    # -----------------------------------------------------------------------


    def compare_and_update(self,other):

        # compare
        if self.authorid != other.get_authorid():
            return False

        # update
        if(len(self.email) < len(other.get_email())):
            self.email = other.get_email()

        if(len(self.affiliation) < len(other.get_affiliation())):
            self.affiliation = other.get_affiliation()

        return True

    # End compare_and_update
    # -----------------------------------------------------------------------


    def prepare_save(self):
        return [{"LASTNAME": self.lastname.encode('utf8'), "FIRSTNAME":self.firstname.encode('utf8'), "EMAIL":self.email.encode('utf8'), "AFFILIATION":self.affiliation.encode('utf8')}]


    # -----------------------------------------------------------------------
    ########## GETTERS ##########
    # -----------------------------------------------------------------------


    def get_authorid(self):
        return self.authorid

    def get_lastname(self):
        return self.lastname

    def get_firstname(self):
        return self.firstname

    def get_email(self):
        return self.email

    def get_affiliation(self):
        return self.affiliation

    def get_joinseq(self):
        return self.joinseq

    # -----------------------------------------------------------------------
    ########## SETTERS ##########
    # -----------------------------------------------------------------------

    def set_lastname(self, new_lastname):
        self.lastname = new_lastname

    def set_firstname(self, new_firstname):
        self.firstname = new_firstname

    def set_email(self, new_email):
        self.email = new_email

    def set_affiliation(self, new_affiliation):
        self.affiliation = new_affiliation

    def set(self, other):
        self.authorid    = other.get_authorid()
        self.lastname    = other.get_lastname()
        self.firstname   = other.get_firstname()
        self.email       = other.get_email()
        self.affiliation = other.get_affiliation()
        self.joinseq     = other.get_joinseq()

    # -----------------------------------------------------------------------
    # -----------------------------------------------------------------------

    def __eq__(self, other) :
        """ Surcharge de == """
        if not isinstance(other,Author):
            return False
        if (self.authorid == other.get_authorid()):
            return True
        return False


    def __ne__(self, other) :
        """ Surcharge de != """
        return not self == other

    # -----------------------------------------------------------------------
