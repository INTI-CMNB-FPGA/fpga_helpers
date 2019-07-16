#!/usr/bin/python
#
# FPGA Wizard
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

import sys, os, readline, re, glob, shutil
import database as db
import common

def get_input(prompt):
    global default
    prompt += " > "
    if default:
       print(prompt)
       return ""
    try:    # Python2
       return raw_input(prompt)
    except: # Python3
       return input(prompt)

def get_top(top_file):
    text = open(top_file).read()
    result = re.findall(r"entity (.*) is",text,re.I) or re.findall(r"module (.*)\(",text,re.I)
    if result:
       return result[0]
    else:
       sys.exit("fpga_wizard (ERROR): I had not found an entity/module declaration")

def complete(text, state):
    for opt in alternatives:
        if opt.startswith(text):
           if not state:
              return opt
           else:
              state -= 1

def set_alternatives(aux):
    global alternatives
    alternatives = aux
    readline.set_completer(complete)

def collect_data():
    # Config autocomplete
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    global alternatives

    # Default Values
    options              = {}
    options['tool']      = 'vivado'
    options['tcl_path']  = '../tcl'
    options['top_file']  = None
    options['files']     = []
    options['fpga_name'] = 'UNSPECIFIED'
    options['fpga_pos']  = '1'
    options['spi_width'] = '1'
    options['bpi_width'] = '8'

    print("INSTRUCTIONS: left EMPTY for default option and press TAB for autocomplete.")

    set_alternatives(db._tools) # available tools
    options['tool'] = get_input("* TOOL to be used? [%s]" % options['tool']) or options['tool']
    if options['tool'] not in alternatives:
       sys.exit("fpga_wizard (ERROR): unsupported tool")

    print("NOTE: if there are no Tcl files in the target path, they are created.")
    readline.set_completer() # browse filesystem
    options['tcl_path'] = get_input("* Path to the Tcl files? [%s]" % options['tcl_path']) or options['tcl_path']

    readline.set_completer() # browse filesystem
    try:
       default = glob.glob('*.v*')[0] # vhdl, vhd, v (probably only one file)
    except:
       default = options['top_file']
    options['top_file'] = get_input("* Top Level file? [%s]" % default) or default
    if options['top_file'] is None or not os.path.exists(options['top_file']):
       sys.exit("fpga_wizard (ERROR): the specified top level does not exists")
    options['top_name'] = get_top(options['top_file'])

    readline.set_completer() # browse filesystem
    print("* Add files to the project (empty file to FINISH).")
    morefiles = 1;
    while (morefiles):
       file = get_input("  * Path to the file [FINISH]")
       lib  = ""
       if len(file):
          lib = get_input("  * In library [None]")
       if len(file):
          options['files'].append([file,lib])
       else:
          morefiles = 0

    set_alternatives(db._boards)
    options['board'] = get_input("* Board to be used? [None]")
    if options['board'] and options['board'] not in alternatives:
       sys.exit("fpga_wizard (ERROR): unsupported board")
    if options['board']:
       options.update(db._boards[options['board']])
    else:
       # FPGA
       set_alternatives([])
       print("* Specify the FPGA")
       options['fpga_name'] = get_input("  * Device [%s]" % options['fpga_name']) or options['fpga_name']
       if len(options['fpga_name']):
          set_alternatives([str(i) for i in db._fpga_pos])
          options['fpga_pos'] = get_input("  * Position [%s]" % options['fpga_pos']) or options['fpga_pos']
          if int(options['fpga_pos']) not in db._fpga_pos:
             sys.exit("fpga_wizard (ERROR): unsupported FPGA position (%d to %d)" % (db._fpga_pos[0], db._fpga_pos[-1]))
       # SPI
       set_alternatives([])
       print("* Specify an attached SPI")
       options['spi_name'] = get_input("  * Device [None]")
       if len(options['spi_name']):
          set_alternatives([str(i) for i in db._spi_width])
          options['spi_width'] = get_input("  * Width in bits [%s]" % options['spi_width']) or options['spi_width']
          if int(options['spi_width']) not in db._spi_width:
             sys.exit("fpga_wizard (ERROR): unsupported SPI data width (%s)" % "|".join(str(n) for n in db._spi_width))
       # BPI
       set_alternatives([])
       print("* Specify an attached BPI")
       options['bpi_name'] = get_input("  * Device [None]")
       if len(options['bpi_name']):
          set_alternatives([str(i) for i in db._bpi_width])
          options['bpi_width'] = get_input("* Width in bits [%s]" % options['bpi_width']) or options['bpi_width']
          if int(options['bpi_width']) not in db._bpi_width:
             sys.exit("fpga_wizard (ERROR): unsupported BPI data width (%s)" % "|".join(str(n) for n in db._bpi_width))

    return options

def main():
    global default
    cli_opt = common.get_options(__file__)
    default = cli_opt.default

    options = collect_data()

    # Copy Tcl files
    if not os.path.exists(options['tcl_path']):
       os.makedirs(options['tcl_path'])
       print("fpga_wizard (INFO): directory %s was created" % options['tcl_path'])
    tcl_orig = common.get_script_path(__file__) + "/tcl"
    if not os.path.exists(options['tcl_path'] + "/Makefile"):
       shutil.copy(tcl_orig + '/Makefile', options['tcl_path'])
       print("fpga_wizard (INFO): Makefile was copy to %s" % options['tcl_path'])
    if not os.path.exists(options['tcl_path'] + "/synthesis.tcl"):
       shutil.copy(tcl_orig + '/synthesis.tcl', options['tcl_path'])
       print("fpga_wizard (INFO): synthesis.tcl was copy to %s" % options['tcl_path'])
    if not os.path.exists(options['tcl_path'] + "/programming.tcl"):
       shutil.copy(tcl_orig + '/programming.tcl', options['tcl_path'])
       print("fpga_wizard (INFO): programming.tcl was copy to %s" % options['tcl_path'])

    # Creating files
    optfile = ""
    # Config devices
    if 'fpga_name' in options and len(options['fpga_name']):
       optfile += "set fpga_name %s\n" % options['fpga_name']
       optfile += "set fpga_pos  %s\n" % options['fpga_pos']
    if 'spi_name'  in options and len(options['spi_name']):
       optfile += "set spi_name  %s\n" % options['spi_name']
       optfile += "set spi_width %s\n" % options['spi_width']
    if 'bpi_name'  in options and len(options['bpi_name']):
       optfile += "set bpi_name  %s\n" % options['bpi_name']
       optfile += "set bpi_width %s\n" % options['bpi_width']
    optfile += "\n"
    # Set FPGA
    if 'fpga_name' in options and options['fpga_name'] is not None:
       optfile += "fpga_device   $fpga_name\n"
    optfile += "\n"
    # Add files and specify the top level
    for file,lib in options['files']:
        if len(lib):
           optfile += "fpga_file     %-30s -lib %s\n" % (file,lib)
        else:
           optfile += "fpga_file     %-30s\n"         % (file)
    if 'top_file' in options:
       optfile += "fpga_file     %-30s -top %s\n"%(options['top_file'],options['top_name'])
    # The Makefile
    makefile = common.get_makefile_content(
       tool=options['tool'], task=None, dev=None, path=options['tcl_path']
    )

    # Gen files and end
    open("Makefile", 'w').write(makefile)
    open("options.tcl", 'w').write(optfile)
    print("fpga_wizard (INFO): Makefile and options.tcl were generated")

if __name__ == "__main__":
   main()
