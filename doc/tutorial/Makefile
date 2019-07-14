doc_DATA          = tutorial.pdf
CLEANFILES        = *.aux *.log *.nav *.snm *.out *.toc *.pdf *.vrb
EXTRA_DIST        = tutorial.tex

clean-local:
	-rm -rf temp

temp/fpgasetup1.txt:
	mkdir -p temp
	echo '$$ fpga_setup --help'                                       > temp/fpgasetup1.txt
	bash ../../fpgahelpers/fpga_setup.sh --help                      >> temp/fpgasetup1.txt

temp/fpgasetup2.txt:
	mkdir -p temp
	echo '$$ fpga_setup'                                              > temp/fpgasetup2.txt
	bash ../../fpgahelpers/fpga_setup.sh --quit                      >> temp/fpgasetup2.txt

temp/fpgasynt.txt:
	mkdir -p temp
	echo '$$ fpga_synt --help'                                        > temp/fpgasynt.txt
	python ../../fpgahelpers/fpga_synt.py --help                     >> temp/fpgasynt.txt

temp/makefile.txt:
	echo '$$ make help'                                               > temp/makefile.txt
	make --no-print-directory -f ../../fpgahelpers/tcl/Makefile help >> temp/makefile.txt

tutorial.pdf: tutorial.tex temp/fpgasetup1.txt temp/fpgasetup2.txt temp/fpgasynt.txt temp/makefile.txt
	pdflatex $<
	pdflatex $<
	@rm -fr *.aux *.log *.nav *.snm *.out *.toc *.vrb
