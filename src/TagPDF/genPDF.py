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

import os
import os.path
import sys
import getopt
import logging

from genLaTeX import GenLaTeXFile
from name import GenName
import utils

# ---------------------------------------------------------------------------


class GenPdfFile( GenLaTeXFile ):
    """
    @authors: Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: Class to generate an empty latex file.

    Represents a class to generate an empty pdf file.
    An header and a footer can be specified.

    """

    def __init__(self):
        """
        Creates a new GenPdfFile instance.
        """
        GenLaTeXFile.__init__(self)

    # End __init__
    # -------------------------------------------------------------------------


    def exportPDF(self, filename):
        """
        Creates a PDF file.

        @param filename (string) Output file name.

        This functions requires 'pdflatex' to be installed.

        """
        # Create a temporary LaTeX file
        fname = os.path.join(os.getcwd(), GenName().get_name())
        self.exportLaTeX(fname+".tex")

        # Execute pdflatex to convert to pdf
        command = 'pdflatex -halt-on-error -interaction nonstopmode '
        command += '"' + fname+'.tex" '

        ret = utils.run_command( command ) # first compilation
        ret = utils.run_command( command ) # second compilation

        if not len(ret):
            logging.debug(ret)
            raise IOError('Error while executing run_command. Does pdflatex installed properly?')

        # Manage output
        if os.path.exists(fname+".pdf"):
            os.rename(fname+".pdf", filename)
            os.rename(fname+".tex", filename[:-4]+".tex")
        else:
            raise IOError('Error: pdflatex produced no output with command: %s'%command)

        for f in os.listdir(os.getcwd()):
            if os.path.basename(fname) in f and not f.endswith(".tex"):
                os.remove(f)

    # End exportPDF
    # -------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Main program to be used inline
# ---------------------------------------------------------------------------

def usage(output):
    """
    Print the usage on an output

    @param output is a string representing the output (for example: sys.stdout)

    """
    output.write('genPdf.py [options] where options are:\n')
    output.write('      -o outputfile           Output file name [REQUIRED] \n')
    output.write('      -l "left header"        Left Header Text\n')
    output.write('      -c "center header"      Center Header Text \n')
    output.write('      -r "right header"       Right Header Text \n')
    output.write('      -L "left footer"        Left Footer Text \n')
    output.write('      -C "center footer"      Center Footer Text \n')
    output.write('      -R "right footer"       Right Footer Text (Default: \\thepage) \n')
    output.write('      -p "paper"              Paper format\n')
    output.write('      -n number               First page number\n')
    output.write('      -N number               Number of pages\n')
    output.write('      -s "style"              Header style\n')
    output.write('      -S "style"              Footer style\n')
    output.write('      -g "R,G,B"              Header color; Red,Green,Blue (Default: "100,100,100") \n')
    output.write('      -G "R,G,B"              Footer colot; Red,Green,Blue (Default: "100,100,100") \n')
    output.write('      --hrule                 Add a rule to separate the header\n')
    output.write('      --frule                 Add a rule to separate the footer\n')
    output.write('      --help                  Print this help\n\n')


# End usage
# ----------------------------------------------------------------------


def Quit(message, status):
    """
    Quit the program with the appropriate status.

    @param message is a text to communicate to the user on sys.stderr.
    @param status is an integer of the status exit value

    """
    sys.stderr.write('genPDF.py '+message)
    sys.exit(status)

# End Quit
# ----------------------------------------------------------------------

if __name__ == "__main__":
    # Example of use:
    #   python genPDF.py
    #       -l "left header"
    #       -c "center header"
    #       -r "right header"
    #       -L "left footer"
    #       -C "center footer"
    #       -R "\\thepage"
    #       -p "letterpaper"
    #       -n 4
    #       -N 2
    #       -s "\\emph"
    #       -S "\\bf"
    #       -g "255,150,50"
    #       -G "150,250,50"
    #       --hrule
    #       -o outputfile

    # -------------------------------------------------------------------------
    # Verify and extract args:
    # -------------------------------------------------------------------------

    # Verify the program name and possibly some arguments
    if len(sys.argv) == 1:
        # stop the program and print an error message
        usage(sys.stderr)
        sys.exit(1)

    # Get options (if any...)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "l:c:r:L:C:R:p:n:N:s:S:g:G:o:", ["help","hrule","frule"])
    except getopt.GetoptError, err:
        # Print help information and exit:
        Quit("Error: "+str(err)+".\nUse option --help for any help.\n", 1)

    # Create Object
    try:
        pdffile = GenPdfFile()
    except Exception, e:
        Quit('Error when creating the PDF object: \n'+str(e)+'\n', 1)

    filename = None
    # Extract options
    for o,a in opts:
        try:
            if o == "-l":
                pdffile.set_left_header(a)
            elif o == "-c":
                pdffile.set_center_header(a)
            elif o == "-r":
                pdffile.set_right_header(a)
            elif o == "-L":
                pdffile.set_left_footer(a)
            elif o == "-C":
                pdffile.set_center_footer(a)
            elif o == "-R":
                pdffile.set_right_footer(a)
            elif o == "-p":
                pdffile.set_paper_format(a)
            elif o == "-n":
                pdffile.set_page_number(a)
            elif o == "-N":
                pdffile.set_number_of_pages(a)
            elif o == "-s":
                pdffile.set_header_style(a)
            elif o == "-S":
                pdffile.set_footer_style(a)
            elif o == "-g":
                pdffile.set_header_color(a)
            elif o == "-G":
                pdffile.set_footer_color(a)
            elif o == "-o":
                filename = a
            elif o == "--hrule":
                pdffile.set_header_rule(True)
            elif o == "--frule":
                pdffile.set_footer_rule(True)
            elif o == "--help": # need help
                print 'Help'
                usage(sys.stdout)
                sys.exit()
        except Exception,e:
            usage(sys.stderr)
            sys.stderr.write('List of accepted paper formats: \n')
            for i in pdffile.get_list_paper_format():
                sys.stderr.write("        "+i+"\n")
            sys.stderr.write("\n")
            sys.stderr.write('List of accepted text styles: \n')
            for i in pdffile.get_list_textstyles():
                sys.stderr.write("        \\"+i+"\n")
            sys.stderr.write("\n")
            sys.exit(1)

    if filename is None:
        usage(sys.stderr)
        sys.exit(1)

    # -------------------------------------------------------------------------
    # Now... do the job!
    pdffile.exportPDF(filename)

# ----------------------------------------------------------------------
