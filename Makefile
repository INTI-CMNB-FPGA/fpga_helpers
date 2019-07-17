#!/usr/bin/make

.PHONY : test

all:

install:
	pip install --user .

uninstall:
	pip uninstall fpgahelpers

test:
	make -C test

clean:
	@rm -fr fpgahelpers/*.pyc fpgahelpers/__pycache__
	@rm -fr dist *.egg-info .eggs
