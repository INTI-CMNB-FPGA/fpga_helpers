#!/usr/bin/python
#
# FPGA Synt, do synthesis based on the project file of the vendor's tool
# Copyright (C) 2017-2019 INTI
# Copyright (C) 2017-2019 Rodrigo A. Melo
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

import glob, sys, os
import database as db
import common

def main():
    options = common.get_options(__file__)

    # Collecting information
    for tool in db._tools:
        if options.file is None:
            try:
                options.file = glob.glob("*.%s" % db._tools[tool]['prj'])[0]
            except:
                options.file = None

    if options.file is None:
       sys.exit("fpga_synt (ERROR): project file not found")
    if not os.path.exists(options.file):
       sys.exit("fpga_synt (ERROR): file %s do not exists" % options.file)

    options.tool = None
    for tool in db._tools:
        if options.file.endswith(".%s" % db._tools[tool]['prj']):
           options.tool = tool
    if options.tool is None:
       sys.exit("fpga_synt (ERROR): unsupported vendor's tool")

    # Executing
    text = common.get_makefile_content(
       tool=options.tool, task=options.task, dev=None,
       path=(common.get_script_path(__file__) + "/tcl")
    )
    common.execute_make(__file__, text)

if __name__ == "__main__":
   main()
