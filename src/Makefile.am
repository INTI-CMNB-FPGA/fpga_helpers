bin_SCRIPTS       = fpga_setup fpga_synt fpga_prog
CLEANFILES        = $(bin_SCRIPTS)
EXTRA_DIST        = fpga_setup.sh fpga_synt.py fpga_prog.py
dist_pkgdata_DATA = fpga_lib.py

fpga_setup: fpga_setup.sh
	cp $< $@

fpga_synt: fpga_synt.py
	cp $< $@

fpga_prog: fpga_prog.py
	cp $< $@

