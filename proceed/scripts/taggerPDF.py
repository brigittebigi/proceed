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
# Tag a PDF file, or all files of a directory (in alpha- order),
# with a specific header/footer
# ---------------------------------------------------------------------------

__docformat__ = "epytext"

# ---------------------------------------------------------------------------

import getopt

import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname( os.path.abspath(__file__))), "src"))

from TagPDF.tagPDF import tagPdfFile

# ---------------------------------------------------------------------------


def usage(output):
    """
    Print the usage on an output

    @param output is a string representing the output (for example: sys.stdout)

    """
    output.write('tagPDF.py [options] where options are:\n')
    output.write('      -i input                Input  PDF file name or directory [REQUIRED]\n')
    output.write('      -o output               Output PDF file name or directory [REQUIRED]\n')
    output.write('      -l "left header"        Left Header Text\n')
    output.write('      -c "center header"      Center Header Text \n')
    output.write('      -r "right header"       Right Header Text \n')
    output.write('      -L "left footer"        Left Footer Text \n')
    output.write('      -C "center footer"      Center Footer Text \n')
    output.write('      -R "right footer"       Right Footer Text (Default: \\thepage) \n')
    output.write('      -p "paper"              Paper format\n')
    output.write('      -n number               First page number\n')
    output.write('      -s "style"              Header style\n')
    output.write('      -S "style"              Footer style\n')
    output.write('      -g "R,G,B"              Header color; Red,Green,Blue (Default: "200,200,200") \n')
    output.write('      -G "R,G,B"              Footer colot; Red,Green,Blue (Default: "200,200,200") \n')
    output.write('      --hrule                 Add a rule to separate the header\n')
    output.write('      --frule                 Add a rule to separate the footer\n')
    output.write('      --help                  Print this help\n\n')

# End usage
# ----------------------------------------------------------------------


def Quit(message=None, status=0, usageoutput=None):
    """
    Quit the program with the appropriate exit status.

    @param message is a text to communicate to the user on sys.stderr.
    @param status is an integer of the status exit value.
    @param usageoutput is a file descriptor.

    """
    if message: sys.stderr.write('export.py '+message)
    if usageoutput: usage(usageoutput)
    sys.exit(status)

# ----------------------------------------------------------------------


if __name__ == "__main__":

    # ##################################################################### #
    # Verify and extract args:
    # ##################################################################### #
    # Verify the program name and possibly some arguments
    if len(sys.argv) < 3:
        Quit(message="Usage.", status=1, usageoutput=sys.stderr)

    # Get options (if any...)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "l:c:r:L:C:R:p:n:s:S:g:G:o:i:", ["help", "hrule", "frule"])
    except getopt.GetoptError as err:
        # Print help information and exit:
        Quit(message="Error: "+str(err)+".\nUse option -h for any help.\n", status=1)

    # Create object
    try:
        tagpdf = tagPdfFile()
    except Exception as e:
        Quit(message='Error when creating the LaTeX object: \n'+str(e)+'\n', status=1)

    inputname = None
    outputname = None

    # Extract options
    for o, a in opts:
        try:
            if o == "-l":
                tagpdf.set_left_header(a)
            elif o == "-c":
                tagpdf.set_center_header(a)
            elif o == "-r":
                tagpdf.set_right_header(a)
            elif o == "-L":
                tagpdf.set_left_footer(a)
            elif o == "-C":
                tagpdf.set_center_footer(a)
            elif o == "-R":
                tagpdf.set_right_footer(a)
            elif o == "-p":
                tagpdf.set_paper_format(a)
            elif o == "-n":
                tagpdf.set_page_number(a)
            elif o == "-s":
                tagpdf.set_header_style(a)
            elif o == "-S":
                tagpdf.set_footer_style(a)
            elif o == "--hrule":
                tagpdf.set_header_rule(True)
            elif o == "--frule":
                tagpdf.set_footer_rule(True)
            elif o == "-g":
                tagpdf.set_header_color(a)
            elif o == "-G":
                tagpdf.set_footer_color(a)
            elif o == "-i":
                inputname = a
            elif o == "-o":
                outputname = a
            elif o == "--help":  # need help
                Quit(message='Help', status=0, usageoutput=sys.stdout)
        except Exception as e:
            sys.stderr.write('List of accepted paper formats: \n')
            for i in tagpdf.get_list_paper_format():
                sys.stderr.write("        "+i+"\n")
            sys.stderr.write("\n")
            sys.stderr.write('List of accepted text styles: \n')
            for i in tagpdf.get_list_textstyles():
                sys.stderr.write("        \\"+i+"\n")
            sys.stderr.write("\n")
            Quit(status=1, usageoutput=sys.stderr)

    if inputname is None or outputname is None:
        Quit(status=1, usageoutput=sys.stderr)

    # Now... start to work!

    if os.path.isdir(inputname) is True and \
            (os.path.isdir(outputname) is True or os.path.exists(outputname) is False):
        tagpdf.tagDir(inputname, outputname)

    elif os.path.isdir(inputname) is False and \
            (os.path.isdir(outputname) is False or os.path.exists(outputname) is False):
        tagpdf.tagFile(inputname, outputname)

    else:
        sys.stderr.write("Error. Both input and output must be of the same type (ie: file or dir)\n\n")
        usage(sys.stderr)
        sys.exit(1)
