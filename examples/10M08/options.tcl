fpga_device "10M08SAE144C8G"

fpga_file "../hdl/blinking.vhdl"     -lib "examples"
fpga_file "../hdl/examples_pkg.vhdl" -lib "examples"
fpga_file "10m08.vhdl"               -top "Top"
fpga_file "10m08.tcl"
