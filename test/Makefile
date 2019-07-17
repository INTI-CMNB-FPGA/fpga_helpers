#!/usr/bin/make

SRCDIR = ../fpgahelpers

FPGAPROG = $(SRCDIR)/fpga_prog.py
FPGASYNT = $(SRCDIR)/fpga_synt.py
FPGAWZRD = $(SRCDIR)/fpga_wizard.py

SCRIPTS  = $(FPGAPROG) $(FPGASYNT) $(FPGAWZRD)

PYTHONS  = python2 python3

test: test-help

test-help:
	@$(foreach PYTHON,$(PYTHONS), \
		$(foreach SCRIPT,$(SCRIPTS), \
			echo "\n\n$(SCRIPT) ($(PYTHON))\n";\
			$(PYTHON) $(SCRIPT) --help;\
		) \
	)
