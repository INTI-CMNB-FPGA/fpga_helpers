#!/usr/bin/python
#
# FPGA Prog, transfers a BitStream to a device
# Copyright (C) 2015-2017 INTI
# Copyright (C) 2015-2017 Rodrigo A. Melo
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

import argparse, os, sys, tempfile
from fpga_helpers import *

###################################################################################################
# Parsing the command line
###################################################################################################

version = "fpga_prog is a member of FPGA Helpers v%s" % (fpga_helpers.version)

parser = argparse.ArgumentParser(
   prog        = 'fpga_prog',
   description = 'Transfers a BitStream to a device.',
   epilog      = "Supported boards: " + ', '.join(fpga_helpers.boards)
)

parser.add_argument(
   '-v', '--version',
   action      = 'version',
   version     = version
)

parser.add_argument(
   'bit',
   default     = "",
   nargs       = '?',
   metavar     = 'BITSTREAM',
   help        = 'bitstream to be transferred'
)

parser.add_argument(
   '-t', '--tool',
   metavar     = 'TOOL',
   choices     = ['ise','quartus','libero','vivado'],
   help        = 'name of the vendor tool to be used (ise|quartus|libero|vivado) [vivado]'
)

parser.add_argument(
   '-d', '--device',
   metavar     = 'DEVICE',
   default     = 'fpga',
   choices     = ['fpga', 'spi', 'bpi', 'xcf', 'detect', 'unlock'],
   help        = 'type of the target device (fpga|spi|bpi|xcf|detect|unlock) [fpga]'
)

parser.add_argument(
   '-b', '--board',
   metavar     = 'BOARDNAME',
   help        = 'name of a supported board (note: if you use the board option, -p, ' +
                 '-m and -w will be overwritten) [None]'
)

parser.add_argument(
   '-m', '--memname',
   metavar     = 'MEMNAME',
   default     = 'UNDEFINED',
   help        = 'name of the memory target device [UNDEFINED]'
)

parser.add_argument(
   '-p', '--position',
   metavar     = 'POSITION',
   type        = int,
   default     = 1,
   help        = 'positive number which represents the POSITION of the device in the ' +
                 'JTAG chain [1]'
)

parser.add_argument(
   '-w', '--width',
   metavar     = 'WIDTH',
   type        = int,
   default     = 1,
   choices     = [1, 2, 3, 4, 8, 16, 32],
   help        = 'positive number which representes the WIDTH of bits of the target ' +
                 'memory (1, 2, 3, 4, 8, 16, 32, 64) [1]'
)

options = parser.parse_args()

###################################################################################################
# Processing the options
###################################################################################################

if not os.path.exists(options.bit) and options.device not in ['detect','unlock'] and options.tool not in ['libero']:
   sys.exit('fpga_prog (ERROR): bitstream needed but not found.')

if options.board and options.board not in fpga_helpers.boards:
   sys.exit("fpga_prog (ERROR): unsupported board")

if options.board is not None and options.device not in ['detect','unlock']:
   if options.device + '_name' not in fpga_helpers.boards[options.board]:
      sys.exit('fpga_prog (ERROR): the device <' + options.device + '> is not ' +
                          'supported in the board <' + options.board + '>.')
   else:
      options.position = fpga_helpers.boards[options.board]['fpga_pos']
      if options.device != 'fpga':
         options.memname = fpga_helpers.boards[options.board][options.device + '_name']
         options.width   = fpga_helpers.boards[options.board][options.device + '_width']

if options.tool is None:
   print("fpga_prog (INFO): you did not specified a tool to use. Choose one:")
   print("1. ISE (Xilinx)")
   print("2. Quartus (INTEL/Altera)")
   print("3. Libero (Microsemi)")
   print("4. Vivado (Xilinx) [default]")
   option = sys.stdin.read(1)
   if option == '1':
      options.tool = "ise"
   elif option == '2':
      options.tool = "quartus"
   elif option == '3':
      options.tool = "libero"
   elif option == '4':
      options.tool = "vivado"
   else:
      sys.exit('fpga_prog (ERROR): invalid option.')

###################################################################################################
# Running
###################################################################################################

# Preparing a temporary Makefile
tempmake = tempfile.NamedTemporaryFile()
tempmake.write("#!/usr/bin/make\n")
tempmake.write("TOOL=%s\n" % options.tool)
tempmake.write("DEV=%s\n" % options.device)
tempmake.write("TCLPATH=%s\n" % (os.path.dirname(os.path.abspath(__file__)) + "/../tcl"))
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

# Executing the Makefile
try:
   os.system("make -f %s prog" % temp.name)
except:
   print("fpga_prog (ERROR): failed when programming")

# The temporary files are destroyed
tempmake.close()
if tempopt is not None:
   tempopt.close()
   os.remove('options.tcl')
