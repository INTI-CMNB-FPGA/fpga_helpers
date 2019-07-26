fpga_device "xc7z010-1-clg400"

fpga_file "../hdl/blinking.vhdl"     -lib "examples"
fpga_file "../hdl/examples_pkg.vhdl" -lib "examples"
fpga_file "zybo.vhdl"                -top "Top"
fpga_file "zybo.xdc"
