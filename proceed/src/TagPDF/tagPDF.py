#!/usr/bin/env python
# -*- coding: utf8 -*-
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
#       Copyright (C) 2013-2018  Brigitte Bigi
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

from genPDF import GenPdfFile
from name import GenName
import utils
import os
import logging

# ---------------------------------------------------------------------------

class tagPdfFile( GenPdfFile ):
    """
    @authors: Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: Class to tag an existing pdf file with a specific header and footer.

    """

    def __init__(self):
        """
        Creates a new tagPdfFile instance.

        """
        GenPdfFile.__init__(self)

    # -------------------------------------------------------------------------

    def tagDir(self, inputname, outputname):
        """ Tag all PDF files of a directory.
        Files are sorted in alpha-numeric order.

        :param inputname: (string) Input directory name (with path).
        :param outputname: (string) Output directory name (with path).

        """
        pdflist = [f for f in sorted(os.listdir(inputname)) if f.lower().endswith(".pdf")]
        pdflistsuccess = list()
        if os.path.exists(outputname) is False:
            os.mkdir(outputname)

        for f in sorted(pdflist):

            inf = os.path.join(inputname,f)
            outf = os.path.join(outputname,f)

            try:
                N = self.tagFile(inf, outf)
                oldN = int(self.get_page_number())
                self.set_page_number(str(oldN + N))
                pdflistsuccess.append(outf)
            except Exception as e:
                logging.info("Error while tagging document {:s}: {:s}"\
                             "".format(inf, str(e)))
                pass

        return pdflistsuccess

    # -------------------------------------------------------------------------

    def tagFile(self, inputname, outputname):
        """ Tag a PDF file.
        This function requires 'pdftk' to be installed.

        @param inputname (string) PDF input file name (including path).
        @param outputname (string) PDF output file name (including path).
        @return The number of pages of the pdf file.

        """
        N = utils.countPages(inputname)
        self.set_number_of_pages(N)

        # Create an empty PDF file, with only the Header and Footer
        fname = os.path.join(os.getcwd(), GenName().get_name())
        self.exportPDF(fname+".pdf")
        
        # Program name:
        # pdftk [pdf-file] background [background-file] output [result-file]
        command = 'pdftk '
        command += '"' + inputname + '" multibackground '
        command += '"' + fname+'.pdf" '
        command += " output "
        command += '"' + outputname + '"'

        ret = utils.run_command(command)

        if len(ret.strip())>0:
            if os.path.exists(outputname):
                os.remove(outputname)
            raise IOError('pdftk failed to tag the file: '+ret)

        if not os.path.exists(outputname):
            raise IOError('File not created.')
        os.remove(fname+".pdf")

        return N
