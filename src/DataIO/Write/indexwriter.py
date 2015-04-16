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

# ---------------------------------------------------------------------------

class IndexWriter:
    """
    @authors: Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: Write the list of documents with authors, etc.

    """

    def __init__( self, status=1 ):
        self._status = status

    def write( self, docs, filename ):
        try:
            fp = codecs.open ( filename , 'w' , 'utf-8')
        except IOError,e:
            raise e

        for doc in docs:
            if doc.get_status()==self._status:
                for auth in doc.get_authors():
                    fp.write(str(doc.get_docid())+' ; ')
                    fp.write(doc.get_title()+' ; ')
                    fp.write(self.__format(auth.get_lastname())+' ; '+self.__format(auth.get_firstname()) + " ; ")
                    fp.write(self.__format(auth.get_email())+' ; ')

                    for numlabo in auth.get_labos():
                        labo = doc.get_laboratory()[int(numlabo)]
                        fp.write(self.__format(', '.join(labo.get_affiliations())))

                    fp.write(' ; \n')#Le point virgule n'est pas très important pour la decomposition du fichier .idx faite dans le fichier Extract_csv_from_idx.py
                    # cependant cela améliore la lisibilité lorsque des papier ne possédes pas d'affiliations

        fp.close()

    def __format(self,s):
        a = s.replace("_", "\_")
        a = a.replace("%", "\%")
        a = a.replace("&", "\&")
        a = a.replace("\s", " ")
        a = re.sub(u' ', u" ", a, re.UNICODE) # espace insecable
        a = re.sub(u'　', u" ", a, re.UNICODE) # espace insecable version 2!
        a = re.sub(u' ­­', u" ", a, re.UNICODE) # espace insecable version 3!
        return a


#-----------------------------------------------------------------------------
