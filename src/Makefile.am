bin_SCRIPTS       = fpga_prepare fpga_synt fpga_prog
CLEANFILES        = $(bin_SCRIPTS)
EXTRA_DIST        = fpga_prepare.sh fpga_synt.py fpga_prog.py
dist_pkgdata_DATA = fpga_lib.py

fpga_prepare: fpga_prepare.sh
	cp $< $@

fpga_synt: fpga_synt.py
	cp $< $@

fpga_prog: fpga_prog.py
	cp $< $@

