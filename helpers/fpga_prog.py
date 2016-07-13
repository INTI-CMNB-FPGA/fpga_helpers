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

lib_dir   = os.path.dirname(os.path.abspath(__file__)) + '/../helpers'
share_dir = os.path.dirname(os.path.abspath(__file__)) + '/..'

if not os.path.exists(share_dir + '/data'):
   share_dir = '/usr/share/fpga-helpers'
   lib_dir = '/usr/lib/fpga-helpers'

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
   metavar='FILE.bit',
   help='BitStream to be transferred'
)
parser.add_argument(
   '-t', '--tool',
   metavar='NAME',
   default=None,
   choices=['ise','quartus2'],
   help='NAME of the vendor tool to be used [ise (default)|quartus2]'
)

devices = parser.add_argument_group('device arguments')
devices.add_argument(
   '-d', '--device',
   metavar='TYPE',
   default='fpga',
   choices=['fpga', 'spi', 'bpi', 'xcf', 'detect', 'unlock'],
   help='TYPE of the target device [fpga(default)|spi|bpi|xcf|detect|unlock]'
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
   metavar='NAME',
   default='UNDEFINED',
   help='NAME of the target memory (when applicable) [UNDEFINED]'
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
   metavar='NAME|FILE',
   help='NAME of a supported board or FILE (.yaml) of a new/custom board ' +
        '(note: if you use the board option, -p, -m and -w could be ' +
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
      board = yaml.load(file(path, 'r'))
   else:
      sys.exit(__file__ + '(ERROR): board <' + options.board + '> not exists.')
   if not options.tool in board['tool']['prog']:
      sys.exit(
         __file__ + '(ERROR): <board> ' + options.board +
         ' is not supported by the <tool> ' + options.tool + '.'
      )
   if options.device not in board:
      sys.exit(__file__ + '(ERROR): the device <' + options.device + '> is not ' +
                          'supported in the board <' + options.board + '>.')
   if options.tool is None and 'prog' in board['tool']:
      print (__file__ + '(INFO): <tool> was taken from the board file.')
      options.tool = board['tool']['prog']
   if 'position' in board[options.device][0]:
      print (__file__ + '(INFO): <position> was taken from the board file.')
      options.position = board[options.device][0]['position']
   if 'name' in board[options.device][0]:
      print (__file__ + '(INFO): <memname> was taken from the board file.')
      options.memname = board[options.device][0]['name']
   if 'width' in board[options.device][0]:
      print (__file__ + '(INFO): <width> was taken from the board file.')
      options.width = board[options.device][0]['width']

if options.tool is None:
   options.tool = 'ise'

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
   file(batch, 'w').write(text)
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
   print command
os.system(command)
