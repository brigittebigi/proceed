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
# ---------------------------------------------------------------------------
# File: commons.py
# ----------------------------------------------------------------------------

import sys
import logging
from logging import info as loginfo

# ----------------------------------------------------------------------------

def usage(output, progname, required, optional, status=0):
    """
    Write the usage on an output .

    @param output (string) represents the output (for example: sys.stdout)
    @param progname (string) is the name of the program
    @param required (dict) is a dictionary of required arguments
    @param optional (dict) is a dictionary of optional arguments
    @param status (int) is the exit status value

    """
    maxlen = max([len(x) for x in required]) + 4
    size = '{0:<%d}'%maxlen

    output.write(progname + ' [options] where:\n required options are:\n')
    for key,value in required.iteritems():
        skey = size.format(key)
        output.write('\t%s%s\n'%(skey,value))

    output.write(' facultative options are:\n')
    for key,value in optional.iteritems():
        skey = size.format(key)
        output.write('\t%s%s\n'%(skey,value))

    sys.exit(status)

# End usage
# ----------------------------------------------------------------------------


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

# ----------------------------------------------------------------------------
