#dev
project set family  "Artix7"
project set device  "xc7a100t"
project set package "csg324"
project set speed   "-3"
#/dev

#prj
lib_vhdl new "LIB_NAME"
xfile add "../core/core_file.vhdl" -lib_vhdl "LIB_NAME"
xfile add "../core/package_file.vhdl" -lib_vhdl "LIB_NAME"
xfile add "../core/top_file.vhdl"
project set top "TOP_NAME"
#/prj

#opt
#project set "FSM Encoding Algorithm" "Sequential" -process "Synthesize - XST"
#/opt
