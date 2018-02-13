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

import codecs
import re
import string
import random

# ---------------------------------------------------------------------------

class HTMLWriter:
    """
    @authors: Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: Write the list of documents in an HTML document.

    """

    def __init__( self, status=1 ):
        self._status = status


    def write_as_list( self, docs, filename ):
        try:
            fp = codecs.open ( filename , 'w' , 'utf-8')
        except IOError,e:
            raise e

        self.__write_header(fp)
        fp.write('  <UL>\n')
        for doc in docs:
            if doc.get_status()==self._status:
                fp.write('    <LI>\n')
                self.__write_authors(fp,doc)
                self.__write_title(fp,doc.get_title())
                abstract = doc.get_abstract()
                if len(abstract) > 0:
                    self.__write_abstract(fp,abstract)
                fp.write('    </LI>\n')
        fp.write('  </UL>\n')
        self.__write_footer(fp)
        fp.close()


    def __write_header(self,fp):
        fp.write('<HTML>\n\n')
        fp.write('<HEAD>\n\n')
        fp.write('    <meta http-equiv="content-type" content="text/html; charset=UTF-8"> \n')
        fp.write('    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"> \n')
        fp.write('    <meta content="all" name="robots"> \n')
        fp.write('    <script language="javascript" type="text/javascript"> \n')
        fp.write('      function showAndHide(theId) \n')
        fp.write('      { \n')
        fp.write('        var el = document.getElementById(theId); \n')
        fp.write('        var link = document.getElementById("moreLink"); \n')
        fp.write('       if (el.style.display=="none")  \n')
        fp.write('       { \n')
        fp.write('         el.style.display="block"; //show element \n')
        fp.write('           link.innerHTML = "Hide Links..."; \n')
        fp.write('       } \n')
        fp.write('       else \n')
        fp.write('       { \n')
        fp.write('         el.style.display="none"; //hide element \n')
        fp.write('          link.innerHTML = "More..."; \n')
        fp.write('       } \n')
        fp.write('       return false; \n')
        fp.write('     } \n')
        fp.write('    </script> \n\n')
        fp.write('    <style type="text/css"> \n')
        fp.write('    .authors { \n')
        fp.write('        font-variant:small-caps; }\n')
        fp.write('    .title { \n')
        fp.write('        font-weight: bold; }\n')
        fp.write('    .abstractlink { \n')
        fp.write('        font-weight: bold; }\n')
        fp.write('    .abstract { \n')
        fp.write('        margin-left:   40px; \n')
        fp.write('        margin-right:  20px; \n')
        fp.write('        padding-left:   20px; \n')
        fp.write('        padding-right:  10px; \n')
        fp.write('        text-align:    justify; \n')
        fp.write('        border-radius: 10px;\n')
        fp.write('        background-color: rgb(200,220,240); }\n')
        fp.write('    </style> \n')
        fp.write('</HEAD>\n\n')
        fp.write('<BODY>\n')


    def __write_footer(self,fp):
        fp.write('</BODY>\n')
        fp.write('</HTML>\n')


    def __write_title(self,fp,title): # title is a string
        fp.write('<span class="title"> ')
        fp.write(unicode(self.__format(title)))
        fp.write('</span> ')


    def __write_authors(self,fp,doc): # authors is a list of authors instances
        fp.write('<span class="authors"> ')
        for auth in doc.get_authors():
            fp.write(self.__format(auth.get_firstname())+' '+self.__format(auth.get_middlename())+' '+self.__format(auth.get_lastname())+', ')
        fp.write('</span> ')


    def __write_abstract(self,fp,abstract):
        absname=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        fp.write('<a class="abstractlink" href="" onMouseOver="return showAndHide(\''+absname+'\')" onMouseOut="return showAndHide(\''+absname+'\')"> \n')
        fp.write(' >> \n')
        fp.write('</a> \n')
        fp.write('<div class="abstract" id="'+absname+'" style="display:none"> \n')
        fp.write('  <span> \n')
        fp.write('    <div id="abstract"> \n')
        fp.write( abstract + '\n')
        fp.write('        </div> \n')
        fp.write('        </span> \n')
        fp.write('        </div> \n')


    def __format(self,s):
        a = s
        a = a.replace("&", "&amp;")
        a = a.replace("\s", "&nbsp;")
        a = a.replace(u"é", "&eacute;")
        a = a.replace(u"è", "&egrave;")
        a = a.replace(u"à", "&agrave;")
        a = re.sub(u' ', u" ", a, re.UNICODE) # espace insecable
        a = re.sub(u'　', u" ", a, re.UNICODE) # espace insecable version 2!
        a = re.sub(u' ­­', u" ", a, re.UNICODE) # espace insecable version 3!
        return a

# End HTMLWriter
#-----------------------------------------------------------------------------

