#fpga_device <FPGA> -tool <TOOL>
#fpga_file   <FILE> -lib <LIBRARY>
#fpga_top    <TOP>
#fpga_set    <KEY> <VALUE> -tool <TOOL>

###############################################################################
#ISE
###############################################################################
#dev
#project set family  "Artix7"
#project set device  "xc7a100t"
#project set package "csg324"
#project set speed   "-3"
#/dev

#prj
#lib_vhdl new "LIB_NAME"
#xfile add "core_file.vhdl" -lib_vhdl "LIB_NAME"
#xfile add "package_file.vhdl" -lib_vhdl "LIB_NAME"
#xfile add "top_file.vhdl"
#project set top "TOP_NAME"
#/prj

#opt
#project set "FSM Encoding Algorithm" "Sequential" -process "Synthesize - XST"
#/opt

###############################################################################
#Vivado
###############################################################################
#dev
#set obj [current_project]
#set_property "part" "xc7a100tcsg324-3" $obj
#/dev

#prj
#add_files core_file.vhdl
#add_files package_file.vhdl
#add_files top_file.vhdl
#set_property library LIB_NAME [get_files core_file.vhdl]
#set_property library LIB_NAME [get_files package_file.vhdl]
#set_property top TOP_NAME     [current_fileset]
#/prj

#opt
#set obj [get_runs synth_1]
#set_property "steps.synth_design.args.fsm_extraction" "sequential" $obj
#/opt

###############################################################################
# Quartus2
###############################################################################
#dev
set_global_assignment -name DEVICE 5CGXFC7C7F23C8
#/dev

#prj
set_global_assignment -name VHDL_FILE core_file.vhdl -library LIB_NAME
set_global_assignment -name VHDL_FILE package_file.vhdl -library LIB_NAME
set_global_assignment -name VHDL_FILE top_file.vhdl
set_global_assignment -name TOP_LEVEL_ENTITY TOP_NAME
#/prj

#opt
set_global_assignment -name STATE_MACHINE_PROCESSING SEQUENTIAL
#/opt
