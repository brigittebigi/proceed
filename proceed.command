#! /bin/bash
# ######################################################################### #
#                                                                           #
# File:    manager                                                          #
# Author:  Brigitte Bigi                                                    #
# Date:    2013-07-08                                                       #
#                                                                           #
# Licence: GPL                                                              #
#   This file is part of Manager.                                           #
#                                                                           #
#   Manager is free software: you can redistribute it and/or modify         #
#   it under the terms of the GNU General Public License as published by    #
#   the Free Software Foundation, either version 3 of the License, or       #
#   any later version.                                                      #
#                                                                           #
#   Manager is distributed in the hope that it will be useful,              #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of          #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
#   GNU General Public License for more details.                            #
#                                                                           #
#   You should have received a copy of the GNU General Public License       #
#   along with Manager.  If not, see <http://www.gnu.org/licenses/>.        #
#                                                                           #
# ######################################################################### #

# Get the current directory (Manager dir name)
curdir=`dirname $0`

# Fix the locale with a generic value!
LANG='C'


# ######################################################################### #

# Manager is here:
unamestr=`uname`
if [[ "$unamestr" == 'Linux' ]]; then
   python $curdir/bin/guimanager.py
else
   arch -i386 python $curdir/bin/guimanager.py
fi

# ######################################################################### #

