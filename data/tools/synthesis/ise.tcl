#
# Tcl for Xilinx ISE Tool
# Copyright (C) 2016 INTI, Rodrigo A. Melo <rmelo@inti.gob.ar>
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

package require cmdline

###################################################################################################
# Functions                                                                                       #
###################################################################################################

proc cmdLineParser {TOOL} {

   set parameters {
       {run.arg  "syn"    "What to RUN  [syn, imp, bit]"}
       {opt.arg  "user"   "OPTimization [user, area, power, speed]"}
   }

   set usage "- A Tcl script to synthesise with $TOOL Tool"
   if {[catch {array set options [cmdline::getoptions ::argv $parameters $usage]}]} {
      puts [cmdline::usage $parameters $usage]
      exit 1
   }

   set ERROR ""

   if {$opts(run)!="syn" && $opts(run)!="imp" && $opts(run)!="bit"} {
      append ERROR "<$opts(run)> is not a supported RUN option.\n"
   }

   if {$opts(opt)!="user" && $opts(opt)!="area" && $opts(opt)!="power" && $opts(opt)!="speed"} {
      append ERROR "<$opts(opt)> is not a supported OPTimization.\n"
   }

   if {$ERROR != ""} {
      puts $ERROR
      puts "Use -help to see available options."
      exit 1
   }

   return [array get options]
}

###################################################################################################
# Main                                                                                            #
###################################################################################################

array set options [cmdLineParser "Xilinx ISE"]
set  RUN   $opts(run)
set  OPT   $opts(opt)
set  ODIR  temp
file mkdir $ODIR

if { [ file exists ise.xise ] } {
   file delete ise.xise
}
project new ise.xise
project set "Work Directory" $ODIR/xst

switch $OPT {
   "area"  {
      project set "Optimization Goal" "Area"
   }
   "power" {
      project set "Optimization Goal" "Area"
      project set "Power Reduction"   "true" -process "Synthesize - XST"
      project set "Power Reduction"   "high" -process "Map"
      project set "Power Reduction"   "true" -process "Place & Route"
   }
   "speed" {
      project set "Optimization Goal" "Speed"
   }
}

source options.tcl

if { $RUN=="syn" || $RUN=="imp" || $RUN=="bit"} {
   process run "Synthesize"    -force rerun
   file copy -force [glob -nocomplain *.syr] ise_syn_$OPT.log
}
if { $RUN=="imp" || $RUN=="bit"} {
   process run "Translate"     -force rerun
   process run "Map"           -force rerun
   process run "Place & Route" -force rerun
   file copy -force [glob -nocomplain *.par] ise_imp_$OPT.log
}
if {$RUN=="bit"} {
   process run "Generate Programming File" -force rerun
}
