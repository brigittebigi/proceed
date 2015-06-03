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
import logging
import os.path
import wx.lib.scrolledpanel as scrolled

from wxgui.sp_icons import SETTINGS_ICON
from wxgui.sp_icons import SAVE_ICON
from wxgui.sp_icons import APPLY_ICON
from wxgui.sp_icons import CANCEL_ICON
from wxgui.sp_icons import APP_ICON

from wxgui.cutils.imageutils import spBitmap
from wxgui.cutils.ctrlutils import CreateGenButton
import utils.unicode_tex as unicode_tex

from wxgui.sp_consts import FRAME_STYLE
from wxgui.sp_consts import FRAME_TITLE
from wxgui.sp_consts import HEADER_FONTSIZE

from sp_glob import ICONS_PATH

# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------

ID_SAVE   = wx.NewId()

FONT_SIZES  = [10,11,12]
FONT_STYLES = ["\\rm","\\it","\\bf","\\sl","\\sf","\\sc","\\tt"]
PAPER_SIZES = ['a4paper', 'letterpaper', 'legalpaper', 'a5paper', 'executivepaper', 'b5paper']

# ---------------------------------------------------------------------------
# Main Settings Frame class
# ---------------------------------------------------------------------------

class ExportSettings( wx.Dialog ):
    """
    Dialog for the user to fix all settings.

    @author:  Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: This class is used to fix all user's settings, with a Dialog.

    """

    def __init__(self, parent, title, prefs):
        """
        Create a new dialog fo fix preferences, sorted in a notebook.

        """
        wx.Dialog.__init__(self, parent, title=FRAME_TITLE+" - Settings", style=FRAME_STYLE)

        # Members
        self._prefsIO = prefs

        self._create_gui()

        # Events of this frame
        wx.EVT_CLOSE(self, self.onClose)

    # End __init__
    # ------------------------------------------------------------------------

    # ------------------------------------------------------------------------
    # Create the GUI
    # ------------------------------------------------------------------------

    def _create_gui(self):
        self._init_infos()
        self._create_title_label()
        self._create_notebook()
        self._create_save_button()
        self._create_cancel_button()
        self._create_close_button()
        self._layout_components()
        self._set_focus_component()

    # End __init__
    #-------------------------------------------------------------------------

    def _init_infos( self ):
        wx.GetApp().SetAppName( "settings" )
        # icon
        _icon = wx.EmptyIcon()
        _icon.CopyFromBitmap( spBitmap(APP_ICON) )
        self.SetIcon(_icon)

    def _create_title_label(self):
        self.title_layout = wx.BoxSizer(wx.HORIZONTAL)
        bmp = wx.BitmapButton(self, bitmap=spBitmap(SETTINGS_ICON, 32), style=wx.NO_BORDER)
        font = wx.Font(HEADER_FONTSIZE, wx.MODERN, wx.NORMAL, wx.BOLD, False, u'Consolas')
        self.title_label = wx.StaticText(self, label="User settings", style=wx.ALIGN_CENTER)
        self.title_label.SetFont( font )
        self.title_layout.Add(bmp,  flag=wx.TOP|wx.RIGHT|wx.ALIGN_RIGHT, border=5)
        self.title_layout.Add(self.title_label, flag=wx.EXPAND|wx.ALL|wx.wx.ALIGN_CENTER_VERTICAL, border=5)

    def _create_notebook(self):
        self.notebook = wx.Notebook(self)
        self.notebook.AddPage(PageSettings(self.notebook, self._prefsIO),     "  Page  ")
        self.notebook.AddPage(HeaderSettings(self.notebook, self._prefsIO),   " Header ")
        self.notebook.AddPage(FooterSettings(self.notebook, self._prefsIO),   " Footer ")
        self.notebook.AddPage(GenerateSettings(self.notebook, self._prefsIO), "Generate")
        self.notebook.AddPage(TitlesSettings(self.notebook, self._prefsIO),   " Titles ")
        self.notebook.AddPage(OtherSettings(self.notebook, self._prefsIO),    " Others ")

    #-------------------------------------------------------------------------

    def _create_save_button(self):
        bmp = spBitmap(SAVE_ICON)
        self.btn_save = CreateGenButton(self, wx.ID_SAVE, bmp, text="Save", tooltip="Save the settings")
        self.Bind(wx.EVT_BUTTON, self.onSave, self.btn_save, wx.ID_SAVE)

    def _create_cancel_button(self):
        bmp = spBitmap(CANCEL_ICON)
        self.btn_cancel = CreateGenButton(self, wx.ID_CANCEL, bmp, text=" Cancel", tooltip="Close this frame")
        self.SetEscapeId(wx.ID_CANCEL)

    def _create_close_button(self):
        bmp = spBitmap(APPLY_ICON)
        self.btn_close = CreateGenButton(self, wx.ID_OK, bmp, text=" Close", tooltip="Close this frame")
        self.btn_close.SetDefault()
        self.btn_close.SetFocus()
        self.SetAffirmativeId(wx.ID_OK)

    def _create_button_box(self):
        button_box = wx.BoxSizer(wx.HORIZONTAL)
        button_box.Add(self.btn_save, flag=wx.RIGHT, border=5)
        button_box.AddStretchSpacer()
        button_box.Add(self.btn_cancel, flag=wx.RIGHT, border=5)
        button_box.Add(self.btn_close, flag=wx.RIGHT, border=5)
        return button_box

    def _layout_components(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.title_layout, 0, flag=wx.ALL|wx.EXPAND, border=5)
        vbox.Add(self.notebook, 1, flag=wx.ALL|wx.EXPAND, border=0)
        vbox.Add(self._create_button_box(), 0, flag=wx.ALL|wx.EXPAND, border=5)
        self.SetSizerAndFit(vbox)
        self.SetMinSize((420,340))

    def _set_focus_component(self):
        self.notebook.SetFocus()

    #-------------------------------------------------------------------------
    # Callbacks
    #-------------------------------------------------------------------------

    def onSave(self, event):
        """ Save preferences in a file. """

        self._prefsIO.Write()

    def onClose(self, event):
        self.SetEscapeId(wx.ID_CANCEL)

    #-------------------------------------------------------------------------
    # Getters...
    #-------------------------------------------------------------------------

    def GetPreferences(self):
        """ Return the preferences. """

        return self._prefsIO

    #-------------------------------------------------------------------------

# ----------------------------------------------------------------------------

class PageSettings( wx.Panel ):

    def __init__(self, parent, prefsIO):

        wx.Panel.__init__(self, parent)
        self.preferences = prefsIO
        sizer = wx.BoxSizer(wx.VERTICAL)

        pf = wx.RadioBox(self, label="Paper format: ", choices=PAPER_SIZES, majorDimension=3)
        pf.SetSelection( PAPER_SIZES.index( self.preferences.GetValue('PAGE_FORMAT') ) )
        pf.Bind(wx.EVT_RADIOBOX, self.onPaperFormat)
        sizer.Add(pf, 0, flag=wx.ALL, border=0)

        keys = ['PAGE_NUMBER', 'TOP_MARGIN', 'BOTTOM_MARGIN', 'HEADER_SIZE', 'FOOTER_SIZE']
        for k in keys:
            pn = wx.SpinCtrl(self, value=str(self.preferences.GetValue(k)))
            pn.SetRange(1, 40)
            pn.Bind(wx.EVT_SPINCTRL, lambda evt, skey=self.preferences.GetValue(k), stype='int': self.onPrefsChange(evt, skey, stype) )
            spn = wx.BoxSizer( wx.HORIZONTAL )
            spn.Add(wx.StaticText(self, label=self.preferences.GetText(k)+':', size=(150,-1)), 0, flag=wx.ALL, border=0)
            spn.Add(pn, 0, flag=wx.ALL, border=0)
            sizer.Add(spn, 0, flag=wx.ALL, border=0)
            sizer.Add((-1, 10))
        self.SetSizer(sizer)

    def onPrefsChange(self, event, skey, stype):
        o = event.GetEventObject()
        logging.debug(' Set pref: key=%s, newvalue=%s'%(skey,str(o.GetValue())))
        self.preferences.SetValue( skey, stype, o.GetValue() )

    def onPaperFormat(self, event):
        o = event.GetEventObject()
        idx = o.GetSelection()
        self.preferences.SetValue( 'PAGE_FORMAT', 'str', PAPER_SIZES[idx] )

#-----------------------------------------------------------------------------

class HeaderSettings( wx.Panel ):

    def __init__(self, parent, prefsIO):

        wx.Panel.__init__(self, parent)
        self.preferences = prefsIO
        sizer = wx.BoxSizer(wx.VERTICAL)
        titleall = ["HEADER_LEFT", "HEADER_CENTER", "HEADER_RIGHT", "HEADER_COLOR"]
        for gen in titleall:
            s = wx.BoxSizer( wx.HORIZONTAL )
            txt = wx.TextCtrl(self, -1, "", size=wx.Size(280,-1), style=wx.TE_LEFT)
            txt.WriteText( self.preferences.GetValue(gen) )
            txt.Bind(wx.EVT_TEXT, lambda evt, skey=gen, stype='str': self.onPrefsChange(evt, skey, stype) )
            s.Add(wx.StaticText(self, label=self.preferences.GetText(gen), size=(150,-1)), 1, flag=wx.ALL, border=0)
            s.Add(txt, 1, flag=wx.ALL, border=0)
            sizer.Add(s, 0, flag=wx.ALL, border=0)
            sizer.Add((-1, 10))

        pf = wx.RadioBox(self, label=self.preferences.GetText("HEADER_STYLE"), choices=FONT_STYLES, majorDimension=8)
        pf.SetSelection( FONT_STYLES.index( self.preferences.GetValue("HEADER_STYLE") ) )
        pf.Bind(wx.EVT_RADIOBOX, self.onHeaderStyle)
        sizer.Add(pf, 0, flag=wx.ALL, border=0)
        sizer.Add((-1, 10))

        cbp = wx.CheckBox(self, label=self.preferences.GetText('HEADER_RULER'), size=(300,-1))
        cbp.SetValue(self.preferences.GetValue('HEADER_RULER'))
        cbp.Bind(wx.EVT_CHECKBOX, self.onRulerChange)
        sizer.Add(cbp, 0, flag=wx.ALL, border=0)

        self.SetSizer(sizer)

    def onHeaderStyle(self, event):
        o = event.GetEventObject()
        idx = o.GetSelection()
        logging.debug(' Set pref: key=HEADER_STYLE, newvalue=%s'%FONT_STYLES[idx])
        self.preferences.SetValue( "HEADER_STYLE", "str", FONT_STYLES[idx] )

    def onRulerChange(self, event):
        o = event.GetEventObject()
        v = o.GetValue()
        logging.debug(' Set pref: key=HEADER_RULER, newvalue=%s'%v)
        self.preferences.SetValue( 'HEADER_RULER', 'bool', bool(v) )

    def onPrefsChange(self, event, skey, stype):
        o = event.GetEventObject()
        v = unicode_tex.unicode_to_tex(o.GetValue()) # accents must be in standard LaTeX
        logging.debug(' Set pref: key=%s, newvalue=%s'%(skey,v))
        self.preferences.SetValue( skey, stype, v )

#-----------------------------------------------------------------------------

class FooterSettings( wx.Panel ):

    def __init__(self, parent, prefsIO):

        wx.Panel.__init__(self, parent)
        self.preferences = prefsIO
        sizer = wx.BoxSizer(wx.VERTICAL)
        titleall = ["FOOTER_LEFT", "FOOTER_CENTER", "FOOTER_RIGHT", "FOOTER_COLOR"]
        for gen in titleall:
            s = wx.BoxSizer( wx.HORIZONTAL )
            txt = wx.TextCtrl(self, -1, "", size=wx.Size(280,-1), style=wx.TE_LEFT)
            txt.WriteText( self.preferences.GetValue(gen) )
            txt.Bind(wx.EVT_TEXT, lambda evt, skey=gen, stype='str': self.onPrefsChange(evt, skey, stype) )
            s.Add(wx.StaticText(self, label=self.preferences.GetText(gen), size=(150,-1)), 1, flag=wx.ALL, border=0)
            s.Add(txt, 1, flag=wx.ALL, border=0)
            sizer.Add(s, 0, flag=wx.ALL, border=0)

        pf = wx.RadioBox(self, label=self.preferences.GetText("FOOTER_STYLE"), choices=FONT_STYLES, majorDimension=8)
        pf.SetSelection( FONT_STYLES.index( self.preferences.GetValue("FOOTER_STYLE") ) )
        pf.Bind(wx.EVT_RADIOBOX, self.onFooterStyle)
        sizer.Add(pf, 0, flag=wx.ALL, border=0)

        cbp = wx.CheckBox(self, label=self.preferences.GetText('FOOTER_RULER'), size=(300,-1))
        cbp.SetValue(self.preferences.GetValue('FOOTER_RULER'))
        cbp.Bind(wx.EVT_CHECKBOX, self.onRulerChange )
        sizer.Add(cbp, 0, flag=wx.ALL, border=0)

        self.SetSizer(sizer)

    def onFooterStyle(self, event):
        o = event.GetEventObject()
        idx = o.GetSelection()
        logging.debug(' Set pref: key=FOOTER_STYLE, newvalue=%s'%FONT_STYLES[idx])
        self.preferences.SetValue( "FOOTER_STYLE", "str", FONT_STYLES[idx] )

    def onRulerChange(self, event):
        o = event.GetEventObject()
        v = o.GetValue()
        logging.debug(' Set pref: key=FOOTER_RULER, newvalue=%s'%v)
        self.preferences.SetValue( 'FOOTER_RULER', 'bool', bool(v) )

    def onPrefsChange(self, event, skey, stype):
        o = event.GetEventObject()
        v = unicode_tex.unicode_to_tex(o.GetValue()) # accents must be in standard LaTeX
        logging.debug(' Set pref: key=%s, newvalue=%s'%(skey,v))
        self.preferences.SetValue( skey, stype, v )

#-----------------------------------------------------------------------------

class GenerateSettings( wx.Panel ):

    def __init__(self, parent, prefsIO):

        wx.Panel.__init__(self, parent)
        self.preferences = prefsIO
        sizer = wx.BoxSizer(wx.VERTICAL)
        genall = ["GENERATE_PROGRAM", "GENERATE_PROGRAM_OVERVIEW", "GENERATE_TABLEOFCONTENTS", "GENERATE_MERGED_SUBMISSIONS", "GENERATE_AUTHORS_INDEX", "GENERATE_AUTHORS_LIST"]
        for gen in genall:
            cbp = wx.CheckBox(self, label=self.preferences.GetText(gen), size=(300,-1))
            cbp.SetValue(self.preferences.GetValue(gen))
            cbp.Bind(wx.EVT_CHECKBOX, lambda evt, skey=gen, stype='bool': self.onPrefsChange(evt, skey, stype) )
            sizer.Add(cbp, 0, flag=wx.ALL, border=0)
        self.SetSizer(sizer)

    def onPrefsChange(self, event, skey, stype):
        o = event.GetEventObject()
        logging.debug(' Set pref: key=%s, newvalue=%s'%(skey,str(o.GetValue())))
        self.preferences.SetValue( skey, stype, o.GetValue() )

#-----------------------------------------------------------------------------

class TitlesSettings( wx.Panel ):

    def __init__(self, parent, prefsIO):

        wx.Panel.__init__(self, parent)
        self.preferences = prefsIO
        sizer = wx.BoxSizer(wx.VERTICAL)
        titleall = ["TITLE_PROGRAM", "TITLE_PROGRAM_OVERVIEW", "TITLE_TABLEOFCONTENTS", "TITLE_AUTHORS_INDEX", "TITLE_AUTHORS_LIST"]
        for gen in titleall:
            s = wx.BoxSizer( wx.HORIZONTAL )
            txt = wx.TextCtrl(self, -1, "", size=wx.Size(300,-1), style=wx.TE_LEFT)
            txt.WriteText( self.preferences.GetValue(gen) )
            txt.Bind(wx.EVT_TEXT, lambda evt, skey=gen, stype='str': self.onPrefsChange(evt, skey, stype) )
            s.Add(wx.StaticText(self, label=self.preferences.GetText(gen), size=(120,-1)), 1, flag=wx.ALL, border=0)
            s.Add(txt, 1, flag=wx.ALL, border=0)
            sizer.Add(s, 0, flag=wx.ALL, border=0)
            sizer.Add((-1, 10))
        self.SetSizer(sizer)

    def onPrefsChange(self, event, skey, stype):
        o = event.GetEventObject()
        v = unicode_tex.unicode_to_tex(o.GetValue()) # accents must be in standard LaTeX
        logging.debug(' Set pref: key=%s, newvalue=%s'%(skey,v))
        self.preferences.SetValue( skey, stype, v )

#-----------------------------------------------------------------------------

class OtherSettings( wx.Panel ):

    def __init__(self, parent, prefsIO):

        wx.Panel.__init__(self, parent)
        self.preferences = prefsIO
        sizer = wx.BoxSizer(wx.VERTICAL)

        sm = ['Follow the planning', 'By session types first then follow the planning']
        pf = wx.RadioBox(self, label="Sort method for submissions: ", choices=sm, majorDimension=1)
        pf.SetSelection( int( self.preferences.GetValue("SORT_BY_SESSION_TYPE_FIRST") ) )
        pf.Bind(wx.EVT_RADIOBOX, self.onSessionSort)
        sizer.Add(pf, 0, flag=wx.ALL, border=0)
        sizer.Add((-1, 10))

        colorall = ["COLOR_1", "COLOR_2", "COLOR_3"]
        for gen in colorall:
            s = wx.BoxSizer( wx.HORIZONTAL )
            txt = wx.TextCtrl(self, -1, "", size=wx.Size(280,-1), style=wx.TE_LEFT)
            txt.WriteText( self.preferences.GetValue(gen) )
            txt.Bind(wx.EVT_TEXT, lambda evt, skey=gen, stype='str': self.onPrefsChange(evt, skey, stype) )
            s.Add(wx.StaticText(self, label=self.preferences.GetText(gen), size=(150,-1)), 1, flag=wx.ALL, border=0)
            s.Add(txt, 1, flag=wx.ALL, border=0)
            sizer.Add(s, 0, flag=wx.ALL, border=0)
        self.SetSizer(sizer)

    def onSessionSort(self, event):
        o = event.GetEventObject()
        idx = o.GetSelection()
        logging.debug(' Set pref: key=SORT_BY_SESSION_TYPE_FIRST, newvalue=%s'%(bool(idx)))
        self.preferences.SetValue( 'SORT_BY_SESSION_TYPE_FIRST', 'bool', bool(idx) )

    def onPrefsChange(self, event, skey, stype):
        o = event.GetEventObject()
        v = o.GetValue() # accents must be in standard LaTeX
        logging.debug(' Set pref: key=%s, newvalue=%s'%(skey,v))
        self.preferences.SetValue( skey, stype, v )

#-----------------------------------------------------------------------------
