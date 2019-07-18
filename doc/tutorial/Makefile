#!/usr/bin/make

VERSION = $(shell sed -ne 's/.*\([0-9]\+\.[0-9]\+\.[0-9]\+\).*/\1/p' ../../fpgahelpers/database.py)

SRCDIR  = ../../fpgahelpers

vpath %      temp

tutorial.pdf: tutorial.tex version setup_help setup_run prog synt wizard makefile
	pdflatex $<
	pdflatex $<
	@rm -fr *.aux *.log *.nav *.snm *.out *.toc *.vrb

temp/version:
	mkdir -p temp
	@echo $(VERSION)                                          > $@

temp/setup_help:
	mkdir -p temp
	echo '$$ fpga_setup --help'                               > $@
	bash $(SRCDIR)/fpga_setup.sh --help                      >> $@

temp/setup_run:
	mkdir -p temp
	echo '$$ fpga_setup'                                      > $@
	bash $(SRCDIR)/fpga_setup.sh --quit                      >> $@

temp/prog:
	mkdir -p temp
	echo '$$ fpga_prog --help'                                > $@
	python $(SRCDIR)/fpga_prog.py --help                     >> $@
	cp $@ temp/prog1
	sed -i '1,14!d' temp/prog1
	cp $@ temp/prog2
	sed -i '1,14d' temp/prog2

temp/synt:
	mkdir -p temp
	echo '$$ fpga_synt --help'                                > $@
	python $(SRCDIR)/fpga_synt.py --help                     >> $@

temp/wizard:
	mkdir -p temp
	cp ../../test/fpga_deps/top.vhdl temp
	cd temp; python ../$(SRCDIR)/fpga_wizard.py --default     > wizard
	rm -fr tcl

temp/makefile:
	echo '$$ make help'                                       > $@
	make --no-print-directory -f $(SRCDIR)/tcl/Makefile help >> $@

clean:
	-rm -rf temp

clean-all: clean
	-rm -rf tutorial.pdf

