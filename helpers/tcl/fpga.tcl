#
# Vendor independat Tcl for FPGA Tools
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
# Parsing the Command Line arguments                                                              #
###################################################################################################

proc cmdLineParser {} {

   set parameters {
       {tool.arg "none"   "Vendor TOOL  [ise, vivado, quartus2]"}
       {run.arg  "syn"    "What to RUN  [syn, imp, bit, clean]"}
       {opt.arg  "user"   "OPTimization [user, area, power, speed]"}
   }

   set usage "- A Tcl script to work with FPGA Tools in a Vendor Independent way"
   if {[catch {array set options [cmdline::getoptions ::argv $parameters $usage]}]} {
      puts [cmdline::usage $parameters $usage]
      exit 1
   }

   set ERROR ""

   if { $options(tool)=="none"} {
      append ERROR "You must specify a supported Vendor TOOL\n"
   }

   if {$options(tool)!="ise" && $options(tool)!="vivado" && $options(tool)!="quartus2"} {
      append ERROR "<$options(tool)> is not a supported Vendor TOOL.\n"
   }

   if {
       $options(run)!="syn"   &&
       $options(run)!="imp"   &&
       $options(run)!="bit"   &&
       $options(run)!="clean"
      } {
      append ERROR "<$options(run)> is not a supported RUN option.\n"
   }

   if {
       $options(opt)!="user"  &&
       $options(opt)!="area"  &&
       $options(opt)!="power" &&
       $options(opt)!="speed"
      } {
      append ERROR "<$options(opt)> is not a supported OPTimization.\n"
   }

   if {$ERROR != ""} {
      puts $ERROR
      puts "Use -help to see available options."
      exit 1
   }

   return [array get options]
}

###################################################################################################
# Small helpers                                                                                   #
###################################################################################################

proc readFile {PATH} {set fp [open $PATH r];set data [read $fp];close $fp;return $data}
proc writeFile {PATH MODE DATA} {set fp [open $PATH $MODE];puts $fp $DATA;close $fp}
proc getSeparator {CHAR QTY} {
   set sep "";for {set i 0} {$i < $QTY} {incr i} {append sep $CHAR};return $sep
}

###################################################################################################
# Xilinx ISE Tool                                                                                 #
###################################################################################################

proc toolIse {ODIR RUN OPT} {

   if { [ file exists ise.xise ] } {
      file delete ise.xise
   }
   project new ise.xise
   project set "Work Directory" $ODIR/xst

   if {$RUN != "clean"} {
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
      source ise_cfg.tcl
   }

   if { $RUN=="syn" || $RUN=="imp" || $RUN=="bit"} {
      process run "Synthesize" -force rerun
      file copy -force [glob -nocomplain *.syr] ise_syn_$OPT.log
   }
   if { $RUN=="imp" || $RUN=="bit"} {
      process run "Translate" -force rerun
      process run "Map" -force rerun
      process run "Place & Route" -force rerun
      file copy -force [glob -nocomplain *.par] ise_imp_$OPT.log
   }
   if {$RUN=="bit"} {
      process run "Generate Programming File" -force rerun
   }

   if { $RUN=="clean" } {
      project clean
      catch {
         file delete -force $ODIR
         file delete -force _xmsgs
         file delete -force iseconfig
         file delete -force [glob -nocomplain *.xise]
         file delete -force [glob -nocomplain *.gise]
         file delete -force [glob -nocomplain *.ncd]
         file delete -force [glob -nocomplain *.html]
      }
   }

}

proc reportIse {ODIR OPT} {
   set systemTime [clock seconds]
   set wdata ""
   append wdata "TimeStamp: "
   append wdata [clock format $systemTime -format {%Y-%m-%d  %H:%M}]\n
   append wdata "Optimized by $OPT\n\n"
   append wdata "Notes: N/A\n\n"
   if { [file exists [glob -nocomplain *.syr]] } {
      set PATH [glob -nocomplain *.syr]
      set rdata [readFile $PATH ]
      append wdata [getSeparator "#" 100]\n
      append wdata "Synthesis\n"
      append wdata [getSeparator "#" 100]\n
      regexp -nocase {(Slice Logic Utilization[\w\s\n-:]*)\n-*\nPartition} $rdata -> result
      append wdata "$result\n"
      regexp -nocase {Minimum period:\s([\d.]*)} $rdata -> result
      set MHZ [expr 1/[expr 0.001 * $result]]
      append wdata "Maximum Frequency: $MHZ MHz\n"
   }
   if { [file exists [glob -nocomplain *.par]] } {
      set PATH [glob -nocomplain *.par]
      set rdata [readFile $PATH ]
      append wdata [getSeparator "#" 100]\n
      append wdata "Implementation\n"
      append wdata [getSeparator "#" 100]\n
      regexp -nocase {(Slice Logic Utilization[\w\s\n-:]*)\n\n\nOverall} $rdata -> result
      append wdata "$result\n\n"
      regexp -nocase {(\d*\.\d*)ns} $rdata -> result
      set MHZ [expr 1/[expr 0.001 * $result]]
      append wdata "Maximum Frequency: $MHZ MHz\n"
   }
   writeFile ise.resume w $wdata
}
###################################################################################################
# Xilinx Vivado Tool                                                                              #
###################################################################################################

proc toolVivado {ODIR RUN OPT} {

   create_project -force vivado $ODIR

   switch $OPT {
      "area"  {
         set obj [get_runs synth_1]
         set_property strategy "Flow_AreaOptimized_high"                       $obj
         set_property "steps.synth_design.args.directive" "AreaOptimized_high" $obj
         set_property "steps.synth_design.args.control_set_opt_threshold" "1"  $obj

         set obj [get_runs impl_1]
         set_property strategy "Area_Explore"                                  $obj
         set_property "steps.opt_design.args.directive" "ExploreArea"          $obj
      }
      "power" {
         #enable power_opt_design and phys_opt_design
         set obj [get_runs synth_1]
         set_property strategy "Vivado Synthesis Defaults"                     $obj

         set obj [get_runs impl_1]
         set_property strategy "Power_DefaultOpt"                              $obj
         set_property "steps.power_opt_design.is_enabled" "1"                  $obj
         set_property "steps.phys_opt_design.is_enabled" "1"                   $obj
      }
      "speed" {
         #enable phys_opt_design
         set obj [get_runs synth_1]
         set_property strategy "Flow_PerfOptimized_high"                       $obj
         set_property "steps.synth_design.args.fanout_limit" "400"             $obj
         set_property "steps.synth_design.args.keep_equivalent_registers" "1"  $obj
         set_property "steps.synth_design.args.resource_sharing" "off"         $obj
         set_property "steps.synth_design.args.no_lc" "1"                      $obj
         set_property "steps.synth_design.args.shreg_min_size" "5"             $obj

         set obj [get_runs impl_1]
         set_property strategy "Performance_Explore"                           $obj
         set_property "steps.opt_design.args.directive" "Explore"              $obj
         set_property "steps.place_design.args.directive" "Explore"            $obj
         set_property "steps.phys_opt_design.is_enabled" "1"                   $obj
         set_property "steps.phys_opt_design.args.directive" "Explore"         $obj
         set_property "steps.route_design.args.directive" "Explore"            $obj
      }
   }

   source vivado_cfg.tcl

   if { $RUN=="syn" || $RUN=="imp" || $RUN=="bit"} {
      launch_runs synth_1
      wait_on_run synth_1
      open_run synth_1
      set UTILIZATION [report_utilization -return_string]
      set TIMING [report_timing -return_string]
      #puts $UTILIZATION
      #puts $TIMING
      writeFile vivado_syn_$OPT.log w $UTILIZATION
      writeFile vivado_syn_$OPT.log a $TIMING
   }
   if { $RUN=="imp" || $RUN=="bit"} {
      launch_runs impl_1
      wait_on_run impl_1
      open_run impl_1
      report_io    -file $ODIR/io_imp.rpt
      report_power -file $ODIR/power_imp.rpt
      set UTILIZATION [report_utilization -return_string]
      set TIMING [report_timing -return_string]
      writeFile vivado_imp_$OPT.log w $UTILIZATION
      writeFile vivado_imp_$OPT.log a $TIMING
   }
   if {$RUN=="bit"} {
      launch_run impl_1 -to_step write_bitstream
      wait_on_run impl_1
   }

   catch {
      file rename -force {*}[glob -nocomplain vivado.jou] $ODIR
      file rename -force {*}[glob -nocomplain vivado.log] $ODIR
      file rename -force {*}[glob -nocomplain *backup.jou] $ODIR
      file rename -force {*}[glob -nocomplain *backup.log] $ODIR
   }

   catch { file rename -force {*}[glob -nocomplain webtalk*] $ODIR }
   if {$RUN=="clean"} {
      file delete -force $ODIR
      catch {file delete -force {*}[glob -nocomplain *.log]}
   }

}

###################################################################################################
# Altera Quartus2 Tool                                                                            #
###################################################################################################

proc toolQuartus2 {ODIR RUN OPT} {

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

   source quartus2_cfg.tcl

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

   if {$RUN=="clean"} {
      file delete -force $ODIR
      file delete -force db
      file delete -force incremental_db
      file delete -force quartus2.qpf
      file delete -force quartus2.qsf
      file delete -force quartus2.qws
      file delete -force {*}[glob -nocomplain *.log]
   }

}

###################################################################################################
# Main                                                                                            #
###################################################################################################

array set options [cmdLineParser]

set ODIR temp-$options(tool)
file mkdir $ODIR

switch $options(tool) {
   "ise"      {
      toolIse $ODIR $options(run) $options(opt)
      reportIse $ODIR $options(opt)
   }
   "vivado"   {
      toolVivado $ODIR $options(run) $options(opt)
   }
   "quartus2" {
      package require ::quartus::project
      package require ::quartus::flow
      toolQuartus2 $ODIR $options(run) $options(opt)
   }
}
