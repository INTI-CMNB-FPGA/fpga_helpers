#dev
set obj [current_project]
set_property "part" "xc7a100tcsg324-3" $obj
#/dev

#prj
read_vhdl -library LIB_NAME ../core/core_file.vhdl
read_vhdl -library LIB_NAME ../core/package_file.vhdl
read_vhdl ../core/top_file.vhdl
set_property top TOP_NAME [current_fileset]
#/prj

#opt
#set obj [get_runs synth_1]
#set_property "steps.synth_design.args.fsm_extraction" "sequential" $obj
#/opt
