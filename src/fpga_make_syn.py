#!/usr/bin/python
#
# FPGA Synt, generates files to make a Synthesis
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

import argparse, yaml, os, sys, shutil, glob

bin_dir = os.path.dirname(os.path.abspath(__file__))
if os.path.exists(bin_dir + '/../data'):
   share_dir = bin_dir + '/..'
   lib_dir   = bin_dir
else:
   share_dir = bin_dir + '/../share/fpga-helpers'
   lib_dir   = share_dir

sys.path.insert(0, lib_dir)
from fpga_lib import *

## Parsing the command line ###################################################

version = 'FPGA Make Syn (FPGA Helpers) v' + getVersion(share_dir)

boards = []
getBoards(boards, share_dir)

parser = argparse.ArgumentParser(
   description='Generates files to make a Synthesis.',
   epilog='Supported boards: ' + ', '.join(boards)
)

parser.add_argument(
   '-v', '--version',
   action='version',
   version=version
)

parser.add_argument(
   'tool',
   metavar='TOOL',
   choices=['ise','vivado','quartus2','all'],
   help='NAME of the vendor tool to be used [ise|vivado|quartus2|all]'
)

parser.add_argument(
   '-b', '--board',
   metavar='NAME|FILE',
   help='NAME of a supported board or FILE (.yaml) of a new/custom board '
)

options = parser.parse_args()

## Processing the options #####################################################

print (__file__ + '(INFO): ' + version)

fpga_prog_text = "# No <board> specified.\n";
if options.board is not None:
   if options.tool == 'all':
      sys.exit(
         __file__ +
         '(ERROR): value <all> for option <tool> is not allowed when <board> is specified.'
      )
   if options.board.endswith(".yaml"):
      path = options.board
   else:
      path = share_dir + '/data/boards/' + options.board + '.yaml'
   if os.path.exists(path):
      board = yaml.load(file(path, 'r'))
   else:
      sys.exit(__file__ + '(ERROR): <board> ' + options.board + ' not exists.')
   if not options.tool in board['tool']['synt']:
      sys.exit(
         __file__ + '(ERROR): <board> ' + options.board +
         ' is not supported by the <tool> ' + options.tool + '.'
      )
   # fpga_prog alternatives
   fpga_prog_text = "";
   for device in sorted(board):
       if device == 'fpga':
          fpga_prog_text += 'prog-fpga: $(BITFILE)\n\tfpga_prog --board=' + \
                            options.board + ' --device=fpga $<\n'
       if device == 'spi':
          fpga_prog_text += 'prog-spi: $(BITFILE)\n\tfpga_prog --board=' + \
                            options.board + ' --device=spi $<\n'
       if device == 'bpi':
          fpga_prog_text += 'prog-bpi: $(BITFILE)\n\tfpga_prog --board=' + \
                            options.board + ' --device=bpi $<\n'

## Generating files ###########################################################

if options.tool != 'all':
   shutil.copy(share_dir + '/data/tools/synthesis/options.tcl', '.')
   shutil.copy(share_dir + '/data/tools/synthesis/' + options.tool + '.tcl', '.')
else:
   for filename in glob.glob(share_dir + '/data/tools/synthesis/*.tcl'):
       shutil.copy(filename, '.')
       file(os.path.basename(filename),'a').write("\n# Created with " + version)
shutil.copy(share_dir + '/data/tools/synthesis/Makefile', '.')
file('Makefile','a').write(fpga_prog_text)
file('Makefile','a').write("\n# Created with " + version)

print (__file__ + '(INFO): files were created.')
