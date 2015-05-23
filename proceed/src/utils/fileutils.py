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
# File: fileutils.py
# ----------------------------------------------------------------------------

__docformat__ = """epytext"""
__authors__   = """Brigitte Bigi (brigitte.bigi@gmail.com)"""
__copyright__ = """Copyright (C) 2011-2015  Brigitte Bigi"""


# ----------------------------------------------------------------------------

import os
import random
import codecs

# ----------------------------------------------------------------------------

def exists(filename):
    """
    os.path.exists() revisited!
        - case-insensitive
        - return the filename or None
    """
    for x in os.listdir( os.path.dirname(filename)):
        if os.path.basename(filename.lower()) == x.lower():
            return os.path.join(os.path.dirname(filename),x)
    return None

# ----------------------------------------------------------------------------

def get_files(directory,extension,recurs=True):
    """
    Get a file list of a directory.

    @param directory is the directory to find files
    @param extension is the file extension to filter the directory content

    @return a list of files

    """
    filelist = []
    if os.path.exists(directory):
        filelist = dirEntries(directory, recurs, extension)
        #filelist = [x for x in os.listdir(directory) if x.lower().endswith(extension.lower())]
    else:
        message = "ERROR: The directory "+directory+" does not exists."
        raise IOError(message)
    return filelist

# ----------------------------------------------------------------------------

def dirEntries(dir_name, subdir, extension):
    """
    Return a list of file names found in directory 'dir_name'.

    If 'subdir' is True, recursively access subdirectories under 'dir_name'.
    Additional argument, if any, is file extension to match filenames.

    """
    fileList = []
    for file in os.listdir(dir_name):
        dirfile = os.path.join(dir_name, file)
        if os.path.isfile(dirfile):
            if not extension:
                fileList.append(dirfile)
            else:
                if dirfile.lower().endswith(extension.lower()):
                    fileList.append(dirfile)
        # recursively access file names in subdirectories
        elif os.path.isdir(dirfile) and subdir:
            fileList.extend(dirEntries(dirfile, subdir, extension))
    return fileList

# ----------------------------------------------------------------------------

def set_tmpfilename():
    randval = random.random()    # random float
    #tmp = "tmp_"+str(datetime.datetime.now())
    tmp = "tmp_"+str(randval)
    return tmp

# ----------------------------------------------------------------------------


def writecsv(filename, rows, separator="\t", encoding="utf-8-sig"):
    """
    Write the rows to the file.
    Args:
        filename (string):
        rows (list):
        separator (string):
        encoding (string):
    """
    with codecs.open(filename, "w+", encoding) as f:
        for row in rows:
            tmp = []
            for s in row:
                if isinstance(s, (float, int)):
                    s = str(s)
                else:
                    s = '"%s"' % s
                tmp.append(s)
            f.write('%s\n' % separator.join(tmp))

# ----------------------------------------------------------------------------
