#!/usr/bin/make
# by RAM

%.pdf: %.tex
	pdflatex $<
	pdflatex $<
	@rm -fr *.aux *.log *.nav *.snm *.out *.toc

all: tutorial.pdf

clean:
	@rm -fr *.aux *.log *.nav *.snm *.out *.toc *.pdf
