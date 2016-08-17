#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# FPGA Tree collects the files of a HDL project
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

# The collected info is:
# * Inside of which LIBRARY is each PACKAGE.
# * Inside of which PACKAGE is each COMPONENT.
# * In which FILE is defined each COMPONENT and PACKAGE.

import argparse, os, sys, glob

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

version = 'FPGA Tree (FPGA Helpers) v' + getVersion(share_dir)

parser = argparse.ArgumentParser(
   prog='fpga_tree',
   description='Collects the files of a HDL project.'
)

parser.add_argument(
   '-v', '--version',
   action='version',
   version=version
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

##

dir = ""
for i in range(0, options.deep):
    dir += "../"

files_all = []
for root, dirs, files in os.walk(dir):
    for file in files:
        if file.endswith('.vhdl') or \
           file.endswith('.vhd')  or \
           file.endswith('.sv')   or \
           file.endswith('.v')       :
           files_all.append(root+'/'+file)

print (files_all)

qty = len(files_all)
if (qty < 1):
   sys.exit('fpga_tree (ERROR): no files were found.')

print("Files found: " + str(qty))

## Coolect info from founded files
#$cnt = 1;
#foreach $file (@files) {
#   open FILE, $file;
#   while (<FILE>) {
#      # Searching LIBRARYs and PACKAGEs on lines such as
#      # use LIBRARY.PACKAGE.xyz;
#      if ($_=~/use\s+(.+)\.(.+)\..+;/i) {
#         $lib = lc($1);
#         if ($lib ne 'ieee' && $lib ne 'std' && $lib ne 'unisim') {
#            $pkg2lib{lc($2)} = lc($1);
#         }
#      }
#      # Searching COMPONENTs inside PACKAGEs
#      if ($_=~/package\s+(.+)\s+is/i) {
#         $pkg = lc($1);
#         $some2file{$pkg} = $file;
#         while (<FILE>) {
#            $line = $_;
#            if ($line=~/end package/i) {
#               break;
#            }
#            if ($_=~/component\s+(.+)\s+is/i) {
#               $com2pkg{lc($1)} = $pkg;
#            }
#         }
#      }
#      # Searching names of ENTITYs and FILEs which include them
#      if ($_=~/entity\s+(.+)\s+is/i) {
#         $some2file{lc($1)} = $file;
#      }
#   }
#   close FILE;
#   $cnt++;
#   print("$cnt of $qty were processed.") if ($cnt%100==0 and $verbosity);
#}
#print("All files were processed.") if ($verbosity);
#if ($verbosity) {
#   print("# Package -> Library\n".(Dump \%pkg2lib));
#   print("# Component -> Package\n".(Dump \%com2pkg));
#   print("# Something -> File\n".(Dump \%some2file));
#}

#%file2some = reverse(%some2file);

## Using the TOP FILE to find all the involved FILES
#unshift(@todo,$top);

#while ($#todo>=0) {
#   $file = shift(@todo); # Remove file of list to analyze
#   print("Analyzing $file ...") if ($verbosity);
#   open FILE, $file;
#   while (<FILE>) {
#      undef $aux;
#      next if ($_=~/^\s*--/); # Jump if comment
#      # Searching used PACKAGEs
#      if ($_=~/use\s+(.+)\.(.+)\..+;/i) {
#         $lib = lc($1);
#         next if ($lib eq 'ieee' || $lib eq 'std' || $lib eq 'unisim'); # Jump if known
#         $pkg = lc($2);
#         print("* lib.pkg: $lib.$pkg") if ($verbosity);
#         $aux = $some2file{$pkg}; # Save probably file to analyze
#      }
#      # Searching used ENTITYs
#      # next if ($_=~/[;@]/);
#      # next if ($_=~/\s*downto\s*|\s+to\s+|signal|constant|variable/);
#      # The instantiation line could be:
#      # LABEL : ENTITY
#      # or
#      # LABEL : entity library.ENTITY [(architecture)]
#      if ($_=~/:.*\.(\w*)|:\s*(\w*)/) {
#         $comp = lc($1).lc($2); # Mark probably entity/component
#      }
#      # Next line must have generic or port map
#      if ($_=~/generic map|port map/) {
#         print("* comp.inst: $comp") if ($verbosity);
#         $aux = $some2file{$comp}; # Save probably file to analyze
#      }
#      # Is the file pending to analyze?
#      next if ((grep $_ eq $aux, @todo) || (grep $_ eq $aux, @done));
#      push(@todo,$aux) if ($aux ne ''); # Mark to analize
#   }
#   close FILE;
#   unshift(@done,$file); # File already processed 
#   #
#   undef $work;
#   $work = $pkg2lib{$file2some{$file}};
#   $work = $pkg2lib{$com2pkg{$file2some{$file}}} if (!$work);
#   $work = "work" if (!$work);
#   unshift(@prj_files,"vhdl $work $file") if ($tool eq 'ise');
#   unshift(@prj_files,"set_global_assignment -name VHDL_FILE $file -library $work")
#      if ($tool eq 'quartus2');
#}
#print("Finished.") if ($verbosity);

#foreach $prj_file (@prj_files) {
#   $text .= "$prj_file\n";
#}

#($name = basename($top)) =~ s/\.[^.]+$//;
#$file  = "$name.prj";
#open(FILE, ">$file") or printError("Failed to create $file.");
#print FILE $text;
#close FILE;

#print join(" \\\n",@done);
