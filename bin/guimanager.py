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

import os
import sys
import platform
import logging
import traceback
from logging import info as loginfo

# ---------------------------------------------------------------------------


# VERIFY PYTHON
# -------------
if sys.version_info < (2, 7):
    import tkMessageBox
    tkMessageBox.showwarning(
        "Python Error...",
        "Your python version is too old. This program requires 2.7\n. Verify your python installation and try again."
        )
    sys.exit(1)

if sys.version_info > (3, 0):
    import tkMessageBox
    tkMessageBox.showwarning(
        "Python Error...",
        "Your python version is not appropriate. This program requires 2.7\n. Verify your python installation and try again."
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


# THEN, VERIFY Manager
# ------------------

# Make sure that we can import libraries
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

try:
    from Manager.manager import MainFrame
except ImportError,e:
    import tkMessageBox
    tkMessageBox.showwarning(
        "Installation Error...",
        "A problem occurred when launching this program:\n'"+str(e)
        )
    sys.exit(1)


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


def show_error():
    message = ''.join(traceback.format_exception(*sys.exc_info()))
    dialog = wx.MessageDialog(None, message, 'Error!', wx.OK|wx.ICON_ERROR)
    dialog.ShowModal()


# ---------------------------------------------------------------------------
# Main application
# ---------------------------------------------------------------------------

if __name__ == '__main__':

    # Log
    log_level = 1
    log_file  = None
    setup_logging(log_level, log_file)

    # Create the wxapp
    mainmanager = wx.App(redirect=True)

    # Create the main frame
    try:
        frame = MainFrame()
        mainmanager.SetTopWindow(frame)
        frame.Show()
        #frame.cause_error()
        mainmanager.MainLoop()
    except:
        show_error()

# ---------------------------------------------------------------------------
