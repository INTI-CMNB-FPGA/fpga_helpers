doc_DATA          = tutorial.pdf
CLEANFILES        = *.aux *.log *.nav *.snm *.out *.toc *.pdf *.vrb
EXTRA_DIST        = tutorial.tex

tutorial.pdf: tutorial.tex
	pdflatex $<
	pdflatex $<
	@rm -fr *.aux *.log *.nav *.snm *.out *.toc *.vrb
