# Changelog

## [v0.4.0] - unreleased
* Moved from Autotools and a Debian package to Python pip.
* The source code of mainly fpga_prog, fpga_synth and fpga_wizard, was improved/simplified.
* The files structure of the repository was modified and simplified.
* The documentation was reordered, simplified and slightly improved.
* A Dockerfile with scripts to build and run an image/container were added to the repository.
  * It mainly contains Free Software tools for HDL simulation (GHDL, iVerilog, Cocotb and GtkWave).

## [v0.3.0] - 2017-08-18
* Unified again Tcl scripts for synthesis.
* Unified programming in a Tcl script. Added support for Vivado.
* Improved Tcl scripts and its Makefile.
* Renamed quartus2 and libero-soc to quartus and libero.
* Added fpga_wizard.py to help to obtain options.tcl and Makefile. It replaces old fpga_synt.py.
* New fpga_synt.py. It helps to do synthesis based on the project file of a vendor's tool.
* Modified fpga_prog.py. Now it use the Tcl script for programming.
* YAML files were replaced by data in database.py (shared database).
* Added the User Guide (English and Spanish).
* The tutorial was updated.

## [v0.2.0] - 2017-01-13 
* Code of Tcl scripts and Makefile were improved.
* Added a Tcl script for Libero-SoC.
* Added support for Libero-SoC on fpga_synt.py and fpga_prog.py.
* Added fpga_deps.py [WIP].
* Added Board files: microsemi_m2s090ts-eval-kit.yaml and xilinx_ml605.yaml.

## [v0.1.1] - 2016-08-17
* Tcl script splitted (one per each vendor) and improved.
* Added fpga_setup.sh, fpga_synt.py and fpga_prog.py.
  * fpga_setup.sh: set the system to run vendor tools.
    * Allows configuration of paths and licenses.
    * Supports ISE, Vivado, Quartus2 and Libero-SoC.
  * fpga_synt.py: copy Tcl files and Makefile to the current directory.
  * fpga_prog.py: transfer a bitstream.
    * Supports ISE impact (transfer to fpga, spi, bpi and one xcf).
    * Supports Quartus2 (transfer to fpga).
* Added a brief tutorial (presentation).
* Added Board files: avnet_s6micro, digilent_atlys, gaisler_xc6s, terasic_de0nano and xilinx_sp601.
* Added autotools use and debian package creation.

## [v0.1.0] - 2016-07-07 
* Includes a Tcl script and Makefile to work with FPGA Tools in a Vendor Independent way.
* It supports synthesis/implementation (not programming yet):
  * From Xilinx: ISE and Vivado.
  * From Altera: Quartus2.
