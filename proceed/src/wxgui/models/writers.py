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
# Imports
# ---------------------------------------------------------------------------

import re
import os.path
import wx
import logging
from threading import Thread

from TagPDF.tagPDF  import tagPdfFile
import TagPDF.utils as utils

from wxgui.models.datadocument import Document
from wxgui.models.dataauthor   import Author
from wxgui.models.datasession  import Session
from wxgui.models.validate     import Validate

from utils.unicode_tex import unicode_to_tex, specialchars_to_tex, unicode_to_texipa

# ---------------------------------------------------------------------------
# Define notification event for thread completion
# ---------------------------------------------------------------------------

EVT_RESULT_ID = wx.NewId()


def EVT_RESULT(win, func):
    """ Define Result Event. """
    win.Connect(-1, -1, EVT_RESULT_ID, func)


class ResultEvent(wx.PyEvent):
    """ Simple event to carry result data. """

    def __init__(self, text, num, percent=None):
        """Init Result Event."""

        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.tasktext = text
        self.tasknum  = num
        self.taskpercent = percent

# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Class
# ---------------------------------------------------------------------------

class pdf_writer( Thread ):
    """
    @authors: Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: Used to export data in a PDF document.

    """

    def __init__(self, notify_window, prefs, conference, documents, authors, sessions, path):
        """
        Init Worker Thread Class.
        """
        Thread.__init__(self)
        self._notify_window = notify_window

        # Members
        self._prefsIO  = prefs
        self.validator = Validate( documents, authors, sessions )
        self.conference = conference
        self.documents = documents
        self.authors   = authors
        self.sessions  = sessions
        self.path      = path
        self._initialize()

        # This starts the thread running on creation, but you could
        # also make the GUI thread responsible for calling this
        #self.start()

    # End __init__
    # ------------------------------------------------------------------------


    def _initialize(self):
        # Members for task progress
        self.tasktext    = ''
        self.tasknum     = -1
        self._want_abort = 0

        # Members for processing data
        self.nbpages = 1           # First page number
        self.sortedsessions = list()
        self.sorteddocs     = list()

    # End _initialize
    # ------------------------------------------------------------------------


    # ------------------------------------------------------------------------
    # Threading
    # ------------------------------------------------------------------------


    def abort(self):
        """ Abort worker thread. """
        # Method for use by main thread to signal an abort

        self._want_abort = 1

    # End abort
    # -----------------------------------------------------------------------


    def run(self):
        """ Run Worker Thread. """
        # Method for use by main thread to make the job.

        logging.info('Generate: Start.')

        self._initialize()
        if self.check() is False:
            wx.PostEvent(self._notify_window, ResultEvent(text='Data are not completed. Please check them before exporting.', num=-1))
            logging.info('Data are not completed. Please check them before exporting.')
            return

        self.sort_documents( sortbytype=self._prefsIO.GetValue('SORT_BY_SESSION_TYPE_FIRST') )

        if self._prefsIO.GetValue('GENERATE_MERGED_SUBMISSIONS') is True:
            logging.info('     Add header/footer to each submission')
            self.run_tag_pdf()

        if self._prefsIO.GetValue('GENERATE_MERGED_SUBMISSIONS') is True:
            logging.info('     Merge all submissions')
            self.run_merge_pdf()

        if self._prefsIO.GetValue('GENERATE_TABLEOFCONTENTS') is True:
            logging.info('     Generate Table of content')
            self.run_toc( self._prefsIO.GetValue('TITLE_TABLEOFCONTENTS') )

        if self._prefsIO.GetValue('GENERATE_AUTHORS_INDEX') is True:
            logging.info('     Generate Index of authors')
            self.run_index_authors( self._prefsIO.GetValue('TITLE_AUTHORS_INDEX') )

        if self._prefsIO.GetValue('GENERATE_AUTHORS_LIST') is True:
            logging.info('     Generate List of authors')
            self.run_list_authors( self._prefsIO.GetValue('TITLE_AUTHORS_LIST') )

        if self._prefsIO.GetValue('GENERATE_PROGRAM') is True:
            logging.info('     Generate the Program')
            self.run_program( self._prefsIO.GetValue('TITLE_PROGRAM') )

        if self._prefsIO.GetValue('GENERATE_PROGRAM_OVERVIEW') is True:
            logging.info('     Generate the Program Overview')
            self.run_short_program( self._prefsIO.GetValue('TITLE_PROGRAM_OVERVIEW') )

        logging.info('Generate: Finished.')
        self._initialize()
        wx.PostEvent(self._notify_window, ResultEvent(text=self.tasktext, num=self.tasknum))

    # End run
    # -----------------------------------------------------------------------


    # -----------------------------------------------------------------------
    # OK... Work is done here:
    # -----------------------------------------------------------------------


    def check(self):
        """
        Check if data are ready to be exported in PDF.
        """

        if self._prefsIO.GetValue('GENERATE_MERGED_SUBMISSIONS') is True:
            if len(self.validator.pdffiles(self.path)) > 0:
                return False
            if len(self.validator.name_in_sessions()) > 0:
                return False
            return True
        return True

    # End check
    # -----------------------------------------------------------------------

    def run_tag_pdf(self):
        """ Tag all PDF files with an header and a footer.

        """
        if not len(self.sorteddocs):
            return

        self.tasktext = 'Add header/footer to PDF files.'
        self.tasknum = 0

        count = 0
        while count < len(self.sorteddocs):

            docid = self.sorteddocs[count]
            self.tasktext = 'Add header/footer to docid '+docid
            wx.PostEvent(self._notify_window, ResultEvent(text=self.tasktext, num=self.tasknum))

            # Create and customize the PDF tagger
            tagpdf = self._create_tagpdf()
            self.__set_session_in_tag(tagpdf, docid)
            self.__set_page_in_tag(tagpdf)
            self.__set_conference_in_tag(tagpdf)

            inputname = os.path.join(self.path, docid + ".pdf")
            outputname = os.path.join(self.path, docid + "-tag.pdf")
            s = self.__get_sessionid_and_rank(docid)
            s = "Paper_" + s[1:-1] + ".pdf"
            outputname2 = os.path.join(self.path,s)

            logging.info('     ... tag: %s --> %s' % (docid, s))
            try:
                N = int(tagpdf.tagFile(inputname, outputname))
                tagpdf.tagFile(inputname, outputname2)
                self.documents[docid].set_pdf_diagnosis(0)
            except Exception as e:
                self._initialize()
                logging.info('     ... ... ERROR for doc %s: %s' % (docid, str(e)))
                wx.PostEvent(self._notify_window, ResultEvent(text='PDF export failed for doc '+docid+'. Error: '+str(e), num=-1))
                self.documents[docid].set_pdf_diagnosis(1)
                #return

            oldN = int(tagpdf.get_page_number())
            self.nbpages = N + oldN
            tagpdf.set_page_number(str(self.nbpages))
            self.documents[docid].set_page(oldN)
            count = count + 1

            if self._want_abort:
            # Use a result of None to acknowledge the abort (of
            # course you can use whatever you'd like or even
            # a separate event type)
                wx.PostEvent(self._notify_window, ResultEvent(text=None, num=-1))
                return
            else:
                wx.PostEvent(self._notify_window, ResultEvent(text=self.tasktext, num=self.tasknum, percent=100.*float(count)/float(len(self.sorteddocs))))

    # End run_tag_pdf
    # -----------------------------------------------------------------------

    def run_merge_pdf(self):
        """
        Merge submission files with: pdftk src1.pdf src2.pdf output res.pdf.

        Try to get tagged PDF files. If no tag file is existing, use the
        original PDF file.

        """
        if not len(self.sortedsessions):
            return

        self.tasktext = 'Merge all tagged submissions.'
        self.tasknum += 1
        wx.PostEvent(self._notify_window, ResultEvent(text=self.tasktext, num=self.tasknum))

        try:
            command = 'pdftk '
            for session in self.sortedsessions:
                for c in range(len(self.sorteddocs)):
                    doc = self.documents[self.sorteddocs[c]]
                    if doc.get_session() != session:
                        continue

                    filename = os.path.join(self.path, self.sorteddocs[c] + "-tag.pdf")
                    if os.path.exists(filename):
                        command = command + '"' + filename + '" '
                    else:
                        filename = os.path.join(self.path, self.sorteddocs[c] + ".pdf")
                        command = command + '"' + filename + '" '
            command += " output " + '"' + os.path.join(self.path, "ALL-submissions.pdf")+ '" '
            ret = utils.run_command( command )
            if len(ret.strip())>0:
                raise IOError('pdftk can not merge files due to the following reason: \n'+ret)
        except Exception as e:
            self._initialize()
            wx.PostEvent(self._notify_window, ResultEvent(text='Can not merge files. No merged output. %s' % e, num=-1))
            return

    # End run_merge_pdf
    # -----------------------------------------------------------------------


    def run_toc(self, title):
        """
        Create the table of contents.
        """

        if not len(self.sortedsessions):
            return

        self.tasktext = 'Create the table of contents.'
        self.tasknum += 1
        wx.PostEvent(self._notify_window, ResultEvent(text=self.tasktext, num=self.tasknum))

        #latex =  "\\thispagestyle{empty}\n"
        #latex += "\\pagestyle{empty}\n"
        latex = '\\section*{'+title+'}\n'
        latex += "\\begin{longtable}{p{15cm}r}\n"

        count = 0
        for session in self.sortedsessions:

            # Add the session name only for sessions with documents
            thissessiondoc = list()
            for i in range(len(self.sorteddocs)):
                doc = self.documents[self.sorteddocs[i]]
                if doc.get_session() == session:
                    thissessiondoc.append( doc )

            # Add documents
            if len(thissessiondoc):

                latex += "  &  \\\\ \n"
                latex += "\\color{color3}{{\\bf " + session.get_session_name() + "}} &  \\\\ \n"
                latex += "  &  \\\\ \n"

                for doc in thissessiondoc:
                    if doc.get_session() != session:
                        continue
                    # first line : title, then page number
                    #latex += "{\\bf " + self.documents[docid].get_title() + "} & "
                    latex += "$ \\color{color1}{"+self.__get_sessionid_and_rank(doc.get_docid()) + "}$ {\\bf " + unicode_to_tex(doc.get_title()) + "} "
                    latex += " & \\color{FooterColor}{" + str(doc.get_page())  + "} \\\\ \n"
                    # second line : complete list of authors
                    latex +=" {\it "
                    for author in doc.get_authors():
                        latex += unicode_to_tex(author.get_firstname())+" "+unicode_to_tex(author.get_lastname())+", "
                    latex = latex[:-2] + "} & \\\\ \n"
                    # an empty line between 2 documents
                    latex += "  &  \\\\ \n"

                    if self._want_abort:
                    # Use a result of None to acknowledge the abort.
                        wx.PostEvent(self._notify_window, ResultEvent(text=None, num=-1))
                        return
                    else:
                        wx.PostEvent(self._notify_window, ResultEvent(text=self.tasktext, num=self.tasknum, percent=100.*float(count)/float(len(self.sortedsessions))))

            count = count + 1
        latex +=  "\\end{longtable}\n"
        #latex = latex.replace('_', '\_')
        try:
            tagpdf = self._create_tagpdf()
            self.__unset_session_in_tag(tagpdf)
            self.__unset_page_in_tag( tagpdf )
            self.__set_conference_in_tag( tagpdf )
            self.__generate_latex( tagpdf, latex, os.path.join(self.path, "TableOfContent.pdf"), inc=False)
        except Exception as e:
            self._initialize()
            logging.info('... Error. Can not create the TOC: %s'%str(e))
            wx.PostEvent(self._notify_window, ResultEvent(text='Error. Can not create the table of contents.', num=-1))
            return

    # End run_toc
    # -----------------------------------------------------------------------


    def run_index_authors(self, title):
        """
        Create the index of authors as a PDF file.
        """

        self.tasktext = 'Create the index of authors.'
        self.tasknum += 1
        wx.PostEvent(self._notify_window, ResultEvent(text=self.tasktext, num=self.tasknum))

        latex =  '\\section*{'+title+'}\n'
        latex += "\\begin{longtable}{p{45mm}p{75mm}r}\n"

        for authorid in sorted(self.authors.keys(), key=lambda v: v.upper()):
            author = self.authors[authorid]

            pages = list()
            for doc in self.documents.values():
                if author in doc.get_authors():
                    p = doc.get_page()
                    if not p is None and not p == 0:
                        pages.append( str(p) )

            if len(pages) > 0:
                docspages = ", ".join(pages)
                latex += unicode_to_tex(author.get_lastname())+", "+self.__initials(author.get_firstname()) + ". & "
                latex += "{\sf " + unicode_to_tex(author.get_email()) + "} & "
                latex += docspages + " \\\\ \n"

            if self._want_abort:
            # Use a result of None to acknowledge the abort.
                wx.PostEvent(self._notify_window, ResultEvent(text=None, num=-1))
                return
        latex +=  "\\end{longtable}\n"

        try:
            tagpdf = self._create_tagpdf()
            self.__unset_session_in_tag(tagpdf)
            self.__unset_page_in_tag( tagpdf )
            self.__set_conference_in_tag( tagpdf )
            self.__generate_latex( tagpdf, latex, os.path.join(self.path, "AuthorsIndex.pdf") )
        except Exception as e:
            self._initialize()
            logging.info('... Error. Can not create the index of authors: %s'%str(e))
            wx.PostEvent(self._notify_window, ResultEvent(text='Error. Can not create the index of authors.', num=-1))
            return

    # End run_index_authors
    # -----------------------------------------------------------------------


    def run_list_authors(self, title):
        """
        Create the list of authors
        """

        self.tasktext = 'Create the list of authors.'
        self.tasknum += 1
        wx.PostEvent(self._notify_window, ResultEvent(text=self.tasktext, num=self.tasknum))

        latex =  '\\section*{'+title+'}\n'
        latex += "\\begin{longtable}{p{8cm}p{8cm}}\n"
        for authorid in sorted(self.authors.keys()):
            author = self.authors[authorid]
            # get only authors of a document!
            for doc in self.documents.values():
                if author in doc.get_authors():
                    latex += unicode_to_tex(author.get_lastname())+" "+unicode_to_tex(author.get_firstname()) + " & "
                    latex += unicode_to_tex(author.get_email()) + " \\\\ \n"
                if self._want_abort:
                # Use a result of None to acknowledge the abort.
                    wx.PostEvent(self._notify_window, ResultEvent(text=None, num=-1))
                    return
        latex += "\\end{longtable}\n"

        try:
            tagpdf = self._create_tagpdf()
            self.__unset_session_in_tag(tagpdf)
            self.__unset_page_in_tag( tagpdf )
            self.__set_conference_in_tag( tagpdf )
            self.__generate_latex( tagpdf, latex, os.path.join(self.path, "AuthorsList.pdf"), inc=False)
        except Exception as e:
            self._initialize()
            logging.info('... Error. Can not create the list of authors: %s'%str(e))
            wx.PostEvent(self._notify_window, ResultEvent(text='Error. Can not create the list of authors.', num=-1))
            return

    # End run_list_authors
    # -----------------------------------------------------------------------


    def run_program(self, title):
        """
        Create the program.
        """

        self.tasktext = 'Create the program.'
        self.tasknum += 1
        wx.PostEvent(self._notify_window, ResultEvent(text=self.tasktext, num=self.tasknum))

        # Necessarily the program is organized by dates!
        self.sort_documents(sortbytype=False)

        latex =  "\\thispagestyle{empty}\n"
        latex += "\\pagestyle{empty}\n"
        latex += '\\section*{'+title+'}\n'

        for datesession in self.sorteddates:
            if len(self.sorteddates)>1:
                latex +=  "\\subsection*{ \\color{color2}{"+datesession.strftime('%A, %B %d %Y')+" } }\n"
            latex += "\\begin{longtable}{p{35mm}p{125mm}}\n"

            for session in self.sortedsessions:

                if session.get_date() == datesession:
                    #latex += "\\hline \n"
                    latex += " & \\\\ \n"
                    # Add the hours info
                    latex += "{\\bf " + session.get_h_deb()+" - "+session.get_h_fin()+"} & "
                    # Add the Session Name
                    latex += "\\color{color3}{{\\bf " + unicode_to_tex(session.get_session_name()) +"}} \\\\ \n"
                    # next line: location or empty line;
                    if session.get_location() is not None:
                        latex += session.get_location()
                    latex += " & \\\\ \n"

                    # Add the list of documents
                    #if "PS" in session.get_session_name(): ######AMLAP: do not include posters in TOC
                    #    continue
                    for i in range(len(self.sorteddocs)):
                        doc = self.documents[self.sorteddocs[i]]
                        if doc.get_session() == session:
                            latex +=" & "
                            # first line : sessionid, title, then page number
                            latex += "$ \\color{color1}{"+ self.__get_sessionid_and_rank(doc.get_docid()) + "} $ "
                            latex += "{\\bf  "+ unicode_to_tex(doc.get_title()) + "} \\\\ \n"
                            # second line : complete list of authors
                            latex +=" & {\it "
                            for author in doc.get_authors():
                                latex += unicode_to_tex(author.get_firstname())+" "+unicode_to_tex(author.get_lastname())+", "
                            latex = latex[:-2] + "} \\\\ \n"
                    #latex += " & \\\\ \n"

                    if self._want_abort:
                    # Use a result of None to acknowledge the abort.
                        wx.PostEvent(self._notify_window, ResultEvent(text=None, num=-1))
                        return
            latex +=  "\\end{longtable}\n"
        #latex = latex.replace('_', '\_')

        try:
            tagpdf = self._create_empty_tagpdf()
            self.__generate_latex(tagpdf, latex, os.path.join(self.path, "Program.pdf"), inc=False)
        except Exception as e:
            self._initialize()
            logging.info('... Error. Can not create the Program: %s'%str(e))
            wx.PostEvent(self._notify_window, ResultEvent(text='Error. Can not create the program.', num=-1))
            return

    # End run_program
    # -----------------------------------------------------------------------


    def run_short_program(self, title):
        """
        Create the short program.
        """

        self.tasktext = 'Create the program overview.'
        self.tasknum += 1
        wx.PostEvent(self._notify_window, ResultEvent(text=self.tasktext, num=self.tasknum))

        # Necessarily the program is organized by dates!
        self.sort_documents(sortbytype=False)

        latex =  "\\thispagestyle{empty}\n"
        latex += "\\pagestyle{empty}\n"
        latex += '\\section*{'+title+'}\n'

        for datesession in self.sorteddates:

            if len(self.sorteddates)>1:
                latex +=  "\\subsection*{ \\color{color2}{"+datesession.strftime('%A, %B %d %Y')+"} }\n"
            latex += "\\begin{longtable}{p{35mm}p{105mm}r}\n"

            prec_hour = ""
            for session in self.sortedsessions:

                if session.get_date() == datesession:
                    # add empty line only if the previous session was not at the same time (not in parallel)
                    if prec_hour != session.get_h_deb():
                        latex += " & & \\\\ \n"
                    else:
                        latex += "\n"
                    prec_hour = session.get_h_deb()
                    # Add the hours info
                    latex += session.get_h_deb()+" - "+session.get_h_fin()+" & "
                    # Add the sessionID only for sessions with documents
                    withdoc = False

                    for i in range(len(self.sorteddocs)):
                        doc = self.documents[self.sorteddocs[i]]
                        if doc.get_session() == session:
                            withdoc = True

                    if withdoc is True:
                        latex += "\\color{color1}{" + session.get_sessionid()+"} "

                    # Add the Session Name
                    sn = unicode_to_tex(session.get_session_name())
                    if sn > 0:
                        latex += "\\color{color3}{" + sn + "}"
                    latex += " & "
                    if session.get_location() is not None:
                        latex += session.get_location()
                    latex += " \\\\ \n"
                    #latex += " & & \\\\ \n"

                    if self._want_abort:
                    # Use a result of None to acknowledge the abort.
                        wx.PostEvent(self._notify_window, ResultEvent(text=None, num=-1))
                        return
            latex +=  "\\end{longtable}\n"
            latex +=  "\\pagebreak\n"
        #latex = latex.replace('_', '\_')

        try:
            tagpdf = self._create_empty_tagpdf()
            self.__generate_latex( tagpdf, latex, os.path.join(self.path, "ProgramOverview.pdf"), inc=False)
        except Exception:
            self._initialize()
            wx.PostEvent(self._notify_window, ResultEvent(text='Error. Can not create the program overview.', num=-1))
            return

    # End run_short_program
    # -----------------------------------------------------------------------


    # -----------------------------------------------------------------------
    # Private
    # -----------------------------------------------------------------------


    def sort_sessions_by_type(self):
        """
        Sort all sessions depending on the date.

        If at least one date is missing, sort on alpha-numeric of keys.

        """
        self.sortedsessions = list()

        # Keep all sessions types
        alltypes = list()
        for session in self.sessions.values():
            sessionidkey = session.get_sessionid()
            sessionidkey = sessionidkey.replace('[', '')
            sessionidkey = sessionidkey.replace(']', '')
            sessionidkey = sessionidkey[0:2]
            if sessionidkey not in alltypes:
                alltypes.append(sessionidkey)
        # sort ID-keys
        self.sortedidkeys = sorted(alltypes)

        # sort sessions inside each type
        for idtype in self.sortedidkeys:

            # keep all sessions of this type
            sessionstype = list()
            for session  in self.sessions.values():
                if idtype in session.get_sessionid():
                    sessionstype.append(session)

            # keep all dates of this session-type in a list
            alldates = list()
            for session in sessionstype: #self.sessions.values():
                sessiondate = session.get_date()
                if sessiondate not in alldates:
                    alldates.append(sessiondate)

            # sort dates
            self.sorteddates = sorted(alldates)
            # sort sessions inside each date
            for date in self.sorteddates:
                # keep all sessions of this date
                sessionsdate = list()
                for session  in sessionstype: #self.sessions.values():
                    if session.get_date() == date:
                        sessionsdate.append(session)

                # sort sessions of this date, with their rank
                ranks = {}
                r = 1000
                for session in sessionsdate:
                    if session.get_rank() != 0:
                        ranks[session.get_rank()] = session
                    else:
                        # some missing ranks...
                        # unsorted sessions at the end
                        ranks[r] = session
                        r = r+1

                    if self._want_abort:
                    # Use a result of None to acknowledge the abort.
                        wx.PostEvent(self._notify_window, ResultEvent(text=None, num=-1))
                        return

                for r in sorted(ranks.keys()):
                    self.sortedsessions.append( ranks[r] )

    # End sort_sessions_by_type
    # -----------------------------------------------------------------------


    def sort_sessions_by_date(self):
        """
        Sort all sessions depending on the date.

        If at least one date is missing, sort on alpha-numeric of keys.

        """
        self.sortedsessions = list()

        if len(self.validator.date_in_sessions()) > 0:
            # Some missing dates in sessions...
            self.sortedsessions = sorted(self.sessions.keys())
            return False

        # keep all dates in a list
        alldates = list()
        for session in self.sessions.values():
            sessiondate = session.get_date()
            if sessiondate not in alldates:
                alldates.append(sessiondate)

        # sort dates
        self.sorteddates = sorted(alldates)

        # sort sessions inside each date
        for date in self.sorteddates:

            # keep all sessions of this date
            sessionsdate = list()
            for session  in self.sessions.values():
                if session.get_date() == date:
                    sessionsdate.append(session)

            # sort sessions of this date, with their rank
            ranks = {}
            r = 1000
            for session in sessionsdate:
                if session.get_rank() != 0:
                    ranks[session.get_rank()] = session
                else:
                    # unsorted sessions at the end
                    ranks[r] = session
                    r = r+1

                if self._want_abort:
                # Use a result of None to acknowledge the abort.
                    wx.PostEvent(self._notify_window, ResultEvent(text=None, num=-1))
                    return

            for r in sorted(ranks.keys()):
                self.sortedsessions.append( ranks[r] )

        return True

    # End sort_sessions_by_date
    # -----------------------------------------------------------------------


    def sort_documents(self, sortbytype=False):
        """
        Sort documents depending on:
        1. the type of sessions (if any),
        2. the date of sessions,
        3. the rank.

        If at least one document is not assigned to a session, sort by docid.

        """

        self.sorteddocs = list()

        if len(self.validator.session_in_documents()) > 0:
            # No sessions, sort by docid...
            self.sorteddocs = sorted(self.documents.keys())
            return False

        # Sort by sessions
        if sortbytype is False:
            self.sort_sessions_by_date()
        else:
            self.sort_sessions_by_type()

        for s in self.sortedsessions:

            # List all docs of this sessions (the docid)
            docs = list()
            for d in self.documents.values():
                if d.get_session() == s:
                    docs.append(d.get_docid())

            # then, sort these docs with their rank...
            ranks = {}
            ranks[0] = None
            for docid in docs:
                if self.documents[docid].get_rank() is None or self.documents[docid].get_rank() == 0:
                    # some missing ranks... get the next good rank
                    r = 1
                    while r in ranks.keys():
                        r = r+1
                else:
                    # get the given rank (except if duplicated!)
                    if self.documents[docid].get_rank() not in ranks.keys():
                        r = self.documents[docid].get_rank()
                    else:
                        r = 1
                        while r in ranks.keys():
                            r = r+1
                ranks[r] = docid
            for r in sorted(ranks.keys()):
                if r > 0:
                    self.sorteddocs.append( ranks[r] )
        return True

    # End sort_documents
    # -----------------------------------------------------------------------

    def _create_empty_tagpdf(self):
        # Create a TagPDF with empty header/footer.
        tagpdf = tagPdfFile()

        tagpdf.set_paper_format( self._prefsIO.GetValue('PAGE_FORMAT') )
        tagpdf.set_top_margin( self._prefsIO.GetValue('TOP_MARGIN') )
        tagpdf.set_bottom_margin( self._prefsIO.GetValue('BOTTOM_MARGIN') )
        tagpdf.set_head_size( self._prefsIO.GetValue('HEADER_SIZE') )
        tagpdf.set_foot_size( self._prefsIO.GetValue('FOOTER_SIZE') )

        tagpdf.set_left_header( "" )
        tagpdf.set_center_header( "" )
        tagpdf.set_right_header( "" )
        tagpdf.set_left_footer( "" )
        tagpdf.set_center_footer( "" )
        tagpdf.set_right_footer( "" )

        tagpdf.set_header_color( self._prefsIO.GetValue('HEADER_COLOR') )
        tagpdf.set_footer_color( self._prefsIO.GetValue('FOOTER_COLOR') )
        tagpdf.set_header_style( self._prefsIO.GetValue('HEADER_STYLE') )
        tagpdf.set_footer_style( self._prefsIO.GetValue('FOOTER_STYLE') )

        tagpdf.set_header_rule( self._prefsIO.GetValue('HEADER_RULER') )
        tagpdf.set_footer_rule( self._prefsIO.GetValue('FOOTER_RULER') )

        tagpdf.set_option( "color1", self._prefsIO.GetValue('COLOUR_1') )
        tagpdf.set_option( "color2", self._prefsIO.GetValue('COLOUR_2') )
        tagpdf.set_option( "color3", self._prefsIO.GetValue('COLOUR_3') )

        tagpdf.set_page_number( self.nbpages )

        return tagpdf

    # -----------------------------------------------------------------------

    def _create_tagpdf(self):
        # Create a TagPDF instance from preferences.
        tagpdf = self._create_empty_tagpdf()

        tagpdf.set_left_header(   unicode_to_tex(self._prefsIO.GetValue('HEADER_LEFT')) )
        tagpdf.set_center_header( unicode_to_tex(self._prefsIO.GetValue('HEADER_CENTER')) )
        tagpdf.set_right_header(  unicode_to_tex(self._prefsIO.GetValue('HEADER_RIGHT')) )
        tagpdf.set_left_footer(   unicode_to_tex(self._prefsIO.GetValue('FOOTER_LEFT')) )
        tagpdf.set_center_footer( unicode_to_tex(self._prefsIO.GetValue('FOOTER_CENTER')) )
        tagpdf.set_right_footer(  unicode_to_tex(self._prefsIO.GetValue('FOOTER_RIGHT')) )

        return tagpdf

    # -----------------------------------------------------------------------

    def __get_sessionid_and_rank(self, docid):
        # Get the session
        __s = self.documents[docid].get_session()
        if __s is None or __s == "":
            return ""
        # Get session id
        sessionid = __s.get_sessionid()
        if not sessionid.startswith('['):
            sessionid = '[' + sessionid + ']'
        # Get session rank
        docrank = self.documents[docid].get_rank()
        # Create the string to return
        if docrank is None or docrank == 0:
            return sessionid

        sessionid = sessionid[:-1] #.replace(']', '')
        return sessionid+"."+str(docrank)+"]"

    # -----------------------------------------------------------------------

    def __set_conference_in_tag(self, tagpdf):
        acronym = self.conference.keys()[0]
            # only one conference can be defined.
            # and the acronym is the key of a conference

        if "conference" in tagpdf.get_option("rightheader").lower():
            tagpdf.set_right_header( acronym )

        if "conference" in tagpdf.get_option("leftheader").lower():
            tagpdf.set_left_header( acronym )

        if "conference" in tagpdf.get_option("centerheader").lower():
            tagpdf.set_center_header( acronym )

        if "conference" in tagpdf.get_option("rightfooter").lower():
            tagpdf.set_right_footer( acronym )

        if "conference" in tagpdf.get_option("leftfooter").lower():
            tagpdf.set_left_footer( acronym )

        if "conference" in tagpdf.get_option("centerfooter").lower():
            tagpdf.set_center_footer( acronym )

    # -----------------------------------------------------------------------

    def __set_page_in_tag(self, tagpdf):

        if "page" in tagpdf.get_option("rightheader").lower():
            tagpdf.set_right_header( "\\thepage" )

        if "page" in tagpdf.get_option("leftheader").lower():
            tagpdf.set_left_header( "\\thepage" )

        if "page" in tagpdf.get_option("centerheader").lower():
            tagpdf.set_center_header( "\\thepage" )

        if "page" in tagpdf.get_option("rightfooter").lower():
            tagpdf.set_right_footer( "\\thepage" )

        if "page" in tagpdf.get_option("leftfooter").lower():
            tagpdf.set_left_footer( "\\thepage" )

        if "page" in tagpdf.get_option("centerfooter").lower():
            tagpdf.set_center_footer( "\\thepage" )

    def __unset_page_in_tag(self, tagpdf):

        if "page" in tagpdf.get_option("rightheader").lower():
            tagpdf.set_right_header( "" )

        if "page" in tagpdf.get_option("leftheader").lower():
            tagpdf.set_left_header( "" )

        if "page" in tagpdf.get_option("centerheader").lower():
            tagpdf.set_center_header( "" )

        if "page" in tagpdf.get_option("rightfooter").lower():
            tagpdf.set_right_footer( "" )

        if "page" in tagpdf.get_option("leftfooter").lower():
            tagpdf.set_left_footer( "" )

        if "page" in tagpdf.get_option("centerfooter").lower():
            tagpdf.set_center_footer( "" )

    # -----------------------------------------------------------------------

    def __set_session_in_tag(self, tagpdf, docid):

        if "session" in tagpdf.get_option("rightheader").lower():
            tagpdf.set_right_header( self.__get_sessionid_and_rank(docid) )

        if "session" in tagpdf.get_option("leftheader").lower():
            tagpdf.set_left_header( self.__get_sessionid_and_rank(docid) )

        if "session" in tagpdf.get_option("centerheader").lower():
            tagpdf.set_center_header( self.__get_sessionid_and_rank(docid) )

        if "session" in tagpdf.get_option("rightfooter").lower():
            tagpdf.set_right_footer( self.__get_sessionid_and_rank(docid) )

        if "session" in tagpdf.get_option("leftfooter").lower():
            tagpdf.set_left_footer( self.__get_sessionid_and_rank(docid) )

        if "session" in tagpdf.get_option("centerfooter").lower():
            tagpdf.set_center_footer( self.__get_sessionid_and_rank(docid) )

    def __unset_session_in_tag(self, tagpdf):

        if "session" in tagpdf.get_option("rightheader").lower():
            tagpdf.set_right_header( "" )

        if "session" in tagpdf.get_option("leftheader").lower():
            tagpdf.set_left_header( "" )

        if "session" in tagpdf.get_option("centerheader").lower():
            tagpdf.set_center_header( "" )

        if "session" in tagpdf.get_option("rightfooter").lower():
            tagpdf.set_right_footer( "" )

        if "session" in tagpdf.get_option("leftfooter").lower():
            tagpdf.set_left_footer( "" )

        if "session" in tagpdf.get_option("centerfooter").lower():
            tagpdf.set_center_footer( "" )

    # -----------------------------------------------------------------------

    def __generate_latex(self, tagpdf, latex, filename, inc=True):
        # recto or verso? Supposed to be on a recto (impair number)
        if inc is True and not self.nbpages%2:
            self.nbpages += 1

        tagpdf.set_page_number( self.nbpages )
        tagpdf.set_tex_content( latex ) #unicode_to_texipa(latex) )
        tagpdf.exportPDF( filename )
        tagpdf.set_tex_content( None )

        # update nbpages
        if inc is True and os.path.exists( filename ):
            self.nbpages += utils.countPages( filename )

    # -----------------------------------------------------------------------

    def __initials(self, name):
        """ Get upper characters of name, separated by a dot. """
        return ".".join([x for x in name if x.isupper()])

    # End __initials
    # -----------------------------------------------------------------------

# ---------------------------------------------------------------------------
