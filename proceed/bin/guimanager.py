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

__docformat__ = """epytext"""
__authors___  = """Brigitte Bigi (brigitte.bigi@gmail.com)"""
__copyright__ = """Copyright (C) 2013-2015  Brigitte Bigi"""

"""
Graphical User Interface to manage documents of a conference.
"""

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

import sys
import os.path
from argparse import ArgumentParser
import traceback
import tkMessageBox
import logging

# ---------------------------------------------------------------------------


# VERIFY PYTHON
# -------------
if sys.version_info < (2, 7):
    tkMessageBox.showwarning(
        "Python Error...",
        "Your python version is too old. Proceed requires 2.7\n. Verify your python installation and try again."
        )
    sys.exit(1)

if sys.version_info >= (3, 0):
    tkMessageBox.showwarning(
        "Python Error...",
        "Your python version is not appropriate. Proceed requires 2.7\n. Verify your python installation and try again."
        )
    sys.exit(1)


# VERIFY WXPYTHON
# ----------------

try:
    import wx
except ImportError,e:
    import tkMessageBox
    tkMessageBox.showwarning(
        "WxPython Error...",
        "WxPython is not installed on your system.\n. Verify your installation and try again."
        )
    sys.exit(1)

try:
    wxv = wx.version().split()[0]
except Exception:
    wxv = '2'

if int(wxv[0]) < 3:
    tkMessageBox.showwarning(
        "WxPython Warning...",
        'Your version of wxpython is too old. You could encounter problem while using Proceed.\n'
        'Please, perform the update at http://wxpython.org/download.php and restart Proceed.\n\n'
        'For any help, see Proceed installation page.')


# THEN, VERIFY Manager
# ------------------

# Make sure that we can import libraries
PROGRAM = os.path.abspath(__file__)
PROCEED = os.path.join(os.path.dirname( os.path.dirname( PROGRAM ) ), "src")
sys.path.insert(0,PROCEED)

try:
    from wxgui.manager import MainFrame
    from utils.commons import setup_logging, test_pdflatex, test_xelatex, test_pdftk
except ImportError as e:
    import tkMessageBox
    tkMessageBox.showwarning(
        "Installation Error...",
        "A problem occurred when launching this program:\n'"+str(e)
        )
    print traceback.format_exc()
    sys.exit(1)

# ---------------------------------------------------------------------------
# Install Gettext
# ---------------------------------------------------------------------------

def install_gettext_in_builtin_namespace():
    def _(message):
        return message
    import __builtin__
    if not "_" in __builtin__.__dict__:
        __builtin__.__dict__["_"] = _

# ---------------------------------------------------------------------------
# Main application
# ---------------------------------------------------------------------------

# Log
log_level = 0
log_file  = None
setup_logging(log_level, log_file)

# Gettext
install_gettext_in_builtin_namespace()


# Arguments
# ------------------------------------------------------------------------

parser = ArgumentParser(usage="%s directory" % os.path.basename(PROGRAM), description="Proceed Graphical User Interface.")
parser.add_argument("files", nargs="*", help='Input directory with conference file(s)')
args = parser.parse_args()

# ----------------------------------------------------------------------------
# Proceed GUI is here:
# ----------------------------------------------------------------------------

# Create the wxapp
mainmanager = wx.App(redirect=True)

# Create the main frame
try:
    logging.debug('Welcome to Proceed')
    frame = MainFrame()
    mainmanager.SetTopWindow(frame)

    if test_pdflatex( ) is False:
        dial = wx.MessageDialog(None, 'pdflatex is not installed on your system.\nThe automatic generation WILL NOT WORK.', 'Exclamation',
        wx.OK | wx.ICON_EXCLAMATION)
        dial.ShowModal()

    if test_xelatex( ) is False:
        dial = wx.MessageDialog(None, 'xetex is not installed on your system.\nThe automatic generation WILL NOT WORK.', 'Exclamation',
            wx.OK | wx.ICON_EXCLAMATION)
        dial.ShowModal()

    if test_pdftk( ) is False:
        dial = wx.MessageDialog(None, 'pdftk is not installed on your system.\nThe automatic generation WILL NOT WORK.', 'Exclamation',
            wx.OK | wx.ICON_EXCLAMATION)
        dial.ShowModal()

    frame.Show()
except:
    tkMessageBox.showwarning(
    "Proceed Error...",
    "A problem occurred when creating the Proceed graphical user interface.\nThe error is: %s"%(str(e))
    )
    print traceback.format_exc()

mainmanager.MainLoop()

# ---------------------------------------------------------------------------
