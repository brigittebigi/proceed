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

"""
Graphical User Interface to manage documents of a conference.
"""

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------


import wx
import logging
import os.path

from sp_glob import program
from wxgui.frames.about       import AboutBox
from wxgui.frames.helpbrowser import HelpBrowser
from wxgui.frames.feedback    import ShowFeedbackDialog

from wxgui.panels.infopanel import InformationPanel
from wxgui.panels.datalist  import NotebookPanel

from wxgui.cutils.imageutils import spBitmap

from wxgui.sp_consts import BACKGROUND_COLOR
from wxgui.sp_consts import ASK_BEFORE_EXIT
from wxgui.sp_consts import MIN_FRAME_W
from wxgui.sp_consts import MIN_FRAME_H
from wxgui.sp_consts import FRAME_H
from wxgui.sp_consts import PANEL_W
from wxgui.sp_consts import FRAME_TITLE
from wxgui.sp_consts import FRAME_STYLE
from wxgui.sp_consts import MENU_ICONSIZE
from wxgui.sp_consts import TB_ICONSIZE

from wxgui.sp_icons import APP_ICON
from wxgui.sp_icons import EXIT_ICON
from wxgui.sp_icons import HELP_ICON
from wxgui.sp_icons import FEEDBACK_ICON
from wxgui.sp_icons import IMPORT_EXPORT_ICON
from wxgui.sp_icons import OPEN_ICON
from wxgui.sp_icons import SAVE_ICON
from wxgui.sp_icons import CHECK_ICON
from wxgui.sp_icons import EXPORT_ICON
from wxgui.sp_icons import ADD_ICON
from wxgui.sp_icons import EDIT_ICON
from wxgui.sp_icons import DELETE_ICON
from wxgui.sp_icons import ABOUT_ICON


# -----------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------

VIEW_TOOLBAR_ID   = wx.NewId()
VIEW_STATUSBAR_ID = wx.NewId()

ID_GENERATE = wx.NewId()
ID_HOME     = wx.NewId()
ID_FEEDBACK = wx.NewId()

# ---------------------------------------------------------------------------


class MainFrame( wx.Frame ):
    """
    @authors: Bastien Herbaut, Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: Proceed Main frame.

    Proceed Graphical User Interface... is here!

    """


    def __init__(self):
        """
        Constructor, with default parameters and preferences.
        """

        try:
            wx.Frame.__init__(self, None, -1, style=FRAME_STYLE)
        except Exception as e:
            logging.debug('Frame init Error: %s'%str(e))
            raise

        # Set title and icon of the frame
        self._init_infos()

        # Creates the menubar, toolbar, and status bar and the client panel
        self._init_frame()

        # Frame properties
        self._frame_properties()

        # Events of this frame
        wx.EVT_SIZE(self,  self.OnSize)
        wx.EVT_CLOSE(self, self.OnExit)

        self._LayoutFrame()
        self.Show(True)

    # ------------------------------------------------------------------------

    # ------------------------------------------------------------------------
    # Private methods to create the GUI and initialize members
    # ------------------------------------------------------------------------

    def _init_infos( self ):
        """
        Set the title and the icon.

        If args contains title, get it... or use the default.

        """
        # colors
        self.SetBackgroundStyle( wx.BG_STYLE_CUSTOM )
        self.SetBackgroundColour( BACKGROUND_COLOR )
        # title
        self.SetTitle( FRAME_TITLE )
        wx.GetApp().SetAppName( program )
        # icon
        _icon = wx.EmptyIcon()
        _icon.CopyFromBitmap( wx.Bitmap(APP_ICON, wx.BITMAP_TYPE_ANY) )
        self.SetIcon(_icon)

    # ------------------------------------------------------------------------

    def _init_frame(self):
        """
        Initializes the frame.

        Creates the default about, menubar, toolbar and status bar.

        """

        # Create the about box
        self._about = AboutBox()

        # the menu
        menubar = self._create_menu()

        # Create the status bar
        self._create_statusbar()

        # Create the toolbar
        self._create_toolbar()

        if wx.Platform == '__WXMAC__':
            self.SetMenuBar(menubar)
            # wxBug: Have to set the menubar at the very end or the automatic
            # MDI "window" menu doesn't get put in the right place when the
            # services add new menus to the menubar

        self._mainpanel = self._create_content( self )

        if wx.Platform != '__WXMAC__':
            self.SetMenuBar(menubar)
            # wxBug: Have to set the menubar at the very end or the automatic
            # MDI "window" menu doesn't get put in the right place when the
            # services add new menus to the menubar

    # ------------------------------------------------------------------------

    def _frame_properties(self):
        """
        Fix frame size (adjust size depending on screen capabilities).

        """

        self.SetSizeHints(MIN_FRAME_W, MIN_FRAME_H)
        (w,h) = wx.GetDisplaySize()
        height = min(FRAME_H, h)
        width  = min(FRAME_H*w/h, w)

        self.SetSize( wx.Size(width,height) )
        self.Centre()
        self.Enable()
        self.SetFocus()

    # ------------------------------------------------------------------------

    def _create_menu(self):
        """
        Create the menu bar and return it.

        """

        menubar = wx.MenuBar()

        menuFile = wx.Menu()
        menuEdit = wx.Menu()
        helpMenu = wx.Menu()

        importItem = wx.MenuItem(menuFile, wx.ID_ADD,   'Import\tCtrl+I', 'Import data from a file')
        openItem   = wx.MenuItem(menuFile, wx.ID_OPEN,  'Open\tCtrl+O', 'Load data from a directory')
        saveItem   = wx.MenuItem(menuFile, wx.ID_SAVE,  'Save\tCtrl+S', 'Save data as CSV files')
        checkItem  = wx.MenuItem(menuFile, wx.ID_APPLY, 'Check', 'Check data')
        exportItem = wx.MenuItem(menuFile, ID_GENERATE, 'Export PDF', 'Export PDF files')
        if wx.Platform == '__WXMAC__':
            exitItem = wx.MenuItem(menuFile, wx.ID_EXIT, '&Quit\tCtrl+Q', 'Exits this program')
        else:
            exitItem = wx.MenuItem(menuFile, wx.ID_EXIT, 'E&xit\tCtrl+Q', 'Exits this program')

        importItem.SetBitmap( spBitmap(IMPORT_EXPORT_ICON, MENU_ICONSIZE) )
        openItem.SetBitmap(   spBitmap(OPEN_ICON,  MENU_ICONSIZE) )
        saveItem.SetBitmap(   spBitmap(SAVE_ICON,  MENU_ICONSIZE) )
        checkItem.SetBitmap(  spBitmap(CHECK_ICON, MENU_ICONSIZE) )
        exportItem.SetBitmap( spBitmap(EXPORT_ICON, MENU_ICONSIZE) )
        exitItem.SetBitmap(   spBitmap(EXIT_ICON, MENU_ICONSIZE) )

        menuFile.AppendItem(importItem)
        menuFile.AppendItem(openItem)
        menuFile.AppendItem(saveItem)
        menuFile.AppendSeparator()
        menuFile.AppendItem(checkItem)
        menuFile.AppendItem(exportItem)
        menuFile.AppendSeparator()
        menuFile.AppendItem(exitItem)

        # Edit
        addItem  = wx.MenuItem(menuFile, wx.ID_NEW,   '&Add',    'Add a new entry in data')
        editItem = wx.MenuItem(menuFile, wx.ID_EDIT,  '&Edit',   'Edit selected data')
        delItem  = wx.MenuItem(menuFile, wx.ID_DELETE,'&Delete', 'Delete selected data')

        addItem.SetBitmap(  spBitmap(ADD_ICON,    MENU_ICONSIZE) )
        editItem.SetBitmap( spBitmap(EDIT_ICON,   MENU_ICONSIZE) )
        delItem.SetBitmap(  spBitmap(DELETE_ICON, MENU_ICONSIZE) )

        menuEdit.AppendItem( addItem )
        menuEdit.AppendItem( editItem )
        menuEdit.AppendItem( delItem )

        # Menu Help
        # Menu Help
        helpItem  = wx.MenuItem(helpMenu, wx.ID_HELP,  '&Help browser...\tF1')
        aboutItem = wx.MenuItem(helpMenu, wx.ID_ABOUT, '&About' + ' ' + wx.GetApp().GetAppName()+"...\tF2")
        homeItem  = wx.MenuItem(helpMenu, ID_HOME,     'Project Homepage...' , 'Visit the project homepage.')
        feedbackItem = wx.MenuItem(helpMenu, ID_FEEDBACK, 'Give Feedback...' , 'Send information, or any suggestions by email.')

        aboutItem.SetBitmap( spBitmap(ABOUT_ICON, MENU_ICONSIZE) )
        helpItem.SetBitmap(  spBitmap(HELP_ICON,  MENU_ICONSIZE) )
        homeItem.SetBitmap(  spBitmap(APP_ICON,   MENU_ICONSIZE) )
        feedbackItem.SetBitmap( spBitmap(FEEDBACK_ICON, MENU_ICONSIZE))

        helpMenu.AppendItem( helpItem )
        helpMenu.AppendItem( aboutItem )
        helpMenu.AppendItem( homeItem )
        helpMenu.AppendItem( feedbackItem )

        menubar.Append(menuFile, "&File")
        menubar.Append(menuEdit, "&Edit")
        menubar.Append(helpMenu, "&Help")

        # Events
        eventslist = [ wx.ID_EXIT, wx.ID_ABOUT, wx.ID_HELP, wx.ID_ADD, wx.ID_OPEN, wx.ID_SAVE, wx.ID_NEW, ID_GENERATE, ID_HOME, ID_FEEDBACK, wx.ID_APPLY, wx.ID_EDIT, wx.ID_DELETE ]
        for event in eventslist:
            wx.EVT_MENU(self, event, self.ProcessEvent)

        wx.EVT_UPDATE_UI(self, VIEW_TOOLBAR_ID,   self.OnUpdateViewToolBar)
        wx.EVT_UPDATE_UI(self, VIEW_STATUSBAR_ID, self.OnUpdateViewStatusBar)

        return menubar

    # -----------------------------------------------------------------------

    def _create_statusbar(self):
        """
        Creates a standard StatusBar.

        """

        sb = wx.StatusBar(self)
        sb.SetFieldsCount(1)
        sb.SetStatusText("...", 0)
        self.SetStatusBar(sb)
        self.GetStatusBar().Show(wx.ConfigBase_Get().ReadInt("ViewStatusBar", True))

    # ------------------------------------------------------------------------

    def _create_toolbar(self):
        """
        Creates the default toolbar.

        """
        toolbar = self.CreateToolBar(style=wx.TB_TEXT|wx.TB_FLAT|wx.TB_DOCKABLE|wx.TB_NODIVIDER)

        toolbar.AddLabelTool(id=wx.ID_EXIT, label="Exit", bitmap=spBitmap(EXIT_ICON,TB_ICONSIZE),bmpDisabled=wx.NullBitmap, kind=wx.ITEM_NORMAL, shortHelp="Quit the application")
        toolbar.AddSeparator()

        toolbar.AddLabelTool(id=wx.ID_ADD,   label="Import", bitmap=spBitmap(IMPORT_EXPORT_ICON, TB_ICONSIZE), bmpDisabled=wx.NullBitmap, kind=wx.ITEM_NORMAL, shortHelp="Import data from a file")
        toolbar.AddLabelTool(id=wx.ID_OPEN,  label="Open",   bitmap=spBitmap(OPEN_ICON, TB_ICONSIZE),  bmpDisabled=wx.NullBitmap, kind=wx.ITEM_NORMAL, shortHelp="Open a new directory")
        toolbar.AddLabelTool(id=wx.ID_SAVE,  label="Save",   bitmap=spBitmap(SAVE_ICON, TB_ICONSIZE),  bmpDisabled=wx.NullBitmap, kind=wx.ITEM_NORMAL, shortHelp="Save into CSV files")
        toolbar.AddLabelTool(id=wx.ID_APPLY, label="Check",  bitmap=spBitmap(CHECK_ICON, TB_ICONSIZE), bmpDisabled=wx.NullBitmap, kind=wx.ITEM_NORMAL, shortHelp="Check the data")
        toolbar.AddLabelTool(id=ID_GENERATE, label="Export", bitmap=spBitmap(EXPORT_ICON, TB_ICONSIZE),bmpDisabled=wx.NullBitmap, kind=wx.ITEM_NORMAL, shortHelp="Export as PDF files")
        toolbar.AddSeparator()

        toolbar.AddLabelTool(id=wx.ID_NEW,   label="Add",    bitmap=spBitmap(ADD_ICON, TB_ICONSIZE),   bmpDisabled=wx.NullBitmap, kind=wx.ITEM_NORMAL, shortHelp="Create a new entry")
        toolbar.AddLabelTool(id=wx.ID_EDIT,  label="Edit",   bitmap=spBitmap(EDIT_ICON, TB_ICONSIZE),  bmpDisabled=wx.NullBitmap, kind=wx.ITEM_NORMAL, shortHelp="Modify the selected entry")
        toolbar.AddLabelTool(id=wx.ID_DELETE,label="Delete", bitmap=spBitmap(DELETE_ICON, TB_ICONSIZE),bmpDisabled=wx.NullBitmap, kind=wx.ITEM_NORMAL, shortHelp="Delete the selected entry")
        toolbar.AddSeparator()

        toolbar.AddLabelTool(id=wx.ID_ABOUT, label="About", bitmap=spBitmap(ABOUT_ICON, TB_ICONSIZE),  bmpDisabled=wx.NullBitmap, kind=wx.ITEM_NORMAL, shortHelp="About this application")

        # events
        eventslist = [ wx.ID_EXIT, wx.ID_ABOUT, wx.ID_HELP, wx.ID_OPEN, wx.ID_SAVE, wx.ID_NEW, ID_GENERATE, wx.ID_APPLY, wx.ID_EDIT, wx.ID_DELETE ]
        for event in eventslist:
            wx.EVT_TOOL(self, event, self.ProcessEvent)

        toolbar.Realize()
        self.SetToolBar(toolbar)

    # ------------------------------------------------------------------------

    def _create_content(self, parent):
        """
        Create the frame content.

        """
        panel = wx.SplitterWindow(parent, -1, style=wx.SP_3DSASH)
        #panel.SetMinimumPaneSize( 200 )
        panel.SetSashGravity(0.3)

        self.nbp = NotebookPanel(panel)
        self.idp = InformationPanel(panel)

        panel.SplitVertically( self.nbp , self.idp , PANEL_W )
        self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED, self.OnSize, panel)

        return panel

    # ------------------------------------------------------------------------

    def _LayoutFrame(self):
        """
        Lays out the frame.

        """
        wx.LayoutAlgorithm().LayoutFrame(self, self._mainpanel)
        self.idp.SendSizeEvent()
        self.Refresh()

    # ------------------------------------------------------------------------

    # ------------------------------------------------------------------------
    # Callbacks to any kind of event
    # ------------------------------------------------------------------------

    def ProcessEvent(self, event):
        """
        Processes an event, searching event tables and calling zero or more
        suitable event handler function(s).  Note that the ProcessEvent
        method is called from the wxPython docview framework directly since
        wxPython does not have a virtual ProcessEvent function.

        """
        id = event.GetId()
        logging.debug('Event received %d' % id)
        if id == wx.ID_EXIT:
            self.OnExit(event)
            return True
        elif id == wx.ID_ABOUT:
            self.OnAbout(event)
            return True
        elif id == VIEW_TOOLBAR_ID:
            self.OnViewToolBar(event)
            return True
        elif id == VIEW_STATUSBAR_ID:
            self.OnViewStatusBar(event)
            return True
        elif id == wx.ID_HELP:
            HelpBrowser( self )
            return True
        elif id == wx.ID_ADD:
            self.OnImport(event)
            return True
        elif id == wx.ID_OPEN:
            self.OnOpen(event)
            return True
        elif id == wx.ID_SAVE:
            self.OnSave(event)
            return True
        elif id == ID_GENERATE:
            self.OnGenerate(event)
            return True
        elif id == wx.ID_APPLY:
            self.OnCheck(event)
            return True
        elif id == wx.ID_EDIT:
            self.OnEditData(event)
            return True
        elif id == wx.ID_NEW:
            self.OnNewData(event)
            return True
        elif id == wx.ID_DELETE:
            self.OnDeleteData(event)
            return True
        elif id == ID_HOME:
            self.OnExternalLink(event)
            return True
        elif id == ID_FEEDBACK:
            ShowFeedbackDialog(self)
            return True

        return wx.GetApp().ProcessEvent(event)

    # ------------------------------------------------------------------------

    # ------------------------------------------------------------------------
    # CALLBACKS
    # ------------------------------------------------------------------------

    def ProcessUpdateUIEvent(self, event):
        """
        Processes a UI event, searching event tables and calling zero or more
        suitable event handler function(s). Note that the ProcessEvent
        method is called from the wxPython docview framework directly since
        wxPython does not have a virtual ProcessEvent function.
        """
        id = event.GetId()
        if id == VIEW_TOOLBAR_ID:
            self.OnUpdateViewToolBar(event)
            return True
        elif id == VIEW_STATUSBAR_ID:
            self.OnUpdateViewStatusBar(event)
            return True

        return wx.GetApp().ProcessUpdateUIEvent(event)

    # -----------------------------------------------------------------------
    # Callbacks
    # -----------------------------------------------------------------------

    def OnViewToolBar(self, event):
        """
        Toggles whether the ToolBar is visible.

        """

        try:
            t = self.GetToolBar()
        except Exception:
            # the toolbar was not created with the frame
            return False

        t.Show(not t.IsShown())
        # send size event to force the whole frame layout
        self.SendSizeEvent()

    # ------------------------------------------------------------------------

    def OnUpdateViewToolBar(self, event):
        """
        Updates the View ToolBar menu item.

        """

        try:
            t = self.GetToolBar()
            if t is None: return False
        except Exception:
            # the toolbar was not created with the frame
            return False

        r = t.IsShown()
        event.Check(t.IsShown())
        # send size event to force the whole frame layout
        self.SendSizeEvent()

    # ------------------------------------------------------------------------

    def OnViewStatusBar(self, event):
        """
        Toggles whether the StatusBar is visible.

        """
        try:
            s = self.GetStatusBar()
            if s is None: return False
        except Exception:
            # the statusbar was not created with the frame
            return False

        s.Show(not self.GetStatusBar().IsShown())
        self._LayoutFrame()

    # ------------------------------------------------------------------------

    def OnUpdateViewStatusBar(self, event):
        """
        Updates the View StatusBar menu item.

        """
        try:
            s = self.GetStatusBar()
            if s is None: return False
        except Exception:
            # the statusbar was not created with the frame
            return False

        event.Check(s.IsShown())
        self._LayoutFrame()

    # ------------------------------------------------------------------------

    def OnSize(self, event):
        """
        Called when the frame is resized and lays out the client window.

        """

        self._LayoutFrame()

    # ------------------------------------------------------------------------

    def OnAbout(self, evt):
        """
        Open the about frame.

        """
        wx.AboutBox( self._about )

    # -----------------------------------------------------------------------

    def OnExit(self, evt):
        """
        Close the frame. Check if data have to be saved.
        """
        reallyquit = wx.ID_YES

        if ASK_BEFORE_EXIT is True:
            dlg = wx.MessageDialog(self, "Do you really want to quit?", "Warning", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
            reallyquit = dlg.ShowModal()
        elif self.nbp.IsSaved() is False:
            dlg = wx.MessageDialog(self, "Some changes have not been saved.\nDo you really want to quit?", "Warning", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
            reallyquit = dlg.ShowModal()

        if reallyquit == wx.ID_YES:
            # Clean directory
            for f in os.listdir(os.getcwd()):
                if f.startswith("tmp_"):
                    os.remove(f)

            logging.info("Good bye...")
            self.Destroy()

    # -----------------------------------------------------------------------

    def OnExternalLink(self, evt):
        """
        Open the web browser.

        """
        eid = evt.GetId()
        if eid == ID_HOME:
            url="https://github.com/brigittebigi/proceed"
#         elif eid == ID_DOC:
#             url="http://sldr.org/sldr000800/preview/documentation.html"
#         elif eid == ID_TRACK:
#             url="http://code.google.com/p/sppas/issues/"
#             wx.MessageBox('Your web browser will be opened.\n'
#                           'First, check if the issue is not already declared in the list.\n'
#                           'Then, declare an issue by clicking on the button "New Issue"',
#                              'Info', wx.OK | wx.ICON_INFORMATION)
        else:
            evt.Skip()
            return

        # It seems under some cases when running under windows the call to
        # subprocess in webbrowser will fail and raise an exception here. So
        # simply trap and ignore it.
        try:
            import webbrowser
            webbrowser.open(url,1)
        except:
            pass
    # -----------------------------------------------------------------------

    # -----------------------------------------------------------------------
    # Callbacks to manage the data
    # -----------------------------------------------------------------------

    def OnImport(self, event):
        self.nbp.OnImport(event)

    def OnOpen(self, event):
        self.nbp.OnOpen(event)

    def OnSave(self, event):
        self.nbp.OnSave(event)

    def OnGenerate(self, event):
        self.nbp.OnGenerate(event)

    def OnCheck(self, event):
        self.nbp.OnCheck(event)


    def OnEditData(self, event):
        self.nbp.OnEditSelected(event)

    def OnNewData(self, event):
        self.nbp.OnNewEntry(event)

    def OnDeleteData(self, event):
        self.nbp.OnDeleteSelected(event)

    # -----------------------------------------------------------------------
    # Functions called by the panels
    # -----------------------------------------------------------------------

    def SetSelected(self, selid):
        """
        Get the selected object and update the information panel.
        """
        o = self.nbp.GetObject(selid)
        if o: self.idp.AddContent(o)
        self.GetStatusBar().SetStatusText('An entry is selected.')

    def UnsetSelected(self):
        """
        Clean the information panel content.
        """
        self.idp.CleanContent()
        self.GetStatusBar().SetStatusText('...')

    # -----------------------------------------------------------------------

# ---------------------------------------------------------------------------
