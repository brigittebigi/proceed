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

__docformat__ = "epytext"

"""
Import abstracts from a conference and save them in a directory,
in the form of one latex file per abstract.

Input can be one of sciencesconf XML file or easychair CSV file.

No options for the output style: use default.

"""

# ---------------------------------------------------------------------------

import getopt

import sys
import os.path
sys.path.append( os.path.join(os.path.dirname(os.path.dirname( os.path.abspath(__file__))), "src") )

from DataIO.Read.reader import Reader
from DataIO.Write.writer import Writer
from structs.prefs import Preferences
from structs.abstracts_themes import all_themes

# ----------------------------------------------------------------------
# USEFUL FUNCTIONS
# ----------------------------------------------------------------------

def usage(output):
    """
    Print the usage of this script on an output.

    @param output is a string representing the output (for example: sys.stdout)

    """
    output.write('import-to-tex.py [options] where options are:\n')
    output.write('      -i file             Input file name                 [required] \n')
    output.write('      -a file             Authors Input file name         [required if easychair] \n')
    output.write('      -o output           Output directory                [required] \n')
    output.write('      -s status           Status number (0-4)             [default=1=accepted]\n')
    output.write('      -r reader name      One of: sciencesconf or easychair [default=sciencesconf]\n')
    output.write('      -S style name       One of: basic, palme, nalte     [default=basic]\n')
    output.write('      -c compiler         One of: pdflatex, xetex         [default=pdflatex]\n')
    output.write('      --help              Print this help\n\n')

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

# End Quit
# ----------------------------------------------------------------------


# --------------------------------------------------------------------------
# MAIN PROGRAM
# --------------------------------------------------------------------------

if __name__:

    # ----------------------------------------------------------------------
    # Get all arguments, verify inputs.
    # ----------------------------------------------------------------------

    # Verify the program name and possibly some arguments
    if len(sys.argv) == 1:
        # stop the program and print an error message
        Quit(status=1, usageoutput=sys.stderr)

    # Get options (if any...)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:a:o:s:r:S:c:", ["help"])
    except getopt.GetoptError, err:
        # Print help information and exit:
        Quit(message="Error: "+str(err)+".\nUse option --help for any help.\n", status=1)

    fileinput    = None
    authorsinput = None
    output       = None
    extension    = "tex"
    status       = 1 # only accepted papers
    readername   = "sciencesconf"
    themename    = "basic"
    compiler     = "pdflatex"

    # Extract options
    for o, a in opts:
        if o == "-i":
            fileinput = a
        elif o == "-a":
            authorsinput = a
        elif o == "-o":
            output = a
        elif o == "-s":
            status = int(a)
        elif o == "-r":
            readername = a
        elif o == "-S":
            themename = a
        elif o == "-c":
            compiler = a
        elif o == "--help": # need help
            Quit(message='Help', status=0, usageoutput=sys.stdout)

    # Verify args

    if fileinput is not None:
        if not os.path.exists(fileinput):
            Quit(message="Error: BAD input file name: "+fileinput+"\n", status=1)
    else:
        Quit(message="Error: an input is required.\n.", status=1, usageoutput=sys.stderr)

    if output is None:
        Quit(message="Error: an output is required.\n.", status=1, usageoutput=sys.stderr)

    if readername == "easychair" and not authorsinput:
        Quit(message="With easychair, an input file with authors is required.", status=1, usageoutput=sys.stderr)


    # ----------------------------------------------------------------------
    # Load input data
    # ----------------------------------------------------------------------
    arguments = {}
    arguments['readername'] = readername
    arguments['filename']   = fileinput
    arguments['authorsfilename'] = authorsinput
    arguments['status'] = status

    reader = Reader( arguments )


    # ----------------------------------------------------------------------
    # Write output data (with default parameters)
    # ----------------------------------------------------------------------

    # Create preferences
    prefs = Preferences()
    theme = all_themes.get_theme(themename)
    prefs.SetTheme( theme )
    prefs.SetValue('COMPILER', 'str', compiler.strip())

    # Create the Writer
    writer = Writer( reader.docs )
    writer.set_status( status )

    # Write as LaTeX and proceed native CSV files
    writer.writeLaTeX_as_Dir( output, prefs )
    writer.writeCSV( output )

    # ----------------------------------------------------------------------
