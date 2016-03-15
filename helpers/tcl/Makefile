#!/usr/bin/make
#
# Makefile of the Vendor independat Tcl for FPGA Tools
# Copyright (C) 2016 INTI, Rodrigo A. Melo <rmelo@inti.gob.ar>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

ISE_BITS           = 64
ISE_ROOT_PATH      = /opt/Xilinx/ise
VIVADO_ROOT_PATH   = /opt/Xilinx/vivado
QUARTUS2_ROOT_PATH = /opt/Altera/quartus2

###################################################################################################

ifneq ("$(wildcard vivado_cfg.tcl)","")
   TOOL = vivado
else ifneq ("$(wildcard ise_cfg.tcl)","")
   TOOL = ise
else ifneq ("$(wildcard quartus2_cfg.tcl)","")
   TOOL = quartus2
else
   $(error You have to have at least one <vendorTool>_cfg.tcl file)
endif

TCL_FILE = fpga.tcl

ISE_TCL          = $(ISE_ROOT_PATH)/ISE/bin/lin$(ISE_BITS)/xtclsh $(TCL_FILE)
ISE_TCL_CON      = $(ISE_ROOT_PATH)/ISE/bin/lin$(ISE_BITS)/xtclsh
ISE_GUI          = $(ISE_ROOT_PATH)/ISE/bin/lin$(ISE_BITS)/ise ise.xise

VIVADO_TCL       = $(VIVADO_ROOT_PATH)/bin/vivado -mode batch -notrace -source $(TCL_FILE) -tclargs
VIVADO_TCL_CON   = $(VIVADO_ROOT_PATH)/bin/vivado -mode tcl
VIVADO_GUI       = $(VIVADO_ROOT_PATH)/bin/vivado temp-vivado/vivado.xpr

QUARTUS2_TCL     = $(QUARTUS2_ROOT_PATH)/quartus/bin/quartus_sh --script $(TCL_FILE)
QUARTUS2_TCL_CON = $(QUARTUS2_ROOT_PATH)/quartus/bin/quartus_sh -s
QUARTUS2_GUI     = $(QUARTUS2_ROOT_PATH)/quartus/bin/quartus quartus2.qpf

ifeq ($(TOOL),ise)
   TCL_CMD  = $(ISE_TCL)
   TCL_CON  = $(ISE_TCL_CON)
   GUI_CMD  = $(ISE_GUI)
else ifeq ($(TOOL),vivado)
   TCL_CMD  = $(VIVADO_TCL)
   TCL_CON  = $(VIVADO_TCL_CON)
   GUI_CMD  = $(VIVADO_GUI)
else ifeq ($(TOOL),quartus2)
   TCL_CMD  = $(QUARTUS2_TCL)
   TCL_CON  = $(QUARTUS2_TCL_CON)
   GUI_CMD  = $(QUARTUS2_GUI)
else
   $(error TOOL is unsupported [ise, vivado, quartus2])
endif

###################################################################################################

all help:
	@echo "Help:"
	@echo "* Main targets:"
	@echo "  * syn: synthesis"
	@echo "  * imp: implementation"
	@echo "  * bit: bitstream"
	@echo "* Optimized variations:"
	@echo "  * syn-area, syn-power, syn-speed"
	@echo "  * imp-area, imp-power, imp-speed"
	@echo "  * bit-area, bit-power, bit-speed"
	@echo "* Others:"
	@echo "  * clean:   to delete generated files"
	@echo "  * TCL_CON: to lunch the Tcl TCL_CON of the vendor Tool"
	@echo "  * gui:     to lunch the Gui of the vendor Tool"
	@echo "* Tools:"
	@echo "  * To specify use TOOL=<vendorTool> when do make"
	@echo "  * The supported vendorTool values are: ise, vivado, quartus2"

syn:
	$(TCL_CMD) -tool $(TOOL) -run syn
syn-area:
	$(TCL_CMD) -tool $(TOOL) -run syn -opt area
syn-speed:
	$(TCL_CMD) -tool $(TOOL) -run syn -opt speed
syn-power:
	$(TCL_CMD) -tool $(TOOL) -run syn -opt power

imp:
	$(TCL_CMD) -tool $(TOOL) -run imp
imp-area:
	$(TCL_CMD) -tool $(TOOL) -run imp -opt area
imp-speed:
	$(TCL_CMD) -tool $(TOOL) -run imp -opt speed
imp-power:
	$(TCL_CMD) -tool $(TOOL) -run imp -opt power

bit:
	$(TCL_CMD) -tool $(TOOL) -run bit
bit-area:
	$(TCL_CMD) -tool $(TOOL) -run bit -opt area
bit-speed:
	$(TCL_CMD) -tool $(TOOL) -run bit -opt speed
bit-power:
	$(TCL_CMD) -tool $(TOOL) -run bit -opt power

clean:
	$(TCL_CMD) -tool $(TOOL) -run clean

clean-all:
	$(ISE_TCL) -tool ise -run clean
	$(VIVADO_TCL) -tool vivado -run clean
	$(QUARTUS2_TCL) -tool quartus2 -run clean

console:
	$(TCL_CON)

gui:
	$(GUI_CMD)

