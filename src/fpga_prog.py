#!/usr/bin/python
#
# FPGA Prog, transfers a BitStream to a device
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

import argparse, yaml, os, sys

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

version = 'FPGA Prog (FPGA Helpers) v' + getVersion(share_dir)

boards = []
getBoards(boards, share_dir)

parser = argparse.ArgumentParser(
   description='Transfers a BitStream to a device.',
   epilog="Supported boards: " + ', '.join(boards)
)

parser.add_argument(
   '-v', '--version',
   action='version',
   version=version
)
parser.add_argument(
   'bit',
   metavar='BITSTREAM',
   help='BitStream to be transferred'
)
parser.add_argument(
   '-t', '--tool',
   metavar='TOOLNAME',
   default='ise',
   choices=['ise','quartus2'],
   help='Name of the vendor tool to be used [ise |quartus2]'
)

devices = parser.add_argument_group('device arguments')
devices.add_argument(
   '-d', '--device',
   metavar='DEVICE',
   default='fpga',
   choices=['fpga', 'spi', 'bpi', 'xcf', 'detect', 'unlock'],
   help='Type of the target device [fpga(default)|spi|bpi|xcf|detect|unlock]'
)
devices.add_argument(
   '-p', '--position',
   metavar='POSITION',
   type=int,
   default=1,
   help='positive number which represents the POSITION of the device in the ' +
        'JTAG chain [1]'
)
devices.add_argument(
   '-m', '--memname',
   metavar='MEMNAME',
   default='UNDEFINED',
   help='Name of the target memory (when applicable) [UNDEFINED]'
)
devices.add_argument(
   '-w', '--width',
   metavar='WIDTH',
   type=int,
   default=1,
   choices=[1, 4, 8, 16, 32],
   help='positive number which representes the WIDTH of bits of the target ' +
        'memory (when applicable) [1]'
)
devices.add_argument(
   '-b', '--board',
   metavar='BOARDNAME|BOARDFILE',
   help='Name of a supported board or file (.yaml) of a new/custom board ' +
        '(note: if you use the board option, -p, -m, -w and -t will be ' +
        'overwritten) []'
)

options = parser.parse_args()
options.output_dir = '/tmp/fpga_prog'

## Processing the options #####################################################

print (__file__ + '(INFO): ' + version)

if options.board is not None:
   if options.board.endswith(".yaml"):
      path = options.board
   else:
      path = share_dir + '/data/boards/' + options.board + '.yaml'
   if os.path.exists(path):
      board = yaml.load(open(path, 'r'))
   else:
      sys.exit(__file__ + '(ERROR): board <' + options.board + '> not exists.')
   if options.device not in board:
      sys.exit(__file__ + '(ERROR): the device <' + options.device + '> is not ' +
                          'supported in the board <' + options.board + '>.')
   if 'prog' in board['tool']:
      print (__file__ + '(INFO): <tool> was taken from the board file.')
      options.tool = board['tool']['prog'][0]
   if 'position' in board[options.device][0]:
      print (__file__ + '(INFO): <position> was taken from the board file.')
      options.position = board[options.device][0]['position']
   if 'name' in board[options.device][0]:
      print (__file__ + '(INFO): <memname> was taken from the board file.')
      options.memname = board[options.device][0]['name']
   if 'width' in board[options.device][0]:
      print (__file__ + '(INFO): <width> was taken from the board file.')
      options.width = board[options.device][0]['width']

if not os.path.exists(options.output_dir):
   os.makedirs(options.output_dir)
   print (__file__ + '(INFO): <' + options.output_dir + '> was created.')

## Creating batch file [when nedded] ##########################################

if options.tool == 'ise':
   text = ""
   path = share_dir + '/data/tools/program/impact/'
   if options.device == 'fpga':
      text += getTextProg(options, path + 'fpga')
   if options.device == 'spi':
      text += getTextProg(options, path + 'mcs_spi') + getTextProg(options, path + 'spi')
   if options.device == 'bpi':
      text += getTextProg(options, path + 'mcs_bpi') + getTextProg(options, path + 'bpi')
   if options.device == 'xcf':
      text += getTextProg(options, path + 'mcs_xcf')
   if options.device == 'detect':
      text += getTextProg(options, path + 'detect')
   if options.device == 'unlock':
      text += getTextProg(options, path + 'unlock')
   text += "quit\n"
   text += '# Generated by ' + version + '\n'
   batch = options.output_dir + '/impact.cmd'
   open(batch, 'w').write(text)
   print (__file__ + '(INFO): <' + batch + '> was created.')

## Running the tool ###########################################################

if options.tool == 'ise':
   lib = "/usr/lib/libusb-driver.so";
   if os.path.exists(lib):
      os.environ['LD_PRELOAD'] = str(lib)
      print (__file__ + '(INFO): <' + lib + '> exists.')
   command = 'impact -batch ' + batch
if options.tool == 'quartus2':
   command  = "jtagconfig; "
   command += "quartus_pgm -c USB-blaster --mode jtag -o "
   command += "'p;" + options.bit + "@" + str(options.position) + "'"
os.system(command)
