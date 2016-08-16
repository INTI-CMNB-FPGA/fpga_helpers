doc_DATA          = tutorial.pdf
CLEANFILES        = *.aux *.log *.nav *.snm *.out *.toc *.pdf *.vrb
EXTRA_DIST        = tutorial.tex

clean-local:
	-rm -rf temp

tutorial.pdf: tutorial.tex
	mkdir -p temp
	echo '$$ fpga_setup --help'              > temp/fpgasetup1.txt
	bash ../../src/fpga_setup.sh --help     >> temp/fpgasetup1.txt
	echo '$$ fpga_setup'                     > temp/fpgasetup2.txt
	bash ../../src/fpga_setup.sh --quit     >> temp/fpgasetup2.txt
	echo '$$ fpga_synt --help'               > temp/fpgasynt.txt
	python ../../src/fpga_synt.py --help    >> temp/fpgasynt.txt
	mkdir -p temp/fpgasynt;                                         \
	cd temp/fpgasynt;                                               \
	rm *;                                                           \
	echo '$$ fpga_synt ise'                  > ../fpgasynt_ex1.txt; \
	python ../../../../src/fpga_synt.py ise >> ../fpgasynt_ex1.txt; \
	echo '$$ ls'                            >> ../fpgasynt_ex1.txt; \
	ls -C                                   >> ../fpgasynt_ex1.txt; \
	echo '$$ fpga_synt all'                  > ../fpgasynt_ex2.txt; \
	python ../../../../src/fpga_synt.py all >> ../fpgasynt_ex2.txt; \
	echo '$$ ls'                            >> ../fpgasynt_ex2.txt; \
	ls -C                                   >> ../fpgasynt_ex2.txt; \
	cp options.tcl                             ../options.txt;      \
	echo '$$ make help'                      > ../makefile.txt;     \
	make --no-print-directory help          >> ../makefile.txt
	pdflatex $<
	pdflatex $<
	@rm -fr *.aux *.log *.nav *.snm *.out *.toc *.vrb
