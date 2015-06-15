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

import wx
import wx.lib
import logging
import wx.grid
import shutil
import os
import csv

from wxgui.sp_consts import BACKGROUND_COLOR
import wxgui.models.readers as readers

from wxgui.models.dataconference  import Conference
from wxgui.models.datasession     import Session
from wxgui.models.dataauthor      import Author
from wxgui.models.datadocument    import Document

from wxgui.frames.checkframe    import CheckFrame
from wxgui.frames.generateframe import GenerateFrame
from wxgui.frames.modifframe    import ModifFrame
from wxgui.frames.createframe   import CreateDocument, CreateAuthor, CreateSession, CreateConference
from wxgui.frames.import_wizard import ImportWizard, EVT_IMPORT_WIZARD_FINISHED

from checklistpanel import CheckListPanel

from sp_glob import PAGESLIST, fieldnames

# ---------------------------------------------------------------------------


class NotebookPanel( wx.Panel ):
    """
    @author: Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: A panel with a notebook to list all data types.

    """

    def __init__(self, parent):

        wx.Panel.__init__(self, parent, -1, style=wx.NO_BORDER)
        self.SetBackgroundColour(BACKGROUND_COLOR)

        self._set_members()

        self._noteBook = wx.Notebook(self, style=wx.NO_BORDER)
        self._noteBook.SetBackgroundColour( BACKGROUND_COLOR )

        self._pages = {}
        for p in PAGESLIST:
            self._pages[p] = CheckListPanel(self._noteBook, p)
            self._noteBook.AddPage( self._pages[p], p )

        noteBookSizer = wx.BoxSizer()
        noteBookSizer.Add(self._noteBook, flag=wx.EXPAND, proportion=1)
        self.SetSizer(noteBookSizer)

        self._noteBook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnChangePage)
        self.Bind(EVT_IMPORT_WIZARD_FINISHED, self.OnImportFinished)

    # -----------------------------------------------------------------------

    def _set_members(self):
        """
        Fix members to default values.
        """

        # notebook page contents
        self._path = None
        self._dataPages = {}
        for p in PAGESLIST:
            self._dataPages[p] = dict()

        # information
        self._isSaved = True
        self._selectedPage = PAGESLIST[0]

    # -----------------------------------------------------------------------

    # -----------------------------------------------------------------------
    # Functions
    # -----------------------------------------------------------------------

    def IsSaved(self):
        """
        Return the current status of the data: saved or not?
        """
        return self._isSaved

    # -----------------------------------------------------------------------

    def GetObject(self, objid):
        for p in PAGESLIST:
            if self._dataPages[p].has_key(objid):
                return self._dataPages[p][objid]
        return None

    # -----------------------------------------------------------------------

    # -----------------------------------------------------------------------
    # Callbacks of the notebook
    # -----------------------------------------------------------------------

    def OnChangePage(self, e):
        e.Skip()
        self._selectedPage = PAGESLIST[ e.GetSelection() ]
        self.GetTopLevelParent().UnsetSelected()

    # -----------------------------------------------------------------------

    # -----------------------------------------------------------------------
    # Callbacks to manage the data
    # -----------------------------------------------------------------------

    def OnImport(self, event):
        """"""
        ImportWizard(self)

    def OnImportFinished(self, event):
        """"""
        logging.debug('Import finished. Load data from: %s'%event.path)
        self.Load(event.path)

    def OnOpen(self, event):
        """
        Callback to open load new data.
        """
        # already loaded data!
        if self._path is not None:
            dlg = wx.MessageDialog(self, "No!\n Data are already opened.", "Warning", wx.OK| wx.ICON_INFORMATION)
            dlg.ShowModal()
            return

        dlg = wx.DirDialog(self, message = "Choose a directory to get data",
            defaultPath = os.path.dirname(os.getcwd()), style=wx.OPEN|wx.DD_DIR_MUST_EXIST|wx.CHANGE_DIR)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            logging.debug('Open a new directory:'+path)
            self.Load(path)
        dlg.Destroy()

    # ------------------------------------------------------------------------

    def Load(self, path):
        """"""
        # Check the directory in order to see if all required files are inside.
        missingPdf = True
        files = {}
        for p in PAGESLIST:
            files[p] = False
        for file_name in os.listdir(path):
            for p in PAGESLIST:
                if file_name.lower() == p.lower()+".csv":
                    files[p] = True
                elif file_name.lower().endswith(".pdf"):
                    missingPdf = False

        if missingPdf is True:
            dlg = wx.MessageDialog(self, "The directory %s does not contain any pdf file. Continue anyway?" % (path), "Warning", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
            retCode = dlg.ShowModal()
            if retCode == wx.ID_NO:
                return

        checkCSV = True
        for a in files.values():
            if a is False:
                checkCSV = False

        if checkCSV is False:
            dlg = wx.MessageDialog(self, "At least one CSV file is missing in %s, do you want to create it?" % (path), "Warning", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
            retCode = dlg.ShowModal()
            if retCode == wx.ID_YES:
                for i in range(len(PAGESLIST)):
                    if files[PAGESLIST[i]] == False:
                        out = csv.DictWriter(open(os.path.join(path,PAGESLIST[i]+".csv"), "wb"), fieldnames[PAGESLIST[i]])
                        d = {}
                        for colname in fieldnames[PAGESLIST[i]]:
                            d[colname] = colname
                        out.writerow(d)
                        #self.FileInDefaultDoc(out, path)
            else:
                return

        try:
            self.GetTopLevelParent().GetStatusBar().SetStatusText('Please wait while loading data...')
            self.useCSVFile( path )
            self.GetTopLevelParent().GetStatusBar().SetStatusText('Data loaded successfully.')
            self.ShowData()
            self._isSaved = True
            self._path = path
        except Exception, error:
            self._set_members()
            dlg = wx.MessageDialog(None, 'Error opening files:\n' + str(error), 'Error...', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()

    # End Load
    # ------------------------------------------------------------------------

    def OnSave(self, event):
        """
        Callback to save loaded data.
        """
        # no loaded data!
        if not self._path:
            self.ForbiddenDialog(event)
            return

        logging.debug('Save')
        if self._isSaved is False:
            dlg = wx.MessageDialog(self, "Confirm you want to save changes?", "Warning", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
            retCode = dlg.ShowModal()
            if retCode == wx.ID_YES:
                for p in PAGESLIST:
                    self.saveCSV( p )
                self._isSaved = True
                self.GetTopLevelParent().GetStatusBar().SetStatusText('Data saved successfully.')

    # End OnSave
    # ------------------------------------------------------------------------

    def OnCheck(self, event):
        """
        Callback to check if loaded data can be exported.
        """
        # no loaded data!
        if not self._path:
            self.ForbiddenDialog(event)
            return

        logging.debug('Check')
        dlg = CheckFrame(self, -1, "Data Verification...", self._dataPages['Documents'], self._dataPages['Authors'], self._dataPages['Sessions'], self._path)
        dlg.ShowModal()

    # End OnCheck
    # ------------------------------------------------------------------------

    def OnGenerate(self, event):
        """
        Callback to export loaded data as a PDF document.
        """

        if not self._path:
            self.ForbiddenDialog(event)
            return

        logging.debug('Generate')
        if self._path is None:
            wx.MessageBox( "Unknown data path.", "Error...", wx.OK | wx.ICON_EXCLAMATION)
            return

        dlg = GenerateFrame(self, -1, "PDF generator...", self._dataPages['Conference'],  self._dataPages['Documents'], self._dataPages['Authors'], self._dataPages['Sessions'], self._path)
        dlg.ShowModal()

    # End OnGenerate
    # ------------------------------------------------------------------------

    def OnNewEntry(self, event):
        """
        Callback to create a new entry.
        """
        logging.debug('New entry in '+self._selectedPage)

        if self._selectedPage == "Authors":
            createdlg = CreateAuthor(self, -1, "Add an author")
            retCode   = createdlg.ShowModal()
            if retCode == wx.ID_OK and len(createdlg.GetFirstName())>0 and createdlg.GetFirstName():
                newauthor = Author(createdlg.GetLastName(),createdlg.GetFirstName())
                eltid     = newauthor.get_authorid()
                # verify (to not create an already existing author)
                if eltid in self._dataPages[self._selectedPage].keys():
                    wx.MessageBox(self, "This author is already existing", "Error", wx.OK | wx.ICON_ERROR)
                    return
                # update data
                self._dataPages[self._selectedPage][newauthor.get_authorid()] = newauthor
                # update wx.grid
                self._pages[self._selectedPage].AddData([eltid])
                self._isSaved = False
                self.GetTopLevelParent().GetStatusBar().SetStatusText('New author added.')

        elif self._selectedPage == "Documents":

            createdlg = CreateDocument(self, -1, "Add a document")
            retCode   = createdlg.ShowModal()

            if retCode == wx.ID_OK:
                eltid = createdlg.GetId()
                logging.debug('   --> new id='+eltid)
                if self._selectedPage == "Documents" and len(eltid)>0:
                    if eltid in self._dataPages[self._selectedPage].keys():
                        wx.MessageBox( "This Document-ID is already existing", "Error", wx.OK | wx.ICON_ERROR)
                        return
                    doc = Document( eltid, authors=list() )
                    # update data
                    self._dataPages[self._selectedPage][doc.get_docid()] = doc
                    # update wx.grid
                    self._pages[self._selectedPage].AddData([eltid])
                    self._isSaved = False
                    self.GetTopLevelParent().GetStatusBar().SetStatusText('New document added.')

        elif self._selectedPage == "Sessions":

            createdlg = CreateSession(self, -1, "Add a session")
            retCode   = createdlg.ShowModal()

            if retCode == wx.ID_OK:
                eltid = createdlg.GetId()
                logging.debug('   --> new id='+eltid)
                if len(eltid)>0:
                    doc = Session(eltid)
                    if eltid in self._dataPages[self._selectedPage].keys():
                        wx.MessageBox( "This Session-ID is already existing", "Error", wx.OK | wx.ICON_ERROR)
                        return
                    # update data
                    self._dataPages[self._selectedPage][doc.get_sessionid()] = doc
                    # update wx.grid
                    self._pages[self._selectedPage].AddData([eltid])
                    self._isSaved = False
                    self.GetTopLevelParent().GetStatusBar().SetStatusText('New session added.')

        elif self._selectedPage == "Conference":
            if len(self._dataPages['Conference']) == 0:
                createdlg = CreateConference(self, -1, "Add information about the conference")
                retCode   = createdlg.ShowModal()
                if retCode == wx.ID_OK:
                    acronym = createdlg.GetAcronym()
                    logging.debug('   --> new conference='+acronym)
                    if len(acronym)>0:
                        # update data
                        self._dataPages[self._selectedPage][acronym] = Conference("", acronym=acronym)
                        # update wx.grid
                        self._pages[self._selectedPage].AddData([acronym])
                        self._isSaved = False
                        self.GetTopLevelParent().GetStatusBar().SetStatusText('Conference added.')

            else:
                wx.MessageBox( "A conference is already defined.\nCan't add a new one!", "Error", wx.OK | wx.ICON_ERROR)


    # ------------------------------------------------------------------------

    def OnEditSelected(self, event):
        """
        Callback to edit the selected entry.
        """
        logging.debug('Edit')
        selection = self._pages[self._selectedPage].GetSelection()
        if selection is None or len(selection)==0:
            wx.MessageBox( "Nothing selected.", "Error...", wx.OK | wx.ICON_EXCLAMATION)
        else:
            dlg = ModifFrame(self, -1, "Modification...", self._selectedPage, selection)
            dlg.ShowModal()
            self.GetTopLevelParent().SetSelected(selection)
            self._isSaved = False
            self.GetTopLevelParent().GetStatusBar().SetStatusText('An entry was modified.')
            dlg.Destroy()

    # End OnEditSelected
    # ------------------------------------------------------------------------

    def OnDeleteSelected(self, event):
        """
        Callback to remove the selected entry.
        """
        eltid = self._pages[self._selectedPage].GetSelection()
        if eltid is None or len(eltid)==0:
            wx.MessageBox( "Nothing selected.", "Error...", wx.OK | wx.ICON_EXCLAMATION)
            return
        else:
            logging.debug('eltid of selection is: %s'%str(eltid))

        dlg = wx.MessageDialog(self, "Do you really want to remove "+eltid+"?", "Warning", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        retCode = dlg.ShowModal()

        if retCode == wx.ID_YES:
            logging.debug('Remove '+eltid)

            # removing an author only if there is no related document
            if self._selectedPage == "Authors":
                for doc in self._dataPages['Documents'].values():
                    for auth in doc.get_authors():
                        if auth.get_authorid() == eltid:
                            dlg = wx.MessageDialog(self, "This author can not be removed because there are documents associated.", "Error", wx.OK | wx.ICON_EXCLAMATION)
                            retCode = dlg.ShowModal()
                            logging.debug('   ---> '+auth.get_authorid()+" not removed.")
                            return
            # removing a session implies to update documents' sessions
            if self._selectedPage == "Sessions":
                for doc in self._dataPages['Documents'].values():
                    session = doc.get_session()
                    if isinstance(session,Session) and session.get_sessionid() == eltid:
                        doc.set_session(None)
                        logging.debug('   ---> session of document: '+str(doc.get_docid())+" removed.")
            # update grid
            self._pages[self._selectedPage].UnsetSelectedData()
            # delete the data
            del self._dataPages[self._selectedPage][eltid]
            self._isSaved = False
            self.GetTopLevelParent().UnsetSelected()
            self.GetTopLevelParent().GetStatusBar().SetStatusText('An entry was deleted.')



    # ------------------------------------------------------------------------
    # Functions to Load/Save Data
    # ------------------------------------------------------------------------

    def saveCSV(self, pagename):
        # create a backup before saving
        filename = os.path.join(self._path,pagename+".csv")
        try:
            shutil.copy(filename, filename+".backup")
        except Exception:
            pass
        # then save
        out = csv.DictWriter(open(filename, "wb"), fieldnames[pagename])
        d = {}
        for colname in fieldnames[pagename]:
            d[colname] = colname
        out.writerow(d)
        for entry in self._dataPages[pagename].values():
            rows = entry.prepare_save()
            for row in rows:
                out.writerow( dict((k, v.encode('utf-8')) for k, v in row.iteritems()) )

    # ------------------------------------------------------------------------

    def findCSV(self,path,filename):
        """ Get the real filename (with upper/lower). """
        filename = filename.lower()
        for f in os.listdir(path):
            if f.lower() == filename+".csv":
                return f

    # ------------------------------------------------------------------------

    def useCSVFile(self, path):

        ConfDict    = dict()
        DocDict     = dict()
        SessionDict = dict()
        AuthorDict  = dict()

        ################## Lecture du fichier AUTHORS.csv ####################
        logging.debug("Read the file: Conference.csv")
        confreader = readers.conference_csv_reader( os.path.join(path,self.findCSV(path,"Conference")) )
        rows = confreader.get_Rows()
        logging.debug( "GOT FOLLOWING ROWS: %s"%rows)
#        if len(rows) != 1:
#            wx.MessageBox('hum... Conference CSV file is corrupted',"Error", wx.OK | wx.ICON_EXCLAMATION)
#        else:
        for r in rows:
            logging.debug( "GOT FOLLOWING ROW: %s"%r)

            confname = confreader.get_ConfName(r)
            acronym  = confreader.get_Acronym(r)
            place    = confreader.get_Place(r)
            dfrom    = confreader.get_DateFrom(r)
            dto      = confreader.get_DateTo(r)
            ConfDict[acronym] = Conference(confname, acronym, place, dfrom, dto)
        self._dataPages['Conference'] = ConfDict

        ################# Lecture du fichier DOCUMENTS.csv ###################
        logging.debug("Read the file: Documents.csv")
        docreader = readers.documents_csv_reader( os.path.join(path,self.findCSV(path,"Documents")) )

        for docid in docreader.get_all_ids():

            authorslist = []
            session     = ""
            title       = ""
            rank        = ""
            page_number = ""
            pdf_diagnosis = ""

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

                if pdf_diagnosis == "" and docreader.get_Diagnosis(row) != "":
                    pdf_diagnosis = docreader.get_Diagnosis(row)

            doc = Document(docid, title, authorslist, session, rank, page_number, pdf_diagnosis)
            DocDict[doc.get_docid()] = doc

        self._dataPages['Documents'] = DocDict


        #################### Lecture du fichier SESSIONS.csv #################
        logging.debug("Read the file: Sessions.csv")

        sessionreader = readers.sessions_csv_reader( os.path.join(path,self.findCSV(path,"Sessions") ))

        for sessionid in sessionreader.get_AllId():
            session_row = sessionreader.get_ById(sessionid)[0]
            session     = Session(sessionid, sessionreader.get_SessionName(session_row), sessionreader.get_Rank(session_row), sessionreader.get_Date(session_row), sessionreader.get_Heure_Deb(session_row), sessionreader.get_Heure_Fin(session_row), sessionreader.get_Chairman(session_row), sessionreader.get_Location(session_row))
            SessionDict[sessionid] = session

        self._dataPages['Sessions'] = SessionDict


        ################## Lecture du fichier AUTHORS.csv ####################
        logging.debug("Read the file: Authors.csv")

        author_reader = readers.authors_csv_reader( os.path.join(path,self.findCSV(path,"Authors")) )

        for lastname, firstname in author_reader.get_all_names():
            rowList = author_reader.get_ByNames(lastname, firstname)
            a_row = rowList.pop()
            auth = Author(lastname,firstname, author_reader.get_email(a_row), author_reader.get_Affiliation(a_row))
            for row in rowList: ### all the authors which have the same name !!
                Other_auth = Author(lastname,firstname, author_reader.get_email(row), author_reader.get_Affiliation(row))
                auth.compare_and_update(Other_auth)## we use this function because there could be the same other twice in the AUTHORS.csv file, so we merge the information
            AuthorDict[auth.get_authorid()] = auth

        self._dataPages['Authors'] = AuthorDict

        logging.debug(" [ OK ] ")

    # ------------------------------------------------------------------------
    # Various...
    # ------------------------------------------------------------------------

    def ShowData(self):
        for p in PAGESLIST:
            self._pages[p].AddData( sorted(self._dataPages[p]) )

    def ForbiddenDialog(self, e):
        dlg = wx.MessageDialog(self, "No data!\n Please open a directory.", "Warning", wx.OK| wx.ICON_INFORMATION)
        dlg.ShowModal()

    # -----------------------------------------------------------------------

# ---------------------------------------------------------------------------
