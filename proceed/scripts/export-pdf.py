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
Import CSV (Documents, Authors, Sessions) and PDF of authors and
export the toc, merge submissions, the program, the list/index of authors.


"""

# ---------------------------------------------------------------------------

import getopt
import logging
from logging import info as loginfo
import sys
import os.path
sys.path.append( os.path.join(os.path.dirname(os.path.dirname( os.path.abspath(__file__))), "src") )

import Manager.models.readers as readers 
from Manager.models.writers import *
from Manager.models.prefs   import Preferences_IO

# ----------------------------------------------------------------------
# USEFUL FUNCTIONS
# ----------------------------------------------------------------------

def usage(output):
    """
    Print the usage of this script on an output.

    @param output is a string representing the output (for example: sys.stdout)

    """
    output.write('export-PDF.py [options] where options are:\n')
    output.write('      -i folder           Input folder (CSV + PDF)        [required] \n')
    output.write('      -S style name       One of: taln-actes, taln-abstracts, simple [default=simple]\n')
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


def findCSV(path,filename):
    """ Get the real filename (with upper/lower). """

    filename = filename.lower()
    for f in os.listdir(path):
        if f.lower() == filename+".csv":
            return f



# ---------------------------------------------------------------------------
# Setup a logger to communicate on the terminal, or a file.
# ---------------------------------------------------------------------------

def setup_logging(log_level, filename):
    """
    Setup default logger to log to stderr or and possible also to a file.

    The default logger is used like this:
        >>> import logging
        >>> logging.error(text message)
    """
    format= "%(asctime)s [%(levelname)s] %(message)s"
    # Setup logging to stderr
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(format))
    console_handler.setLevel(log_level)
    logging.getLogger().addHandler(console_handler)

    # Setup logging to file if filename is specified
    if filename:
        file_handler = logging.FileHandler(filename, "w")
        file_handler.setFormatter(logging.Formatter(format))
        file_handler.setLevel(log_level)
        logging.getLogger().addHandler(file_handler)
    logging.getLogger().setLevel(log_level)
    loginfo("Logging set up with log level=%s, filename=%s", log_level,
            filename)


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

    # Log
    log_level = 0
    log_file  = None
    setup_logging(log_level, log_file)

    # Get options (if any...)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:S:", ["help"])
    except getopt.GetoptError, err:
        # Print help information and exit:
        Quit(message="Error: "+str(err)+".\nUse option --help for any help.\n", status=1)

    dirinput     = None
    stylename    = "simple"

    # Extract options
    for o, a in opts:
        if o == "-i":
            dirinput = a
        elif o == "-S":
            stylename = a
        elif o == "--help": # need help
            Quit(message='Help', status=0, usageoutput=sys.stdout)

    # Verify args

    if dirinput is not None:
        if not os.path.exists(dirinput):
            Quit(message="Error: BAD input file name: "+fileinput+"\n", status=1)
    else:
        Quit(message="Error: an input is required.\n.", status=1, usageoutput=sys.stderr)


    # ----------------------------------------------------------------------
    # Load input data
    # ----------------------------------------------------------------------
    docreader     = readers.documents_csv_reader( os.path.join(dirinput,findCSV(dirinput,"Documents")) )
    sessionreader = readers.sessions_csv_reader( os.path.join(dirinput,findCSV(dirinput,"Sessions") ))
    author_reader = readers.authors_csv_reader( os.path.join(dirinput,findCSV(dirinput,"Authors")) )

    DocDict     = dict()
    SessionDict = dict()
    AuthorDict  = dict()

    for docid in docreader.get_all_ids():

        authorslist = []
        session     = ""
        title       = ""
        rank        = ""
        page_number = ""

        for row in docreader.get_ById(docid):

            author = docreader.get_Author(row)
            if author not in AuthorDict.keys():
                authorslist.append(author)

            if session == "" and docreader.get_Session(row) != "":
                session = docreader.get_Session(row)
                if session not in SessionDict.keys():
                    SessionDict[session.get_sessionid()] = session

            if title == "" and docreader.get_DocTitle(row) != "":
                title = docreader.get_DocTitle(row)

            if rank == "" and docreader.get_Rank(row) != "":
                rank = docreader.get_Rank(row)

            if page_number == "" and docreader.get_NumPage(row) != "":
                page_number = docreader.get_NumPage(row)

        doc = Document(docid, title, authorslist, session, rank, page_number)
        DocDict[doc.get_docid()] = doc

    logging.info( "Number of documents: %d"%len(DocDict.keys()))


    for sessionid in sessionreader.get_AllId():
        session_row = sessionreader.get_ById(sessionid)[0]
        session     = Session(sessionid, sessionreader.get_SessionName(session_row), sessionreader.get_Rank(session_row), sessionreader.get_Date(session_row), sessionreader.get_Heure_Deb(session_row), sessionreader.get_Heure_Fin(session_row), sessionreader.get_Chairman(session_row), sessionreader.get_Location(session_row))
        SessionDict[sessionid] = session

    logging.info( "Number of sessions: %d"%len(SessionDict.keys()))


    for lastname, firstname in author_reader.get_all_names():
        rowList = author_reader.get_ByNames(lastname, firstname)
        a_row = rowList.pop()
        auth = Author(lastname,firstname, author_reader.get_email(a_row), author_reader.get_Affiliation(a_row))
        for row in rowList: ### all the authors which have the same name !!
            Other_auth = Author(lastname,firstname, author_reader.get_email(row), author_reader.get_Affiliation(row))
            auth.compare_and_update(Other_auth)## we use this function because there could be the same other twice in the AUTHORS.csv file, so we merge the information
        AuthorDict[auth.get_authorid()] = auth

    logging.info( "Number of authors: %d"%len(AuthorDict.keys()))


    prefs = Preferences_IO()

    if stylename == 'taln-abstracts':
        prefs.SetTheme(1)
    elif stylename == 'taln-actes':
        prefs.SetTheme(2)
    else:
        prefs.SetTheme(0)


    logging.info( "Create pdf_writer")
    pdfwriter = pdf_writer(None, prefs, DocDict, AuthorDict, SessionDict, dirinput)


    # ----------------------------------------------------------------------
    # Write output data (with default parameters)
    # ----------------------------------------------------------------------

    pdfwriter.run()

    # ----------------------------------------------------------------------
