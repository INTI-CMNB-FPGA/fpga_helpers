#!/usr/bin/python
#
# Functions shared between FPGA Helpers
# Copyright (C) 2019 INTI
# Copyright (C) 2019 Rodrigo A. Melo
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

import argparse
import os
import sys
import tempfile

import database as db

def get_script_name(script):
    return os.path.basename(os.path.abspath(script)).split(".")[0]

def get_script_path(script):
    return os.path.dirname(os.path.abspath(script))

"""Here the command line arguments of all the helpers are parsed."""
def get_options(script):
    program = get_script_name(script)
    version = db.__version__
    description = {
        'fpga_wizard' : "A wizard to generate the project files options.tcl and Makefile.",
        'fpga_prog'   : "Transfers a BitStream to a device.",
        'fpga_synt'   : "Run synthesis based on a project file generated with a vendor tool.",
        'fpga_deps'   : "Collects the files of an HDL project."
    }
    epilogue = {
        'fpga_wizard' : "",
        'fpga_prog'   : "Supported boards: %s" % ', '.join(db._boards),
        'fpga_synt'   : "",
        'fpga_deps'   : ""
    }

    parser = argparse.ArgumentParser(
        prog        = program,
        description = description[program],
        epilog      = epilogue[program]
    )
    parser.add_argument(
        '-v', '--version',
        action      = 'version',
        version     = "%s is a member of FPGA Helpers v%s" % (program, version)
    )
    parser.add_argument(
        '--debug',
        action      = 'store_true',
        help        = 'for test purposes'
    )

    if program in ['fpga_wizard']:
       parser.add_argument(
           '--default',
           action      = 'store_true',
           help        = 'to apply default selections'
       )

    if program in ['fpga_prog']:
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
            default     = 'vivado',
            choices     = db._tools,
            help        = "name of the vendor tool to be used (%s) [vivado]" % "|".join(db._tools)
        )
        parser.add_argument(
           '-d', '--device',
           metavar     = 'DEVICE',
           default     = 'fpga',
           choices     = db._devices,
           help        = "type of the target device (%s) [fpga]" % "|".join(db._devices)
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
            choices     = db._fpga_pos,
            help        = 'positive number which represents the POSITION of the device in the ' +
                          'JTAG chain (%d to %d) [1]' % (db._fpga_pos[0],db._fpga_pos[-1])
        )
        parser.add_argument(
            '-w', '--width',
            metavar     = 'WIDTH',
            type        = int,
            default     = 1,
            choices     = db._mem_width,
            help        = 'positive number which representes the WIDTH of bits of the target ' +
                          'memory (%s) [1]' % "|".join(str(n) for n in db._mem_width)
        )

    if program in ['fpga_synt']:
        parser.add_argument(
            '-t', '--task',
            metavar = 'TASK',
            choices = ['syn','imp','bit'],
            default = 'bit',
            help    = 'TASK to be executed (syn|imp|bit) [bit]'
        )
        parser.add_argument(
            'file',
            nargs   = '?',
            metavar = 'PROJECT_FILE',
            help    = 'PROJECT_FILE to be used [auto detected]'
        )

    if program in ['fpga_deps']:
        parser.add_argument(
            '--verbose',
            action='count'
        )
        parser.add_argument(
            'top',
            metavar='TOPFILE',
            nargs='?',
            help='Top Level File'
        )
        parser.add_argument(
            '-d', '--deep',
            metavar='DEEP',
            type=int,
            default=4,
            help='DEEP where to start to search [4]'
        )

    options = parser.parse_args()

    return options

"""Content of the project's Makefile."""
def get_makefile_content(tool, task, dev, path):
    text  = "#!/usr/bin/make\n"
    text += "# Generated with FPGA Helpers v%s\n" % db.__version__
    text += "TOOL=%s\n" % tool
    if task is not None:
       text += "TASK=%s\n" % task
    if dev is not None:
       text += "DEV=%s\n" % dev
    text += "TCLPATH=%s\n" % path
    text += "include $(TCLPATH)/Makefile"
    return text

"""Executes a temporary Makefile."""
def execute_make(script, text):
    program = get_script_name(script)
    target = "prog" if program=="fpga_prog" else "run"
    temp = tempfile.NamedTemporaryFile(mode='w')
    temp.write(text)
    temp.flush()
    try:
        os.system("make -f %s %s" % (temp.name, target))
    except:
        print("%s (ERROR): make failed" % program)
    temp.close()
