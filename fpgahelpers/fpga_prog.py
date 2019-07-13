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

import os, sys, tempfile
import database, common

options = common.get_options(__file__)

###################################################################################################
# Processing the options
###################################################################################################

if not os.path.exists(options.bit) and options.device not in ['detect','unlock'] and options.tool not in ['libero']:
   sys.exit('fpga_prog (ERROR): bitstream needed but not found.')

if options.board and options.board not in database.boards:
   sys.exit("fpga_prog (ERROR): unsupported board")

if options.board is not None and options.device not in ['detect','unlock']:
   if options.device + '_name' not in database.boards[options.board]:
      sys.exit('fpga_prog (ERROR): the device <' + options.device + '> is not ' +
                          'supported in the board <' + options.board + '>.')
   else:
      options.position = database.boards[options.board]['fpga_pos']
      if options.device != 'fpga':
         options.memname = database.boards[options.board][options.device + '_name']
         options.width   = database.boards[options.board][options.device + '_width']

###################################################################################################
# Preparing files
###################################################################################################

# Preparing a temporary Makefile
tempmake = tempfile.NamedTemporaryFile(mode='w')
tempmake.write("#!/usr/bin/make\n")
tempmake.write("TOOL=%s\n" % options.tool)
tempmake.write("DEV=%s\n" % options.device)
tempmake.write("TCLPATH=%s\n" % (common.get_script_path(__file__) + "/tcl"))
tempmake.write("include $(TCLPATH)/Makefile")
tempmake.flush()

tempopt = None;
# Preparing a temporary options.tcl (if not exists)
if not os.path.exists('options.tcl'):
   tempopt = open('options.tcl','w')
   if 'memname' in options:
      tempopt.write("set fpga_name %s\n" % options.memname)
      tempopt.write("set spi_name  %s\n" % options.memname)
      tempopt.write("set bpi_name  %s\n" % options.memname)
      tempopt.write("set xcf_name  %s\n" % options.memname)
   if 'position' in options:
      tempopt.write("set fpga_pos  %s\n" % options.position)
      tempopt.write("set xcf_pos   %s\n" % options.position)
   if 'width' in options:
      tempopt.write("set spi_width %s\n" % options.width)
      tempopt.write("set bpi_width %s\n" % options.width)
      tempopt.write("set xcf_width %s\n" % options.width)
   tempopt.flush()

###################################################################################################
# Running
###################################################################################################

# Executing the Makefile
try:
   os.system("make -f %s prog" % tempmake.name)
except:
   print("fpga_prog (ERROR): failed when programming")

###################################################################################################
# Ending
###################################################################################################

# The temporary files are destroyed
tempmake.close()
if tempopt is not None:
   tempopt.close()
   os.remove('options.tcl')
