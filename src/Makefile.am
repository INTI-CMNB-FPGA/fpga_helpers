bin_SCRIPTS       = fpga_deps fpga_prog fpga_setup fpga_synt fpga_wizard
CLEANFILES        = $(bin_SCRIPTS)
EXTRA_DIST        = database.py fpga_deps.py fpga_prog.py fpga_setup.sh fpga_synt.py fpga_wizard.py

dbdir             = $(pkgdatadir)
db_DATA           = database.py

fpga_deps: fpga_deps.py
	cp $< $@

fpga_prog: fpga_prog.py
	cp $< $@

fpga_synt: fpga_synt.py
	cp $< $@

fpga_setup: fpga_setup.sh
	cp $< $@

fpga_wizard: fpga_wizard.py
	cp $< $@
