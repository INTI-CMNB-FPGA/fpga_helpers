#dev
set obj [current_project]
set_property "part" "xc7a100tcsg324-3" $obj
#/dev

#prj
add_files ../core/core_file.vhdl
add_files ../core/package_file.vhdl
add_files ../core/top_file.vhdl
set_property library LIB_NAME [get_files ../core/core_file.vhdl]
set_property library LIB_NAME [get_files ../core/package_file.vhdl]
set_property top TOP_NAME [current_fileset]
#/prj

#opt
#set obj [get_runs synth_1]
#set_property "steps.synth_design.args.fsm_extraction" "sequential" $obj
#/opt
