fpga_device "mpf300ts-1-fcg1152"

fpga_file "../hdl/blinking.vhdl"     -lib "examples"
fpga_file "../hdl/examples_pkg.vhdl" -lib "examples"
fpga_file "mpf300eval.vhdl"          -top "Top"
fpga_file "mpf300eval.pdc"
