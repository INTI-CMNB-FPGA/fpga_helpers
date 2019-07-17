#!/usr/bin/python
#
# FPGA Prog, transfers a BitStream to a device
# Copyright (C) 2015-2019 INTI
# Copyright (C) 2015-2019 Rodrigo A. Melo
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

import os
import sys

import database as db
import common

def main():
    options = common.get_options(__file__)

    # Processing the options
    if not os.path.exists(options.bit) and options.device not in ['detect','unlock'] and options.tool not in ['libero']:
       sys.exit('fpga_prog (ERROR): bitstream needed but not found.')
    if options.board and options.board not in db._boards:
       sys.exit("fpga_prog (ERROR): unsupported board")
    if options.board is not None and options.device not in ['detect','unlock']:
       if options.device + '_name' not in db._boards[options.board]:
          sys.exit(
              "fpga_prog (ERROR): the device <%s> is not supported in the board <%s>." %
              (options.device, options.board)
          )
       else:
          options.position = db._boards[options.board]['fpga_pos']
          if options.device != 'fpga':
             options.memname = db._boards[options.board][options.device + '_name']
             options.width   = db._boards[options.board][options.device + '_width']

    if not options.debug:
       # Preparing files
       temp = None;
       if not os.path.exists('options.tcl'):
          temp = open('options.tcl','w')
          if 'memname' in options:
             for dev in ['fpga', 'spi', 'bpi', 'xcf']:
                 temp.write("set %s_name %s\n" % (dev, options.memname))
          if 'position' in options:
             for dev in ['fpga', 'xcf']:
                 temp.write("set %s_pos %s\n" % (dev, options.position))
          if 'width' in options:
             for dev in ['spi', 'bpi', 'xcf']:
                 temp.write("set %s_width %s\n" % (dev, options.width))
          temp.flush()
       # Executing
       text = common.get_makefile_content(
          tool=options.tool, task=None, dev=options.device,
          path=(common.get_script_path(__file__) + "/tcl")
       )
       common.execute_make(__file__, text)
       if temp is not None:
          temp.close()
          os.remove('options.tcl')
    else:
       print(options)

if __name__ == "__main__":
   main()
