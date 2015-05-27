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

import wx
import wx.lib.newevent
import wx.wizard
import logging
import os.path
import sys
sys.path.append( os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname( os.path.abspath(__file__))))), "src") )


from wxgui.cutils.imageutils import spBitmap
from wxgui.sp_consts import HEADER_FONTSIZE
from wxgui.sp_consts import FRAME_STYLE
from wxgui.sp_consts import FRAME_TITLE
from wxgui.sp_icons  import IMPORT_EXPORT_ICON
from wxgui.sp_icons  import GRID_ICON
from wxgui.sp_icons  import TEX_ICON
from wxgui.sp_icons  import WWW_ICON

from DataIO.Read.reader import Reader
from DataIO.Write.writer import Writer
from structs.prefs import Preferences
from structs.abstracts_themes import all_themes
from wxgui.frames.processprogress import ProcessProgressDialog

# ---------------------------------------------------------------------------
ImportFinishedEvent, EVT_IMPORT_WIZARD_FINISHED = wx.lib.newevent.NewEvent()
ImportFinishedCommandEvent, EVT_IMPORT_WIZARD_FINISHED_COMMAND = wx.lib.newevent.NewCommandEvent()
# ---------------------------------------------------------------------------

class ImportWizard( wx.wizard.Wizard ):

    def __init__(self, parent):
        wx.wizard.Wizard.__init__(self, parent, -1)#, title=FRAME_TITLE+" - Import", style=FRAME_STYLE)
        self.output = ""

        self.page0 = InputPage(self)
        self.page0.SetName("input")
        self.page1 = OutputPage(self)
        self.page1.SetName("output")
        self.page2 = LatexPage(self)
        self.page2.SetName("latex")

        wx.wizard.WizardPageSimple.Chain(self.page0, self.page1)
        wx.wizard.WizardPageSimple.Chain(self.page1, self.page2)

        self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGED, self.onPageChanged)
        self.Bind(wx.wizard.EVT_WIZARD_FINISHED, self.onFinished)

        wx.CallAfter(self.SetSize,(520,440))
        self.RunWizard(self.page0)
        self.Destroy()

    #----------------------------------------------------------------------
    def onPageChanged(self, event):
        """"""
        page = event.GetPage()

        if page.GetName() == "output":
            if not os.path.exists(self.page0.urlFld.GetValue()):
                wx.MessageBox("A valid input file name is required.", 'Info', wx.OK | wx.ICON_INFORMATION)
                self.RunWizard(self.page0)
                return
            else:
                p = ProcessProgressDialog(self)
                arguments = {}
                arguments['readername']      = self.page0.confname
                arguments['filename']        = self.page0.urlFld.GetValue()
                arguments['authorsfilename'] = self.page0.urlauthFld.GetValue()
                arguments['progress'] = p
                try:
                    self.reader = Reader( arguments )
                    p.close()
                except Exception as e:
                    wx.MessageBox("Error while reading file:\n%s"%str(e), 'Info', wx.OK | wx.ICON_INFORMATION)
                    self.Destroy()

        elif page.GetName() == "latex":
#             if len(self.page1.urlFld.GetValue().strip()):
#                 wx.MessageBox("A directory is required.", 'Info', wx.OK | wx.ICON_INFORMATION)
#                 self.RunWizard(self.page1)
#                 return
            self.output = self.page1.urlFld.GetValue().strip()

            if not os.path.exists( self.output ):
                try:
                    os.mkdir( self.output )
                except Exception as e:
                    wx.MessageBox("Error while creating output directory:\n%s"%str(e), 'Info', wx.OK | wx.ICON_INFORMATION)
                    self.RunWizard(self.page1)
                    return
            try:
                self.writer = Writer( self.reader.docs )
                self.writer.set_status( self.page1.status )
                if self.page1.exportcsv:
                    self.writer.writeCSV( self.output )
                if self.page1.exporthtml:
                    self.writer.writeHTML( self.output )
            except Exception as e:
                wx.MessageBox("Error while creating output files:\n%s"%str(e), 'Info', wx.OK | wx.ICON_INFORMATION)
                self.RunWizard(self.page1)
                return

    #----------------------------------------------------------------------
    def onFinished(self, event):
        """"""
        if self.page2.export is True:

            # Create preferences
            prefs = Preferences()
            theme = all_themes.get_theme( self.page2.theme )
            prefs.SetTheme( theme )
            prefs.SetValue('COMPILER', 'str', self.page2.compiler.strip())
            # Write as LaTeX in the same dir as proceed CSV files
            p = ProcessProgressDialog(self)
            self.writer.set_progress(p)
            self.writer.writeLaTeX_as_Dir( self.output, prefs )
            self.writer.set_progress(None)
            p.close()

        evt = ImportFinishedEvent(path=self.output)
        evt.SetEventObject(self)
        wx.PostEvent(self.GetParent(), evt)

    #----------------------------------------------------------------------

# ----------------------------------------------------------------------------

class InputPage(wx.wizard.WizardPageSimple):
    """ Parameters for the input data. """

    def __init__(self, parent):
        """
        Constructor.
        """
        wx.wizard.WizardPageSimple.__init__(self, parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.dirname = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

        title_layout = wx.BoxSizer(wx.HORIZONTAL)
        bmp = wx.BitmapButton(self, bitmap=spBitmap(IMPORT_EXPORT_ICON, 32), style=wx.NO_BORDER)
        font = wx.Font(HEADER_FONTSIZE, wx.MODERN, wx.NORMAL, wx.BOLD, False, u'Consolas')
        title_label = wx.StaticText(self, label="File to import and related information:", style=wx.ALIGN_CENTER)
        title_label.SetFont( font )
        title_layout.Add(bmp,  flag=wx.TOP|wx.RIGHT|wx.ALIGN_RIGHT, border=5)
        title_layout.Add(title_label, flag=wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=5)
        sizer.Add(title_layout, 0, flag=wx.ALL, border=0)
        sizer.Add((-1, 10))

        # --------- Conference web site
        confnames = ['sciencesconf', 'easychair']
        self.confname = 'sciencesconf'
        readername = wx.RadioBox(self, label="    The file to import comes from:     ", size=(410,-1), choices=confnames, majorDimension=1)
        readername.SetSelection( 0 )
        readername.Bind(wx.EVT_RADIOBOX, self.onConfName)
        sizer.Add(readername, 0, flag=wx.ALL, border=0)
        sizer.Add((-1, 10))

        # --------- Input file name
        hBox = wx.BoxSizer(wx.HORIZONTAL)
        hBox.Add(wx.StaticText(self, label="File name:", size=(100,30)), flag=wx.TOP|wx.ALIGN_CENTER_VERTICAL, border=5)
        self.urlFld = wx.TextCtrl(self, size=(300,30))
        hBox.Add(self.urlFld, 1, flag=wx.LEFT, border=2)
        checkBtn = wx.Button(self, -1, "Choose...", size=(80,30))
        checkBtn.Bind(wx.EVT_BUTTON, lambda evt, temp="input": self.onOpen(evt, temp) )
        hBox.Add(checkBtn, 0, flag=wx.LEFT, border=10)
        sizer.Add(hBox, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP)
        sizer.Add((-1, 10))

        # --------- Input file name for authors
        hBox = wx.BoxSizer(wx.HORIZONTAL)
        self.authtext = wx.StaticText(self, label="Authors file:", size=(100,30))
        hBox.Add(self.authtext, flag=wx.TOP|wx.ALIGN_CENTER_VERTICAL, border=5)
        self.urlauthFld = wx.TextCtrl(self, size=(300,30))
        hBox.Add(self.urlauthFld, 1, flag=wx.LEFT, border=2)
        self.checkauthBtn = wx.Button(self, -1, "Choose...", size=(80,30))
        self.checkauthBtn.Bind(wx.EVT_BUTTON, lambda evt, temp="author": self.onOpen(evt, temp) )
        hBox.Add(self.checkauthBtn, 0, flag=wx.LEFT, border=10)
        sizer.Add(hBox, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP)

        self.enable()

        self.SetSizer(sizer)

    def onOpen(self, event, temp):
        filename = self.file_open()
        if filename:
            if temp == "input":
                self.urlFld.SetValue(filename)
            else:
                self.urlauthFld.SetValue(filename)

    def onConfName(self, event):
        o = event.GetEventObject()
        self.confname = o.GetStringSelection()
        self.enable()

    def enable(self):
        if self.confname == 'easychair':
            self.authtext.SetForegroundColour( wx.Colour(180,80,80))
            self.checkauthBtn.Enable(True)
        else:
            self.authtext.SetForegroundColour( wx.Colour(128,128,128))
            self.checkauthBtn.Enable(False)

    def file_open(self):
        with wx.FileDialog(self, "Choose a file to import", self.dirname,
                           "", "*.*", wx.OPEN) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                directory, filename = dlg.GetDirectory(), dlg.GetFilename()
                return os.path.join(directory, filename)
        return None


# ----------------------------------------------------------------------------

class OutputPage(wx.wizard.WizardPageSimple):
    """ Parameters for the output data. """

    def __init__(self, parent):
        """
        Constructor.
        """
        wx.wizard.WizardPageSimple.__init__(self, parent)
        self.urlFld = ""
        self.dirname = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

        sizer = wx.BoxSizer(wx.VERTICAL)

        title_layout = wx.BoxSizer(wx.HORIZONTAL)
        bmp = wx.BitmapButton(self, bitmap=spBitmap(GRID_ICON, 32), style=wx.NO_BORDER)
        font = wx.Font(HEADER_FONTSIZE, wx.MODERN, wx.NORMAL, wx.BOLD, False, u'Consolas')
        title_label = wx.StaticText(self, label="Where to save:", style=wx.ALIGN_CENTER)
        title_label.SetFont( font )
        title_layout.Add(bmp,  flag=wx.TOP|wx.RIGHT|wx.ALIGN_RIGHT, border=5)
        title_layout.Add(title_label, flag=wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=5)
        sizer.Add(title_layout, 0, flag=wx.ALL, border=0)
        sizer.Add((-1, 10))

        # --------- Output directory
        hBox = wx.BoxSizer(wx.HORIZONTAL)
        hBox.Add(wx.StaticText(self, label="Directory:", size=(100,30)), flag=wx.TOP|wx.ALIGN_CENTER_VERTICAL, border=5)
        self.urlFld = wx.TextCtrl(self, size=(300,30))
        hBox.Add(self.urlFld, 1, flag=wx.LEFT, border=2)
        checkBtn = wx.Button(self, -1, "Choose...", size=(80,30))
        checkBtn.Bind(wx.EVT_BUTTON, self.onDirectory )
        hBox.Add(checkBtn, 0, flag=wx.LEFT, border=10)
        sizer.Add(hBox, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP)
        sizer.Add((-1, 10))
        self.SetSizer(sizer)

        # ---------- Status
        allstatus = ['all papers', 'only accepted papers']
        self.status = 1
        statusradio = wx.RadioBox(self, label="    Choose papers to save:     ", size=(410,-1), choices=allstatus, majorDimension=1)
        statusradio.SetSelection( 1 )
        statusradio.Bind(wx.EVT_RADIOBOX, self.onStatus)
        sizer.Add(statusradio, 0, flag=wx.ALL, border=0)
        sizer.Add((-1, 20))

        # ----------CSV
        self.exportcsv = True
        cbp = wx.CheckBox(self, label="Save as CSV files for Proceed", size=(300,-1))
        cbp.SetValue(True)
        cbp.Bind(wx.EVT_CHECKBOX, self.onExportAsCSV)
        sizer.Add(cbp, 0, flag=wx.LEFT, border=0)
        sizer.Add((-1, 10))

        # ----------HTML
        self.exporthtml = False
        cbp = wx.CheckBox(self, label="Save the list of papers in HTML", size=(300,-1))
        cbp.SetValue(False)
        cbp.Bind(wx.EVT_CHECKBOX, self.onExportAsHTML)
        sizer.Add(cbp, 0, flag=wx.LEFT, border=0)

    def onDirectory(self, event):
        with wx.DirDialog(self, "Choose a directory to save in", self.dirname, style=wx.DD_CHANGE_DIR) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.urlFld.SetValue( dlg.GetPath() )

    def onStatus(self, event):
        o = event.GetEventObject()
        self.status = o.GetSelection()

    def onExportAsCSV(self, event):
        o = event.GetEventObject()
        self.exportcsv = bool( o.GetValue() )

    def onExportAsHTML(self, event):
        o = event.GetEventObject()
        self.exporthtml = bool( o.GetValue() )

# ----------------------------------------------------------------------------

class LatexPage(wx.wizard.WizardPageSimple):
    """ Process the data. """

    def __init__(self, parent):
        """
        Constructor.
        """
        wx.wizard.WizardPageSimple.__init__(self, parent)
        self.urlFld = ""
        self.dirname = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

        sizer = wx.BoxSizer(wx.VERTICAL)

        title_layout = wx.BoxSizer(wx.HORIZONTAL)
        bmp = wx.BitmapButton(self, bitmap=spBitmap(GRID_ICON, 32), style=wx.NO_BORDER)
        font = wx.Font(HEADER_FONTSIZE, wx.MODERN, wx.NORMAL, wx.BOLD, False, u'Consolas')
        title_label = wx.StaticText(self, label="Save abstracts as LaTeX...", style=wx.ALIGN_CENTER)
        title_label.SetFont( font )
        title_layout.Add(bmp,  flag=wx.TOP|wx.RIGHT|wx.ALIGN_RIGHT, border=5)
        title_layout.Add(title_label, flag=wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=5)
        sizer.Add(title_layout, 0, flag=wx.ALL, border=0)
        sizer.Add((-1, 10))

        # ----------CHECK
        self.export = False
        cbp = wx.CheckBox(self, label="Create each abstract as a LaTeX file", size=(300,-1))
        cbp.SetValue(False)
        cbp.Bind(wx.EVT_CHECKBOX, self.onExport)
        sizer.Add(cbp, 0, flag=wx.LEFT, border=0)
        sizer.Add((-1, 10))

        # ------------- Theme
        self.theme = all_themes.get_theme('basic')
        self.themeradio = wx.RadioBox(self, label="    Choose a style:     ", size=(410,-1), choices=all_themes.get_themes().keys(), majorDimension=1)
        self.themeradio.SetSelection( 0 )
        self.themeradio.Bind(wx.EVT_RADIOBOX, self.onTheme)
        sizer.Add(self.themeradio, 0, flag=wx.LEFT, border=40)
        sizer.Add((-1, 10))

        # ------------- Compiler
        self.compilers = ['pdflatex', 'xetex']
        self.compiler = 'pdflatex'
        self.comradio = wx.RadioBox(self, label="    Choose the LaTeX compiler:     ", size=(410,-1), choices=self.compilers, majorDimension=1)
        self.comradio.SetSelection( 0 )
        self.comradio.Bind(wx.EVT_RADIOBOX, self.onCompiler)
        sizer.Add(self.comradio, 0, flag=wx.LEFT, border=40)
        sizer.Add((-1, 10))

        # ------------- PDF
        self.pdf = True
        self.cbp = wx.CheckBox(self, label="Compile the LaTeX files", size=(300,-1))
        self.cbp.SetValue(True)
        self.cbp.Bind(wx.EVT_CHECKBOX, self.onPDFChange)
        sizer.Add(self.cbp, 0, flag=wx.LEFT, border=40)

        self.enable(False)
        self.SetSizer(sizer)

    def onCompiler(self, event):
        o = event.GetEventObject()
        self.compiler = o.GetStringSelection()

    def onTheme(self, event):
        o = event.GetEventObject()
        self.theme = o.GetStringSelection()

    def onPDFChange(self, event):
        o = event.GetEventObject()
        self.pdf.SetValue( o.GetValue() )

    def onExport(self, event):
        o = event.GetEventObject()
        self.export = bool( o.GetValue() )
        self.enable(self.export)

    def enable(self, value):
        if value is False:
            self.themeradio.SetForegroundColour(wx.Colour(128,128,128))
            self.comradio.SetForegroundColour(wx.Colour(128,128,128))
        else:
            self.themeradio.SetForegroundColour(wx.Colour(80,80,200))
            self.comradio.SetForegroundColour(wx.Colour(80,80,200))
        for i in range(len(all_themes.get_themes().keys())):
            self.themeradio.EnableItem(i,value)
        for i in range(len(self.compilers)):
            self.comradio.EnableItem(i,value)
        self.cbp.Enable(value)

# ----------------------------------------------------------------------------

class HTMLPage(wx.wizard.WizardPageSimple):
    """ Diagnosis of the PDF for the output data. """

    def __init__(self, parent):
        """
        Constructor.
        """
        wx.wizard.WizardPageSimple.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

# ----------------------------------------------------------------------------

if __name__ == "__main__":
    app = wx.App(False)
    ImportWizard(None)
    app.MainLoop()

#----------------------------------------------------------------------
