#
# FPGA Lib, functions used by FPGA Helpers suite members
# Copyright (C) 2015-2016 INTI, Rodrigo A. Melo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os, yaml

def getVersion(install_dir):
    return file(install_dir + '/VERSION', 'r').read().strip()

def getBoards(boards, install_dir):
    path = install_dir + '/data/boards'
    if os.path.isdir(path):
       for file in sorted(os.listdir(path)):
           if file.endswith(".yaml"):
              boards.append(os.path.splitext(file)[0])
    else:
       boards.append('there are no files installed in the system.')
