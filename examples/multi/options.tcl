# For Synthesis ###############################################################

# Function: fpga_device   <FPGA> [-tool <TOOL>]     Return: none
#   Use -tool <TOOL> to specify FPGAs from different vendors.
#   Useful when comparing synthesis results between vendors.
# Function: fpga_file     <FILE> [-lib <LIBRARY>]   Return: none
#   Use -lib to specify a library which is not work (only VHDL).
# Function: fpga_file     <FILE> [-top <TOPNAME>]   Return: none
#   Use -top to specify as top level and the component name.
# Constant: $FPGA_TOOL                              Name of the running tool
#   Useful to specify options for a particular vendor tool.

fpga_device "XC6SLX9-2-CSG324"  -tool "ise"
fpga_device "xc7a100t-3-csg324" -tool "vivado"
fpga_device "5CGXFC7C7F23C8"    -tool "quartus"
fpga_device "M2S090TS-1-fg484"  -tool "libero"

fpga_file "../hdl/blinking.vhdl"     -lib "examples"
fpga_file "../hdl/examples_pkg.vhdl" -lib "examples"

if {$FPGA_TOOL == "ise"} {
   fpga_file "../s6micro/s6micro.vhdl"       -top "Top"
   fpga_file "../s6micro/s6micro.ucf"
} elseif {$FPGA_TOOL == "vivado"} {
   fpga_file "../zybo/zybo.vhdl"             -top "Top"
   fpga_file "../zybo/zybo.xdc"
} elseif {$FPGA_TOOL == "quartus"} {
   fpga_file "../max10eval/max10eval.vhdl"   -top "Top"
   fpga_file "../max10eval/max10eval.tcl"
} elseif {$FPGA_TOOL == "libero"} {
   fpga_file "../mpf300eval/mpf300eval.vhdl" -top "Top"
   fpga_file "../mpf300eval/mpf300eval.pdc"
}

# For Programming #############################################################

# _pos:   position in jtag chain
# _width: data bits
# _name:  name of the memory

set fpga_pos  1
set spi_width 1
set spi_name  W25Q64BV
set bpi_width 8
set bpi_name  28F128J3D
