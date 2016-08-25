#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# FPGA Deps collects the files of a HDL project
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

# Assumptions:
# * Files are well formed.
# * VHDL:
#   * A file could have one or more packages and/or one or more entities.
#   * The architectures must be in the file where their entity is.
#   * Configurations are no supported.
# * Verilog:
#   * A file could have one or more modules.

import argparse, os, sys, re, mimetypes

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

version = 'FPGA Deps (FPGA Helpers) v' + getVersion(share_dir)

parser = argparse.ArgumentParser(
   prog='fpga_deps',
   description='Collects the files of a HDL project.'
)

parser.add_argument(
   '-v', '--version',
   action='version',
   version=version
)

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

if (options.verbose):
   print ("\nOptions: " + str(options))

dir = "."
for i in range(0, options.deep):
    dir += "../"

## Collecting files ###########################################################

files_all = []
for root, dirs, files in os.walk(dir):
    for file in files:
        filepath = root+'/'+file
        if file.endswith('.vhdl') or \
           file.endswith('.vhd')  or \
           file.endswith('.sv')   or \
           file.endswith('.v')       :
           files_all.append(filepath)

if (options.verbose):
   print ("\nFiles: " + str(files_all))

qty = len(files_all)
if (qty < 1):
   sys.exit('fpga_deps (ERROR): no files were found.')

if (options.verbose):
   print("\nFiles found: " + str(qty))

## Collecting data from founded files #########################################

# Data to collect:
# * Inside of which LIBRARY is each PACKAGE.
# * Inside of which PACKAGE is each COMPONENT.
# * In which FILE is defined each COMPONENT and PACKAGE.
# * In which FILE is defined each MODULE.
# Warnings:
# * A file could contain more than a PACKAGE, COMPONENT or MODULE.
# * There may be repeated names!
#   * More than one LIBRARY can contain PACKAGEs with the same name (the same
#     PACKAGE name can be on more than one library).

knownlibs = ["ieee", "std", "unisim"]
cnt = 1

lib_pkg  = []
file_pkg = []
file_ent = []
pkg_com  = []

for file in files_all:
    data = open(file, 'r').read();
    # Searching LIBRARYs and PACKAGEs on lines such as:
    # use LIBRARY.PACKAGE.xyz;
    match = re.findall('use\s+(.+)\.(.+)\..+;', data, re.IGNORECASE);
    for lib,pkg in match:
        if lib.lower() not in knownlibs:
           lib_pkg.append([lib, pkg])
    # Searching names of PACKAGEs and FILEs which include them:
    # package PACKAGE is
    match = re.findall('package\s+(.+)\s+is', data, re.IGNORECASE);
    for pkg in match:
        file_pkg.append([file,pkg])
        # Searching COMPONENTs inside PACKAGEs:
        # component COMPONENT is
        match = re.findall('component\s+(.+)\s+is', data, re.IGNORECASE)
        for com in match:
            pkg_com.append([pkg,com])
    # Searching names of ENTITYs and FILEs which include them:
    # entity ENTITY is
    match = re.findall('entity\s+(.+)\s+is', data, re.IGNORECASE);
    for ent in match:
        file_ent.append([file,ent])
    #
    cnt+=1
    if cnt%5==0 and options.verbose:
       print ("%4d of %4d files were processed" % (cnt,qty))

lib_pkg_clean = []
for values in lib_pkg:
    if values not in lib_pkg_clean:
       lib_pkg_clean.append(values)
lib_pkg = lib_pkg_clean

if (options.verbose):
   print ("%4d of %4d files were processed" % (qty,qty))
   print ("\nlib_pkg:  " + str(lib_pkg))
   print ("\nfile_pkg: " + str(file_pkg))
   print ("\npkg_com:  " + str(pkg_com))
   print ("\nfile_ent: " + str(file_ent))

###############################################################################

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
