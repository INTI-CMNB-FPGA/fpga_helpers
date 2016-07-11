#fpga_device   <FPGA> [-tool <TOOL>]        Return: none
#fpga_file     <FILE> [-lib <LIBRARY>]      Return: none
#fpga_top      <TOP>                        Return: none
#fpga_get_tool                              Return: running tool

#dev
fpga_device "xc7a100t-3-csg324" -tool "ise"
fpga_device "xc7a100t-3-csg324" -tool "vivado"
fpga_device "5CGXFC7C7F23C8"    -tool "quartus2"
#/dev

#prj
fpga_file "core_file.vhdl"    -lib "LIB_NAME"
fpga_file "package_file.vhdl" -lib "LIB_NAME"
fpga_file "top_file.vhdl"
fpga_top  "TOP_NAME"
#/prj

#opt
if {[fpga_get_tool] == "ise"} {
   project set "FSM Encoding Algorithm" "Sequential" -process "Synthesize - XST"
} elseif {[fpga_get_tool] == "vivado"} {
   set_property "steps.synth_design.args.fsm_extraction" "sequential" [get_runs synth_1]
} elseif {[fpga_get_tool] == "quartus2"} {
   set_global_assignment -name STATE_MACHINE_PROCESSING SEQUENTIAL
}
#/opt
