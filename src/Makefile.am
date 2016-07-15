bin_SCRIPTS       = fpga_prepare fpga_make_syn fpga_prog
CLEANFILES        = $(bin_SCRIPTS)
EXTRA_DIST        = fpga_prepare.sh fpga_make_syn.py fpga_prog.py
dist_pkgdata_DATA = fpga_lib.py

fpga_prepare: fpga_prepare.sh
	cp $< $@

fpga_make_syn: fpga_make_syn.py
	cp $< $@

fpga_prog: fpga_prog.py
	cp $< $@

