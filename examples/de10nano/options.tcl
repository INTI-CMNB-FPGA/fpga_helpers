fpga_device "5CSEBA6U23I7"

fpga_file "../hdl/blinking.vhdl"     -lib "examples"
fpga_file "../hdl/examples_pkg.vhdl" -lib "examples"
fpga_file "de10nano.vhdl"            -top "Top"
fpga_file "de10nano.tcl"

set fpga_pos 2
