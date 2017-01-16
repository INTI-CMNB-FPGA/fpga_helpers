#
# Tcl to synthesize an existing project with the Vendor Tool (if supported)
# Copyright (C) 2017 INTI, Rodrigo A. Melo <rmelo@inti.gob.ar>
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

# Parsing command line
set TASK [expr {[lindex $::argv 1] eq "" ? "bit" : [lindex $::argv 1]}]
if {$TASK!="syn" && $TASK!="imp" && $TASK!="bit"} {
   puts "$TASK is not a supported TASK option [syn, imp, bit].\n"
   exit 1
}

# Discovering used vendor tool
set TOOL "Unknown"
catch {globals get display_type;                set TOOL "ise"}
catch {list_features;                           set TOOL "vivado"}
catch {get_environment_info -operating_system;  set TOOL "quartus2"}
catch {defvar_set -name "FORMAT" -value "VHDL"; set TOOL "libero-soc"}

##[ ISE ]######################################################################
if { $TOOL=="ise" } {
   project open [glob -nocomplain *.xise]
   process run "Synthesize"                -force rerun
   if { $TASK=="syn" } {project_close; exit 0}
   process run "Translate"                 -force rerun
   process run "Map"                       -force rerun
   process run "Place & Route"             -force rerun
   if { $TASK=="imp" } {project_close; exit 0}
   process run "Generate Programming File" -force rerun
   project close
##[ Vivado ]###################################################################
} elseif { $TOOL=="vivado" } {
   open_project [glob -nocomplain *.xpr]
   reset_run synth_1
   launch_runs synth_1
   wait_on_run synth_1
   if { $TASK=="syn" } {close_project; exit 0}
   open_run synth_1
   launch_runs impl_1
   wait_on_run impl_1
   if { $TASK=="imp" } {close_project; exit 0}
   open_run impl_1
   launch_run impl_1 -to_step write_bitstream
   wait_on_run impl_1
   close_project
##[ Quartus2 ]#################################################################
} elseif { $TOOL=="quartus2" } {
   package require ::quartus::flow
   project_open -force [glob -nocomplain *.qpf]
   execute_module -tool map
   if { $TASK=="syn" } {project_close; exit 0}
   execute_module -tool fit
   execute_module -tool sta
   if { $TASK=="imp" } {project_close; exit 0}
   execute_module -tool asm
   project_close
##[ Libero-SoC ]###############################################################
} elseif { $TOOL=="libero-soc" } {
   open_project [glob -nocomplain *.prjx]
   run_tool -name {COMPILE}
   if { $TASK=="syn" } {close_project; exit 0}
   run_tool -name {PLACEROUTE}
   run_tool -name {VERIFYTIMING}
   if { $TASK=="imp" } {close_project; exit 0}
   run_tool -name {GENERATEPROGRAMMINGFILE}
   close_project
##[ Other ]####################################################################
} else {
   puts "Unsupported vendor tool."
   exit 1
}
