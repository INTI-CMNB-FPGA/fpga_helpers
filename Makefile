#!/usr/bin/make

.PHONY : doc test

all:

doc:
	make -C doc/tutorial

install:
	pip install --user .

uninstall:
	pip uninstall fpgahelpers

test:
	make -C test

clean:
	@rm -fr fpgahelpers/*.pyc fpgahelpers/__pycache__
	@rm -fr dist *.egg-info .eggs
	make -C doc/tutorial clean-all
