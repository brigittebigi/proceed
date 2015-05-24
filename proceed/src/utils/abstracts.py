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
# ---------------------------------------------------------------------------

import re
from HTMLParser import HTMLParser

# ---------------------------------------------------------------------------

# create a subclass and override the handler methods
class HTMLCleaner( HTMLParser ):
    """
    Override HTMLParser to store the data content as an HTML cleaner.
    """
    def __init__(self):
        HTMLParser.__init__(self)
        self.intag=False
        self.mydata = ""

    def handle_starttag(self, tag, attrs):
        self.intag=True

    def handle_endtag(self, tag):
        self.intag=False

    def handle_data(self, data):
        self.mydata = self.mydata + data

    def get_data(self):
        return self.mydata

# ---------------------------------------------------------------------------

def html_to_tex(abstract):
    a = abstract
    a = re.sub(u'<p align=["\s\w\xaa-\xff]+>', ur' ', a, re.UNICODE)
    a = re.sub(u"<[\s]*p[\s]*>", "\n", a, re.UNICODE)
    a = re.sub(u"<[\s]/[\s]p[\s]>", "\n\n", a, re.UNICODE)
    a = re.sub(u"<ol>", "\n\\begin{enumerate}\n", a, re.UNICODE)
    a = re.sub(u"<[\s]*/[\s]*ol>", "\n\\end{enumerate}\n", a, re.UNICODE)
    a = re.sub(u"<li>", "\n\\begin{itemize} \n\\item ", a, re.UNICODE)
    a = re.sub(u"<[\s]*/[\s]*li>", "\n\\end{itemize}", a, re.UNICODE)
    a = re.sub(u"<i>", "{\it ", a, re.UNICODE)
    a = re.sub(u"<[\s]*/[\s]*i>", "}", a, re.UNICODE)
    a = re.sub(u"<b>", "{\\bf ", a, re.UNICODE)
    a = re.sub(u"<[\s]*/[\s]*b>", "}", a, re.UNICODE)
    a = re.sub(u"<strong>", "{\\em ", a, re.UNICODE)
    a = re.sub(u"<[\s]*/[\s]*strong>", "}", a, re.UNICODE)
    a = re.sub(u"<br[\s]*/>", "\n", a, re.UNICODE)
    a = re.sub(u"<ul>", '', a, re.UNICODE)
    return a

# ---------------------------------------------------------------------------
