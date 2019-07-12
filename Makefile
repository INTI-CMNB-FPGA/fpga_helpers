#!/usr/bin/make

all:

install:
	pip install --user .

uninstall:
	pip uninstall fpgahelpers

clean:
	@rm -fr dist *.egg-info
