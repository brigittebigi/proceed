#!/usr/bin/env python
# -*- coding: utf8 -*-
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
#       Copyright (C) 2013-2018  Brigitte Bigi
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

from subprocess import Popen, PIPE, STDOUT
import re
from name import GenName
import os

# ---------------------------------------------------------------------------


def run_command(command):
    """
    Execute a command, wait, and print output in the log file.

    @param command is a string to represent the command to execute

    """
    p = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT)
    #retval = p.wait()
    line = p.communicate()
    return line[0]

# ------------------------------------------------------------------------


def countPages(filename):
    """
    Estimates the number of pages of a PDF document.

    @param filename (string) File to be counted.
    @return (int)

    This function requires pdftk to be installed:
    https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/

    """
    data = file(filename, "rb").read()

    rx_count_pages = re.compile(r"/Type\s*/Page([^s]|$)", re.MULTILINE|re.DOTALL)
    nb_pages = len(rx_count_pages.findall(data))
    if nb_pages == 0:
        output_name = GenName().get_name()
        command = 'pdftk '
        command += filename + ' dump_data output '
        command += output_name
        ret = run_command(command)
        if os.path.exists(output_name) is False:
            raise IOError('The file %s was not created by pdftk'.format(output_name))
        fp = open(output_name, 'r')
        for line in fp:
            if "NumberOfPages:" in line:
                nb_pages = int(line.split()[1])
        fp.close()
        os.remove(output_name)

    return nb_pages

# ------------------------------------------------------------------------


def formatPages(filename):
    """
    Convert the "numeric size" of a PDF document to a "paper format".

    @param filanem (string) File to be observed to get the size.

    """
    mediabox = {"0 0 595 842":"a4paper", "0 0 595.276 841.89":"a4paper", "0 0 612 792":"letterpaper", "0 0 498.898 708.661":"b5paper", "0 0 419.528 595.276":"a5paper"}

    fp = open(filename, 'r')
    fsize = None
    for line in fp:
        line = line.strip()
        if "/MediaBox [" in line or "/MediaBox[" in line:
            line = line[line.find("/MediaBox"):]
            line = line[:line.find("]")]
            fsize = line.split("[")[1]
            fsize = fsize.replace("]","")
            fsize = fsize.strip()
            break
    fp.close()

    if fsize is None:
        return IOError

    # Nice: the format is exactly good!
    if fsize in mediabox:
        return mediabox[fsize]

    # Use a ratio, and fix... the nearest format as possible...
    l = float(fsize.split()[2])
    L = float(fsize.split()[3])
    ratio = L/l
    if ratio < 1.31:
        return "letterpaper"

    return "a4paper"
