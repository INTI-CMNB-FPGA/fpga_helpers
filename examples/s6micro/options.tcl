fpga_device "XC6SLX9-2-CSG324"

fpga_file "../hdl/blinking.vhdl"     -lib "examples"
fpga_file "../hdl/examples_pkg.vhdl" -lib "examples"
fpga_file "s6micro.vhdl"             -top "Top"
fpga_file "s6micro.ucf"

set fpga_pos  1
set spi_width 1
set spi_name  W25Q64BV
set bpi_width 8
set bpi_name  28F128J3D
