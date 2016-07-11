#!/usr/bin/make
#
# Makefile for Synthesis with Tcl files (FPGA Helpers)
# Copyright (C) 2016 INTI, Rodrigo A. Melo
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
###############################################################################

ifneq ("$(wildcard vivado.tcl)","")
   TOOL = vivado
else ifneq ("$(wildcard ise.tcl)","")
   TOOL = ise
else ifneq ("$(wildcard quartus2.tcl)","")
   TOOL = quartus2
else
   $(error You have to have at least one <vendorTool>.tcl file)
endif

TCL_FILE           = $(TOOL).tcl

ISE_TCL            = xtclsh $(TCL_FILE)
ISE_TCL_CON        = xtclsh
ISE_GUI            = ise ise.xise
ISE_CLEAN          = _ngo xst xlnx_auto_0_xdb _xmsgs *.bgn *.bld *.cmd_log  \
                     *.csv *.html *.lso *.map *.mrp *.ncd *.ngc *.ngd *.ngm \
                     *.ngr *.pad *.par *.pcf *.prj *.ptwx *.stx *.syr *.twr \
                     *.twx *.unroutes *.ut *.txt *.xml *.xpi *.xrpt *.xst   \
                     *.log *.gise
ISE_CLEAN_ALL      = $(ISE_CLEAN) *.xise

VIVADO_TCL         = vivado -mode batch -notrace -source $(TCL_FILE) -tclargs
VIVADO_TCL_CON     = vivado -mode tcl
VIVADO_GUI         = vivado temp-vivado/vivado.xpr
VIVADO_CLEAN       = *.cache *.hw *.ip_user_files *.jou *.log *.rpt *.runs
VIVADO_CLEAN_ALL   = $(VIVADO_CLEAN) *.xpr

QUARTUS2_TCL       = quartus_sh --script $(TCL_FILE)
QUARTUS2_TCL_CON   = quartus_sh -s
QUARTUS2_GUI       = quartus quartus2.qpf
QUARTUS2_CLEAN     = db incremental_db *.done *.jdi *.log *.pin *.qpf *.rpt \
                     *.sld *.sof *.summary *.txt
QUARTUS2_CLEAN_ALL = $(QUARTUS2_CLEAN) *.qsf

ifeq ($(TOOL),ise)
   TCL_CMD   = $(ISE_TCL)
   TCL_CON   = $(ISE_TCL_CON)
   GUI_CMD   = $(ISE_GUI)
   CLEAN     = $(ISE_CLEAN)
   CLEAN_ALL = $(ISE_CLEAN_ALL)
else ifeq ($(TOOL),vivado)
   TCL_CMD   = $(VIVADO_TCL)
   TCL_CON   = $(VIVADO_TCL_CON)
   GUI_CMD   = $(VIVADO_GUI)
   CLEAN     = $(VIVADO_CLEAN)
   CLEAN_ALL = $(VIVADO_CLEAN_ALL)
else ifeq ($(TOOL),quartus2)
   TCL_CMD   = $(QUARTUS2_TCL)
   TCL_CON   = $(QUARTUS2_TCL_CON)
   GUI_CMD   = $(QUARTUS2_GUI)
   CLEAN     = $(QUARTUS2_CLEAN)
   CLEAN_ALL = $(QUARTUS2_CLEAN_ALL)
else
   $(error TOOL is unsupported [ise, vivado, quartus2])
endif

###############################################################################

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
	@echo "  * console: to lunch the Tcl Console of the vendor Tool"
	@echo "  * gui:     to lunch the Gui of the vendor Tool"
	@echo "* Tools:"
	@echo "  * To specify use TOOL=<vendorTool> when do make"
	@echo "  * The supported vendorTool values are: ise, vivado, quartus2"

syn:
	$(TCL_CMD) -run syn
syn-area:
	$(TCL_CMD) -run syn -opt area
syn-speed:
	$(TCL_CMD) -run syn -opt speed
syn-power:
	$(TCL_CMD) -run syn -opt power

imp:
	$(TCL_CMD) -run imp
imp-area:
	$(TCL_CMD) -run imp -opt area
imp-speed:
	$(TCL_CMD) -run imp -opt speed
imp-power:
	$(TCL_CMD) -run imp -opt power

bit:
	$(TCL_CMD) -run bit
bit-area:
	$(TCL_CMD) -run bit -opt area
bit-speed:
	$(TCL_CMD) -run bit -opt speed
bit-power:
	$(TCL_CMD) -run bit -opt power

clean:
	@rm -fr $(CLEAN)

clean-all:
	@rm -fr $(CLEAN_ALL)

total-clean:
	@rm -fr $(ISE_CLEAN_ALL)
	@rm -fr $(VIVADO_CLEAN_ALL)
	@rm -fr $(QUARTUS2_CLEAN_ALL)

console:
	$(TCL_CON)

gui:
	$(GUI_CMD)

###############################################################################

