#dev
set_global_assignment -name DEVICE 5CGXFC7C7F23C8
#/dev

#prj
set_global_assignment -name VHDL_FILE ../core/core_file.vhdl    -library LIB_NAME
set_global_assignment -name VHDL_FILE ../core/package_file.vhdl -library LIB_NAME
set_global_assignment -name VHDL_FILE ../core/top_file.vhdl
set_global_assignment -name TOP_LEVEL_ENTITY TOP_NAME
#/prj

#opt
#set_global_assignment -name STATE_MACHINE_PROCESSING SEQUENTIAL
#/opt
