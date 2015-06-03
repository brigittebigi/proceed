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
import string
from HTMLParser import HTMLParser

import unicode_tex

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

def html_to_mytags(abstract):
    a = abstract
    a = re.sub(u'<p align=["\s\w\xaa-\xff]+>', ur'\n\n', a, re.UNICODE)
    a = re.sub(u"<[\s]*p[\s]*>", "\n\n", a, re.UNICODE)
    a = re.sub(u"<[\s]/[\s]p[\s]>", "\n\n", a, re.UNICODE)
    a = re.sub(u"<br[\s]*/>", "\n\n", a, re.UNICODE)
    a = re.sub(u"<li>", "\n BEGINITEMIZE\n    ITEMITEM ", a, re.UNICODE)
    a = re.sub(u"<[\s]*/[\s]*li>", "\n ENDITEMIZE\n", a, re.UNICODE)
    a = re.sub(u"<i>", "BEGINITALIC", a, re.UNICODE)
    a = re.sub(u"<[\s]*/[\s]*i>", "ENDITALIC", a, re.UNICODE)
    a = re.sub(u"<b>", "BEGINBOLD", a, re.UNICODE)
    a = re.sub(u"<[\s]*/[\s]*b>", "ENDBOLD", a, re.UNICODE)
    a = re.sub(u"<strong>", "BEGINSTRONG", a, re.UNICODE)
    a = re.sub(u"<[\s]*/[\s]*strong>", "ENDSTRONG", a, re.UNICODE)
    return a

def mytags_to_tex(abstract):
    a = abstract
    a = re.sub(u"BEGINENUMERATE", '\\begin{enumerate}', a, re.UNICODE)
    a = re.sub(u"ENDENUMERATE",   '\\end{enumerate}',   a, re.UNICODE)
    a = re.sub(u"BEGINITEMIZE",   '\\begin{itemize}',   a, re.UNICODE)
    a = re.sub(u"ENDITEMIZE",     '\\end{itemize}',     a, re.UNICODE)
    a = re.sub(u"ITEMITEM",       '\\item', a, re.UNICODE)
    a = re.sub(u"BEGINITALIC",    '{\\it ', a, re.UNICODE)
    a = re.sub(u"ENDITALIC",      '}', a, re.UNICODE)
    a = re.sub(u"BEGINBOLD",      '{\\bf ', a, re.UNICODE)
    a = re.sub(u"ENDBOLD",        '}', a, re.UNICODE)
    a = re.sub(u"BEGINSTRONG",    '{\\em ', a, re.UNICODE)
    a = re.sub(u"ENDSTRONG",      '}', a, re.UNICODE)

    return a

# ---------------------------------------------------------------------------


def unicode_to_tex_old_version(abstract):
    a = abstract
    a = re.sub(u' ', u" ", a, re.UNICODE)   # espace insecable
    a = re.sub(u'　', u" ", a, re.UNICODE)   # espace insecable version 2!
    a = re.sub(u' ­­', u" ", a, re.UNICODE) # espace insecable version 3!
    a = re.sub(u"ʼ", u"'", a, re.UNICODE)   # apostrophe
    a = re.sub(u"‘", u"'", a, re.UNICODE)   # apostrophe
    a = re.sub(u"É", u"\\'e", a, re.UNICODE)   #
    a = re.sub(u"é", u"\\'e", a, re.UNICODE)   #
    a = re.sub(u"è", u"\\`e", a, re.UNICODE)   #
    a = re.sub(u"ë", u'\\"e', a, re.UNICODE)   #
    a = re.sub(u"ê", u"\\^e", a, re.UNICODE)   #
    a = re.sub(u"à", u"\\`a", a, re.UNICODE)   #
    a = re.sub(u"â", u"\\^a", a, re.UNICODE)   #
    a = re.sub(u"ã", u"\\~a", a, re.UNICODE)   #
    a = re.sub(u"î", u"\\^i", a, re.UNICODE)   #
    a = re.sub(u"ï", u'\\"i', a, re.UNICODE)   #
    a = re.sub(u"í", u"\\'i", a, re.UNICODE)
    a = re.sub(u"ù", u"\\`u", a, re.UNICODE)   #
    a = re.sub(u"ü", u'\\"u', a, re.UNICODE)
    a = re.sub(u"ú", u"\\'u", a, re.UNICODE)
    a = re.sub(u"ç", u"\\c{c}", a, re.UNICODE)   #
    a = re.sub(u"ô", u"\\^o", a, re.UNICODE)   #
    a = re.sub(u"ó", u"\\'o", a, re.UNICODE)

    a = re.sub(u"–", u"-", a, re.UNICODE)
    a = re.sub(u"’", u"'", a, re.UNICODE)   # apostrophe
    a = re.sub(u"ˈ", "'", a, re.UNICODE)
    a = re.sub(u'´', "'", a, re.UNICODE)

    a = re.sub(u"é", u"\\'e", a, re.UNICODE)
    a = re.sub(u"è", u"\\`e", a, re.UNICODE)
    a = re.sub(u"à", u"\\`a", a, re.UNICODE)
    a = re.sub(u"ã", u"\\~a", a, re.UNICODE)
    a = re.sub(u"û", u"\\^u", a, re.UNICODE)
    a = re.sub(u"ú", u"\\'u", a, re.UNICODE)
    a = re.sub(u"â", u"\\^a", a, re.UNICODE)
    a = re.sub(u"á", u"\\'a", a, re.UNICODE)
    a = re.sub(u"ç", u"\\c{c}", a, re.UNICODE)   #
    a = a.replace(u'≤', '$\leq$')
    a = a.replace(u'‐', '--')
    a = a.replace(u'ﬂ', 'fl')
    a = a.replace(u'í', "\\'i")

    a = a.replace(u'η', "$\eta$") # grec

    a = a.replace(u'ɛ̃','\\textipa{\~E}')
    a = a.replace(u'ɑ̃','\\textipa{\~A}')
    a = a.replace(u'ɐ̃','\\textipa{\~5}')
    a = a.replace(u'Ā', '\\textipa{\=A}')
    a = a.replace(u'Ē', '\\textipa{\=E}')
    a = a.replace(u'Ī', '\\textipa{\=I}')
    a = a.replace(u'Ō', '\\textipa{\=O}')
    a = a.replace(u'Ū', '\\textipa{\=U}')
    a = a.replace(u'Ă', '\\textipa{\\v{A}}')
    a = a.replace(u'Ĕ', '\\textipa{\\v{E}}')
    a = a.replace(u'Ĭ', '\\textipa{\\v{I}}')
    a = a.replace(u'Ŏ', '\\textipa{\\v{O}}')
    a = a.replace(u'Ŭ', '\\textipa{\\v{U}}')
    a = a.replace(u'Ṽ','\\~V')
    a = a.replace(u'i͂','\\~i')
    a = a.replace(u'w̃','\\~w')
    a = a.replace(u'j̃','\\~j')

    a = a.replace(u'ɨ', "\\textipa{1}") # IPA
    a = a.replace(u'ʃ','\\textipa{S}')
    a = a.replace(u'ʝ','\\textipa{J}')
    a = a.replace(u'ɛ','\\textipa{E}')
    a = a.replace(u'æ','\\textipa{\\ae}')
    a = a.replace(u'ɾ','\\textipa{R}')
    a = a.replace(u'ɹ','\\textipa{\*r}')
    a = a.replace(u'ɻ','\\textipa{\:r}')
    a = a.replace(u'ʎ','\\textipa{L}')
    a = a.replace(u'ə','\\textipa{@}')
    a = a.replace(u'ɑ','\\textipa{A}')
    a = a.replace(u'ɔ','\\textipa{O}')
    a = a.replace(u'ʒ','\\textipa{Z}')
    a = a.replace(u'ʀ','\\textipa{\;R}')
    a = a.replace(u'ʁ','\\textipa{K}')
    a = a.replace(u'ʔ','\\textipa{P}')
    a = a.replace(u'ø','\\textipa{\o}')

    return a

# ---------------------------------------------------------------------------
