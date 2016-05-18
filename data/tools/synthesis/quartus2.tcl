#
# Tcl for Altera Quartus2 Tool
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
package require ::quartus::project
package require ::quartus::flow

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

array set options [cmdLineParser "Altera Quartus2"]
set  RUN   $opts(run)
set  OPT   $opts(opt)
set  ODIR  temp
file mkdir $ODIR

project_new quartus2 -overwrite
set_global_assignment -name PROJECT_OUTPUT_DIRECTORY $ODIR

switch $OPT {
   "area"  {
      set_global_assignment -name OPTIMIZATION_MODE "AGGRESSIVE AREA"
      set_global_assignment -name OPTIMIZATION_TECHNIQUE AREA
   }
   "power" {
      set_global_assignment -name OPTIMIZATION_MODE "AGGRESSIVE POWER"
      set_global_assignment -name OPTIMIZE_POWER_DURING_SYNTHESIS "EXTRA EFFORT"
      set_global_assignment -name OPTIMIZE_POWER_DURING_FITTING "EXTRA EFFORT"
   }
   "speed" {
      set_global_assignment -name OPTIMIZATION_MODE "AGGRESSIVE PERFORMANCE"
      set_global_assignment -name OPTIMIZATION_TECHNIQUE SPEED
   }
}

source options.tcl

if { $RUN=="syn" || $RUN=="imp" || $RUN=="bit"} {
   execute_module -tool map
   file copy -force [glob -nocomplain $ODIR/*.map.rpt] quartus2_syn_$OPT.log
}
if { $RUN=="imp" || $RUN=="bit"} {
   execute_module -tool fit
   execute_module -tool sta
   file copy -force [glob -nocomplain $ODIR/*.fit.rpt] quartus2_imp_$OPT.log
}
if {$RUN=="bit"} {
   execute_module -tool asm
}

project_close