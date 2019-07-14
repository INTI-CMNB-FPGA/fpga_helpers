#!/usr/bin/make

all:

install:
	pip install --user .

uninstall:
	pip uninstall fpgahelpers

clean:
	@rm fpgahelpers/*.pyc
	@rm -fr dist *.egg-info .eggs
