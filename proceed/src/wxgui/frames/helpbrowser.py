#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# ---------------------------------------------------------------------------
#            ___   __    __    __    ___
#           /     |  \  |  \  |  \  /        Automatic
#           \__   |__/  |__/  |___| \__      Annotation
#              \  |     |     |   |    \     of
#           ___/  |     |     |   | ___/     Speech
#           =============================
#
#           http://sldr.org/sldr000800/preview/
#
# ---------------------------------------------------------------------------
# developed at:
#
#       Laboratoire Parole et Langage
#
#       Copyright (C) 2011-2015  Brigitte Bigi
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
# ----------------------------------------------------------------------------
# File: helpbrowser.py
# ----------------------------------------------------------------------------

__docformat__ = """epytext"""
__authors__   = """Brigitte Bigi"""
__copyright__ = """Copyright (C) 2011-2015  Brigitte Bigi"""


# -------------------------------------------------------------------------
# Imports
# -------------------------------------------------------------------------

import codecs
import os.path
import re
import wx
import wx.html
import webbrowser

from dependencies.markdown import markdown
from dependencies.markdown.extensions.tables import TableExtension
from dependencies.markdown.extensions.fenced_code import FencedCodeExtension
from dependencies.markdown.extensions.codehilite import CodeHiliteExtension

from wxgui.sp_icons import APP_ICON
from wxgui.sp_icons import HELP_ICON
from wxgui.sp_icons import LOGOUT_ICON
from wxgui.sp_icons import HOME_ICON
from wxgui.sp_icons import FORWARD_ICON
from wxgui.sp_icons import BACKWARD_ICON
from wxgui.sp_icons import NEXT_ICON
from wxgui.sp_icons import PREVIOUS_ICON
from wxgui.cutils.imageutils import spBitmap

from wxgui.sp_consts import HELP_PATH
from wxgui.sp_consts import DOC_IDX
from wxgui.sp_consts import HELP_IDX_EXT
from wxgui.sp_consts import BUTTON_ICONSIZE

from wxgui.sp_consts import FRAME_STYLE
from wxgui.sp_consts import FRAME_TITLE


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

HOME_ID     = wx.NewId()
BACKWARD_ID = wx.NewId()
FORWARD_ID  = wx.NewId()
PREVIOUS_ID = wx.NewId()
NEXT_ID     = wx.NewId()


# ---------------------------------------------------------------------------
# Functions

def format_title(content):
    title = ' '.join(content)
    title = title.replace('#', '').strip()
    return title

def format_header(content):
    header = content.replace('#', '').strip()
    return header

def format_body(content):
    body = ' '.join(content)
    return body

def load_page(url_md):
    """
    Load a page. Expected Utf-8 encoding.
    @param url_md Filename of a markdown file.
    @return List of lines
    """
    try:
        with codecs.open(url_md, 'r', 'utf-8') as fd:
            content = fd.readlines()
    except Exception:
        content = ["No documentation available for this page."]

    return content

# End
# ---------------------------------------------------------------------------



# ---------------------------------------------------------------------------
# One page of the HelpSystem
# ---------------------------------------------------------------------------


class HelpPage( object ):
    """
    @author:  Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL, v3
    @summary: One page of a wiki-like help system.

    Convert the original markdown file into html.

    """

    def __init__(self, help_system, id, header, body):
        """
        Create a page.

        @param help_system (HelpSystem) is the parent
        @param id (string) identifier of the page
        @param header (string) top header of the page
        @param body(string) body of the page (markdown format)

        """
        self.help_system = help_system
        self.id     = id
        self.header = header
        self.body   = body

    # End __init__
    # -----------------------------------------------------------------------


    def _patch_html(self, html_body):
        """
        Patch html for blocks of code.
        """
        # Patch for Source code
        incode = ""
        tab_body = html_body.split('\n')
        html_body = ""
        for line in tab_body:
            # End of code
            if len(incode)>0 and "~~~" in line:
                incode = ""
                html_body += "</font></code></pre></td></tr></TABLE>\n"
                continue
            elif "~~~" in line:
                if len(incode)==0:
                    incode = "yes"
                if "python" in line.lower():
                    incode = "python"
                html_body += "<TABLE border=1 width=90%><tr><td bgcolor='#D8D8D8'><pre><code><font color='#464646'>\n"
                continue

            if incode == "python":
                comment = ""
                commentline = line.find('# ')
                if commentline>-1:
                    comment = "<font color='#497747'>" + line[commentline:] + "</font>"
                    line = line[:commentline-1]
                line = line.replace('"""', '<font color="#CA1C25">"""</font>')
                line = line.replace('@param ', '<font color="#CA1C25">@param </font>')
                line = line.replace('@return ', '<font color="#CA1C25">@return </font>')
                line = line.replace('import ', "<font color='#75A094'>import</font> ")
                line = line.replace('from ', "<font color='#75A094'>from</font> ")
                line = line.replace('def ', "<font color='#1C26CA'>def</font> ")
                line = line.replace('elif ', "<font color='#1C26CA'>elif</font> ")
                line = line.replace('if ', "<font color='#1C26CA'>if</font> ")
                line = line.replace('else:', "<font color='#1C26CA'>else:</font>")
                line = line.replace('print ', "<font color='#1C26CA'>print</font> ")
                line = line.replace(' in ', "<font color='#1C26CA'> in</font> ")
                line = line.replace(' and ', "<font color='#1C26CA'> and</font> ")
                line = line.replace(' or ', "<font color='#1C26CA'> or</font> ")
                line = line.replace('for ', "<font color='#1C26CA'>for</font> ")
                if "if" in line and "name" in line and "main" in line:
                    line = "<font color='#1C26CA'>if</font> <bold>__name__</bold> == <bold>'__main__'</bold>:"

                line = line + comment

            # Other patch for h4 titles
            elif line.find('####')>-1:
                line = line.replace("####","")
                line = "<h4>"+line+"</h4>"

            html_body += line+"\n"

        return html_body


    def GetHtml(self):
        """
        Get the page content in html (version 3) format.

        @return string

        """

        html_body = markdown(self.body, output_format="html4", extensions=[TableExtension()]) #,FencedCodeExtension()])

        # Change headers
        # Our link markup: Replace Help(foo) with proper link
        while True:
            match = re.search(r"Help\(([^)]+)\)", html_body)
            if match:
                page = self.help_system.GetPage(match.group(1))
                replacement = "??"
                if page:
                    replacement = "<a href=\"%s%s\">%s</a>" % (
                        self.help_system.page_prefix,
                        match.group(1), page.header)
                html_body = html_body[0:match.start(0)] + replacement + \
                       html_body[match.end(0):]
            else:
                break

        while True:
            match = re.search(r"Color\(([^)]+)\)", html_body)
            if match:
                replacement = "<font color=\"red\">%s</font>" %match.group(1)
                html_body = html_body[0:match.start(0)] + replacement + \
                       html_body[match.end(0):]
            else:
                break

        # Ensure image path (in our md files, each image path starts by "./etc")
        html_body = html_body.replace('./etc', HELP_PATH)

        # Code
        html_body = self._patch_html(html_body)

        return u"<h1>%s</h1>\n%s" % (self.header,html_body)

# End HelpPage
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# HelpSystem
# ---------------------------------------------------------------------------


class HelpSystem( object ):
    """
    @author:  Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: A wiki-like help system: data of the pages.

    """

    def __init__(self, resources_prefix, page_prefix):
        """
        Create a new HelpSystem.

        @param resources_prefix
        @param page_prefix

        """
        self.pages = {}
        self.ranks = [] # used if pages are ranked
        self.resources_prefix = resources_prefix
        self.page_prefix = page_prefix
        self._install_page(id=str(HOME_ID), header="Help content", body="")

    # End __init__
    # -----------------------------------------------------------------------


    def _get_pages_matching_search(self, search):
        search_words = search.split(" ")
        content_res = [r"\b%s\b" % x for x in search_words]
        matches = []
        for page in self.pages.values():
            match = True
            for content_re in content_res:
                if (not re.search(content_re, page.header, re.IGNORECASE) and
                    not re.search(content_re, page.body, re.IGNORECASE)):
                    match = False
                    break
            if match:
                matches.append(page)
        return matches

    # ------------------------------------------------------------------------


    def _install_page(self, id, header="", body=""):
        """
        Create a new HelpPage and store it into the dict of pages.
        """
        self.pages[id] = HelpPage(self, id, header, body)
        self.ranks.append(id)


    # ------------------------------------------------------------------------


    def _install_sections_of_chapter(self, chapterid, body=[], whereiam=""):
        """
        Install all sections of a chapter: one section=one page.
        """
        toc = ""
        sectionid = ""
        sectionheader = ""
        sectionbody = []
        for i,line in enumerate(body):
            # new section
            if line.startswith('###') is True and line.startswith('####') is False:
                # add the previous section as a page
                if len(sectionid) > 0 and len(sectionheader) > 0 and len(sectionbody) > 0:
                    b = "Color(**"+whereiam+" >> "+sectionheader+"**)\n"+format_body(sectionbody)
                    self._install_page(sectionid, sectionheader, b)
                    toc += "        - Help(%s)\n" % sectionid
                    sectionbody = []
                # fix id and header
                sectionid = chapterid+'_'+str(i)
                sectionheader = format_header( line )
            else:
                # body
                sectionbody.append(line)
        # last section
        if len(sectionid) > 0 and len(sectionheader) > 0 and len(sectionbody) > 0:
            b = "Color(**"+whereiam+" >> "+sectionheader+"**)\n"+format_body(sectionbody)
            self._install_page(sectionid, sectionheader, b)
            toc += "        - Help(%s)\n" % sectionid

        return toc


    def _install_chapter(self, url_idx, c):
        """
        Load a chapter of the documentation, from an index file.
        """
        toc = ""
        base_path = os.path.dirname(url_idx)
        try:
            with codecs.open(url_idx, 'r', 'utf-8') as fd:

                # Read the index (the list of files of this chapter, one file=one section)
                lines = fd.readlines()
                if len(lines)==0: raise Exception('No content at url: %s'%url_idx)

                urls = list()
                for line in lines:
                    line = line.strip()
                    line = os.path.join(base_path,line)
                    urls.append( line )

                # The first page is always the title of the chapter
                title = format_title( load_page(urls[0]) )
                toc += "%d. Color(**%s**)\n" %(c,title)

                # The sections/pages of this chapter
                for i in range(1,len(urls)):
                    chaptercontent = load_page(urls[i])
                    # The first line is the title of the section
                    header = format_header(chaptercontent[0])
                    # The rest of the file is the body
                    whereiam = title + " >> "+ header
                    subtoc = self._install_sections_of_chapter(urls[i], chaptercontent[1:], whereiam)
                    if len(subtoc) == 0:
                        toc += "    - Help(%s)\n" % urls[i]
                        self._install_page(urls[i], header, format_body(chaptercontent[1:]))
                    else:
                        toc += "    - **%s**\n" % header
                        toc += subtoc

        except Exception:
            toc = ""

        return toc

    # -----------------------------------------------------------------------


    def Install(self, doc_idx, id, header="Help"):
        """
        Load the documentation, from an index file: load all found pages.

        @param doc_idx (string) Documentation index file name
        @param id (string)
        @param header (string) Header of the TOC

        """
        toc_body = ""
        base_path = os.path.dirname(doc_idx)
        try:
            with codecs.open(doc_idx, 'r', 'utf-8') as fd:

                # Read the index (the list of chapters of this documentation, one file=one chapter)
                lines = fd.readlines()
                if len(lines)==0: raise Exception('No content at url: %s'%doc_idx)

                urls = list()
                for line in lines:
                    line = line.strip()
                    line = os.path.join(base_path,line,line+".idx")
                    urls.append( line )

                for c,chapter_idx in enumerate(urls):
                    toc_body += self._install_chapter(chapter_idx,c)

        except Exception:
            toc_body = ""

        # Then, append this TOC to main one
        self.GetPage(str(HOME_ID)).body += toc_body

    # End Install
    # -----------------------------------------------------------------------


    def GetSearchSesultsPage(self, search):
        """
        Return a page, the content is the result of a search request.

        @param search (string) Pattern to search in all installed pages.
        @return string (Html)

        """
        matches = self._get_pages_matching_search(search)
        # search
        tex = ""
        tex += "<ul>"
        for page in matches:
            tex += "<li>"
            tex += "<a href=\"%s%s\">%s</a>" % (self.page_prefix, page.id, page.header)
            tex += "</li>"
        tex += "</ul>"
        search_page_html = "<h1>%s</h1>\n%s" % (
            "Search results for '%s'" % search,
            tex)
        return search_page_html

    # End GetSearchSesultsPage
    # -----------------------------------------------------------------------


    def GetPage(self, id):
        """
        Return the page with the given id, or None.

        @return HelpPage

        """
        return self.pages.get(id, None)

    # GetPage
    # -----------------------------------------------------------------------


    def GetNextPageId(self, id):
        """
        Return the page following the page with the given id, or None.

        @return HelpPage

        """
        if id == str(HOME_ID):
            return None

        if not id in self.ranks:
            return None

        idx = self.ranks.index(id)
        if ( idx+1 < len(self.ranks) ): # not the last index!
            return self.ranks[idx+1]

        return None

    # GetNextPage
    # -----------------------------------------------------------------------


    def GetPreviousPageId(self, id):
        """
        Return the page preceding the page with the given id, or None.

        @return HelpPage

        """
        if id == str(HOME_ID):
            return None

        if not id in self.ranks:
            return None

        idx = self.ranks.index(id)
        if ( idx > 0 ): # not the first index!
            return self.ranks[idx-1]

        return None

    # GetNextPage
    # -----------------------------------------------------------------------

# End HelpSystem
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Help Browser Frame
# ---------------------------------------------------------------------------


class HelpBrowser( wx.Frame ):
    """
    @author:  Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL
    @summary: A wiki-like help browser.

    """

    def __init__(self, parent):
        """
        Create a wiki-like help browser.
        """
        wx.Frame.__init__(self, parent, title=FRAME_TITLE+" - Help browser", size=(600, 550), style=FRAME_STYLE)

        self.history = []
        self.current_pos = -1
        self._create_help_system()

        self._create_gui()
        self._update_buttons()


    # End __init__
    # ------------------------------------------------------------------------


    # ------------------------------------------------------------------------
    # Help system, help pages
    # ------------------------------------------------------------------------

    def _create_help_system(self):
        self.help_system = HelpSystem(HELP_PATH, "page:")
        self.help_system.Install(DOC_IDX, "documentation", "Documentation")


    def _show_page(self, id, type="page", change_history=True):
        """
        Where which is a tuple (type, id):

          * (page, page_id)
          * (search, search_string)
        """
        if change_history:
            same_page_as_last = False
            if self.current_pos != -1:
                current_type, current_id = self.history[self.current_pos]
                if id == current_id:
                    same_page_as_last = True
            if same_page_as_last == False:
                self.history = self.history[:self.current_pos + 1]
                self.history.append((type, id))
                self.current_pos += 1
        self._update_buttons()
        if type == "page":
            self.html_window.SetPage(self._generate_page(id))
        elif type == "search":
            self.html_window.SetPage(self.help_system.GetSearchSesultsPage(id))
        self.Show()
        self.Raise()


    # ------------------------------------------------------------------------
    # Create the GUI
    # ------------------------------------------------------------------------


    def _create_gui(self):
        self._init_infos()
        self._create_toolbar()
        self._create_html()
        self._go_home()


    def _init_infos( self ):
        wx.GetApp().SetAppName( "helpbrowser" )
        # icon
        _icon = wx.EmptyIcon()
        _icon.CopyFromBitmap( spBitmap(APP_ICON) )
        self.SetIcon(_icon)


    def _create_toolbar(self):
        self.toolbar = self.CreateToolBar(style=wx.TB_TEXT|wx.TB_FLAT|wx.TB_DOCKABLE|wx.TB_NODIVIDER)

        size = (BUTTON_ICONSIZE, BUTTON_ICONSIZE)

        close_bmp   = spBitmap(LOGOUT_ICON,   BUTTON_ICONSIZE)
        home_bmp    = spBitmap(HOME_ICON,     BUTTON_ICONSIZE)
        back_bmp    = spBitmap(BACKWARD_ICON, BUTTON_ICONSIZE)
        forward_bmp = spBitmap(FORWARD_ICON,  BUTTON_ICONSIZE)
        previous_bmp= spBitmap(PREVIOUS_ICON, BUTTON_ICONSIZE)
        next_bmp    = spBitmap(NEXT_ICON,     BUTTON_ICONSIZE)
        self.toolbar.SetToolBitmapSize(size)

        # Close
        self.toolbar.AddLabelTool(wx.ID_CLOSE, "Close", close_bmp, shortHelp="Close this browser")

        # Separator
        self.toolbar.AddSeparator()

        # Home
        home_str = "Go to the Table of contents"
        self.toolbar.AddLabelTool(HOME_ID, "Home", home_bmp, shortHelp=home_str)

        # Backward
        backward_str = "Go back one page"
        self.toolbar.AddLabelTool(BACKWARD_ID, "Backward", back_bmp, shortHelp=backward_str)

        # Forward
        forward_str = "Go forward one page"
        self.toolbar.AddLabelTool(FORWARD_ID, "Forward", forward_bmp, shortHelp=forward_str)

        # Separator
        self.toolbar.AddSeparator()

        # Previous
        previous_str = "Go to the preceding page"
        self.toolbar.AddLabelTool(PREVIOUS_ID, "Prev", previous_bmp, shortHelp=previous_str)

        # Next
        next_str = "Go to the next page"
        self.toolbar.AddLabelTool(NEXT_ID, "Next", next_bmp, shortHelp=next_str)

        # Separator
        self.toolbar.AddSeparator()

        # Search
        self.search = wx.SearchCtrl(self.toolbar, size=(200, -1), style=wx.TE_PROCESS_ENTER)
        self.toolbar.AddControl(self.search)

        self.toolbar.SetToolSeparation(10)

        self.toolbar.Realize()

        self.Bind(wx.EVT_TOOL, self.OnClose, id=wx.ID_CLOSE)
        self.Bind(wx.EVT_TOOL, self.OnToolbarClicked, id=PREVIOUS_ID)
        self.Bind(wx.EVT_TOOL, self.OnToolbarClicked, id=NEXT_ID)
        self.Bind(wx.EVT_TOOL, self.OnToolbarClicked, id=FORWARD_ID)
        self.Bind(wx.EVT_TOOL, self.OnToolbarClicked, id=BACKWARD_ID)
        self.Bind(wx.EVT_TOOL, self.OnToolbarClicked, id=HOME_ID)

        self.Bind(wx.EVT_TEXT_ENTER, self.OnSearchText, self.search)


    def _create_html(self):
        # Html window
        self.html_window = wx.html.HtmlWindow(self)
        self.html_window.Connect(wx.ID_ANY, wx.ID_ANY, wx.EVT_KEY_DOWN.typeId, self.OnKeyDown)

        self.Bind(wx.html.EVT_HTML_LINK_CLICKED, self.OnLinkClicked, self.html_window)



    # -----------------------------------------------------------------------
    # Callbacks to events
    # -----------------------------------------------------------------------

    def OnClose(self, event):
        """
        Event handler used to hide the frame.
        """
        self.Show(False)

    # End OnClose
    # -----------------------------------------------------------------------


    def OnKeyDown(self, evt):
        """
        Event handler used when a keyboard key has been pressed.

        The following keys are handled:
        Key         Action
        --------    ------------------------------------
        Backspace   Go to previous page
        """
        keycode = evt.GetKeyCode()
        if keycode == wx.WXK_BACK:
            self._go_back()
        evt.Skip()

    # End OnKeyDown
    # -----------------------------------------------------------------------


    def OnToolbarClicked(self, e):
        """
        Event handler used when a button of the toolbar has been pressed.
        """
        bid = e.GetId()
        if bid == HOME_ID:
            self._go_home()
        elif bid == BACKWARD_ID:
            self._go_back()
        elif bid == FORWARD_ID:
            self._go_forward()
        elif bid == PREVIOUS_ID:
            self._go_previous()
        elif bid == NEXT_ID:
            self._go_next()

    # End OnToolbarClicked
    # -----------------------------------------------------------------------


    def OnSearchText(self, e):
        """
        Event handler used when a text has been entered in the search bar.
        """
        self._search(self.search.GetValue())

    # End OnSearchText
    # -----------------------------------------------------------------------


    def OnLinkClicked(self, e):
        url = e.GetLinkInfo().GetHref()
        if url.startswith("page:"):
            self._show_page(url[5:])
        else:
            webbrowser.open(url)

    # End OnLinkClicked
    # -----------------------------------------------------------------------


    # -----------------------------------------------------------------------
    # Private
    # -----------------------------------------------------------------------


    def _go_home(self):
        self._show_page(str(HOME_ID))


    def _go_back(self):
        if self.current_pos > 0:
            self.current_pos -= 1
            current_type, current_id = self.history[self.current_pos]
            self._show_page(current_id, type=current_type, change_history=False)


    def _go_forward(self):
        if self.current_pos < len(self.history) - 1:
            self.current_pos += 1
            current_type, current_id = self.history[self.current_pos]
            self._show_page(current_id, type=current_type, change_history=False)


    def _go_previous(self):
        if self.current_pos != -1:
            current_type, current_id = self.history[self.current_pos]
            prev_id = self.help_system.GetPreviousPageId(current_id)
            if prev_id:
                self._show_page(prev_id)


    def _go_next(self):
        if self.current_pos != -1:
            current_type, current_id = self.history[self.current_pos]
            next_id = self.help_system.GetNextPageId(current_id)
            if next_id:
                self._show_page(next_id)


    def _search(self, string):
        string = string.strip()
        if len(string) > 0:
            self._show_page(string, type="search")


    def _update_buttons(self):
        current_id = -1
        if self.current_pos != -1:
            current_type, current_id = self.history[self.current_pos]

        history_len = len(self.history)
        enable_backward = history_len > 1 and self.current_pos > 0
        enable_forward = history_len > 1 and self.current_pos < history_len - 1
        enable_next = str(current_id) != str(HOME_ID)
        enable_prev = str(current_id) != str(HOME_ID)
        self.toolbar.EnableTool(BACKWARD_ID, enable_backward)
        self.toolbar.EnableTool(FORWARD_ID, enable_forward)
        self.toolbar.EnableTool(PREVIOUS_ID, enable_prev)
        self.toolbar.EnableTool(NEXT_ID, enable_next)


    def _generate_page(self, id):
        page = self.help_system.GetPage(id)
        if page == None:
            error_page_html = "<h1>%s</h1><p>%s</p>" % (
                "Page not found",
                "Could not find page with id=%s" % id)
            return self._wrap_in_html(error_page_html)
        else:
            return self._wrap_in_html(page.GetHtml())


    def _wrap_in_html(self, content):
        HTML_SKELETON = """
        <html>
        <head>
        </head>
        <body>
        %s
        </body>
        </html>
        """
        return HTML_SKELETON % content

# ---------------------------------------------------------------------------
