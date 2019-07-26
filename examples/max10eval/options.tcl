fpga_device "10M08SAE144C8G"

fpga_file "../hdl/blinking.vhdl"     -lib "examples"
fpga_file "../hdl/examples_pkg.vhdl" -lib "examples"
fpga_file "max10eval.vhdl"           -top "Top"
fpga_file "max10eval.tcl"
