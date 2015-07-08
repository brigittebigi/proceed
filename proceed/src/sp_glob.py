#!/usr/bin/env python2
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
#       Copyright (C) 2013-2015  Brigitte Bigi
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
# File: sp_glob.py
# ----------------------------------------------------------------------------

import os.path


# ---------------------------------------------------------------------------
# Define the base path of SPPAS sources
# ---------------------------------------------------------------------------

BASE_PATH = os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) )


# ---------------------------------------------------------------------------
# Define all paths (relatively to BASE_SPPAS)
# ---------------------------------------------------------------------------

ICONS_PATH     = os.path.join( BASE_PATH , "etc", "icons" )
SAMPLES_PATH   = os.path.join( os.path.dirname(BASE_PATH), "samples" )
SETTINGS_FILE  = os.path.join(BASE_PATH, "etc", "settings.dump")

# ----------------------------------------------------------------------------
# Data
# ----------------------------------------------------------------------------

PAGESLIST  = ['Conference','Documents','Authors','Sessions']
fieldnames = {}
fieldnames[PAGESLIST[0]] = ["ACRONYM", "CONFERENCE_NAME", "PLACE", "DATE_FROM", "DATE_TO"]
fieldnames[PAGESLIST[1]] = ["DOCID", "TITLE", "LASTNAME", "FIRSTNAME", "SESSION_ID", "RANK", "PAGE_NUMBER", "PDF_DIAGNOSIS"]
fieldnames[PAGESLIST[2]] = ["LASTNAME", "FIRSTNAME", "EMAIL", "AFFILIATION"]
fieldnames[PAGESLIST[3]] = ["SESSION_ID", "SESSION_NAME", "RANK", "DATE", "H-DEB", "H-FIN", "CHAIRMAN", "LOCATION"]

# ---------------------------------------------------------------------------
# Constants: Proceed Information
# ---------------------------------------------------------------------------

author     = "Brigitte Bigi"
contact    = "brigite.bigi@gmail.com"
program    = "Proceed"
version    = "0.4"
copyright  = "Copyright (C) 2013-2015 Brigitte Bigi"
url        = "http://www.lpl-aix.fr/~bigi/proceed/"
brief      = "Proceed generates automatically book of abstracts or proceedings of a conference."
docformat  = "epytext"
license    = "GNU Public License, version 3"
license_text = """
------------------------------------------------------------

By using Proceed, you agree to cite a reference in your publications.
See the documentation to get the list of references, or get the PDF
files in the documentation/references sub-folder.

------------------------------------------------------------

Proceed is free software; you can redistribute
it and/or modify it under the terms of the GNU General Public License as
published by the Free Software Foundation; either version 3 of the License,
or (at your option) any later version.

Proceed is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details. You should have
received a copy of the GNU General Public License along with File Hunter;
if not, write to the Free Software Foundation, Inc., 59 Temple Place,
Suite 330, Boston, MA  02111-1307  USA

------------------------------------------------------------"""
